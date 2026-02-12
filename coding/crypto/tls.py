"""
usage: {0} <mode> [<options>]

modes:
  genkeys < PRIMES             generate RSA keys for the server
  server HOST PORT KEYFILE     start a secured server
  client HOST PORT PUBKEYFILE  connect a secured client

examples:
  # generate the RSA key pair for the server (takes two primes as input)
  {{ openssl prime --generate --bits 1024 \\
  & openssl prime --generate --bits 1024; }} | python {0} genkeys

  # alternative: enter primes interactively
  python {0} genkeys < PRIMES

  # start the server (reads the private key)
  python {0} server localhost 4433 key.priv

  # connect the client (reads the server's public key)
  python {0} client localhost 4433 key.pub

  # pipe data through the secure channel (works like nc)
  python {0} client localhost 4433 key.pub > output.file
  python {0} client localhost 4433 key.pub < input.file

protocol:
  A rudimentary TLS-like protocol using DHE-RSA key exchange:
  1. ClientHello:      client sends version + random nonce
  2. ServerHello:      server sends version + random nonce + RSA public key
                       + DH group + DH public key + signature of DH params
  3. ClientKeyExchange: client sends its DH public key
  4. Finished:         both sides exchange HMAC of handshake transcript
  5. Application data: AES-CBC encrypted + HMAC authenticated records

note: this is an educational implementation, not suitable for production use
"""
# see https://en.wikipedia.org/wiki/Transport_Layer_Security
#     https://www.ietf.org/rfc/rfc5246.txt (TLS 1.2)
#     https://www.ietf.org/rfc/rfc5116.txt (AEAD)

import json
from os import urandom
import socket
import struct
from io import BytesIO
from math import ceil
from enum import Enum

import aes
import dh
import hmac
import rsa
import sha2

PROTOCOL_VERSION = "TINY-TLS-1.0"


class MsgType(Enum):
    CLIENT_HELLO = "ClientHello"
    SERVER_HELLO = "ServerHello"
    CLIENT_KEY_EXCHANGE = "ClientKeyExchange"
    CLIENT_FINISHED = "ClientFinished"
    SERVER_FINISHED = "ServerFinished"

DH_GROUP_ID = 1  # 2048-bit MODP Group (RFC 3526)
DH_KEY_SIZE = 256  # bits
AES_KEY_SIZE = 256  # bits
HMAC_DIGEST = sha2.SHA512_256
HMAC_SIZE = 32  # bytes (SHA512/256 output)
RANDOM_SIZE = 32  # bytes
MAX_RECORD_SIZE = 1 << 16  # 64 KB max record size
# CBC overhead: 16-byte IV + up to 16 bytes PKCS#7 padding + 32-byte HMAC
MAX_DATA_SIZE = MAX_RECORD_SIZE - 16 - 16 - HMAC_SIZE


class TinyTLSHandshakeError(Exception):
    pass


class TinyTLSRecordError(Exception):
    pass


class TinyTLSConnection:
    """
    A rudimentary TLS-like connection wrapping a TCP socket.

    Provides a DHE-RSA handshake to establish a shared secret, then uses
    AES-CBC for encryption and HMAC-SHA512/256 for message authentication
    (encrypt-then-MAC).
    """

    def __init__(self, sock, server_rsa_keys=None):
        """
        Wrap a connected TCP socket _sock_.

        For server mode, _server_rsa_keys_ must be a tuple (e, d, n) with the
        full RSA key material. For client mode, it can be omitted.
        """
        self._sock = sock
        self._server_rsa_keys = server_rsa_keys
        self._send_enc_key = None
        self._recv_enc_key = None
        self._send_mac_key = None
        self._recv_mac_key = None
        self._send_seq = 0
        self._recv_seq = 0
        self._transcript = b""

    def _send_msg(self, data):
        """Send a length-prefixed message over the socket."""
        header = struct.pack("!I", len(data))
        self._sock.sendall(header + data)

    def _recv_msg(self):
        """Receive a length-prefixed message from the socket."""
        header = self._recv_exact(4)
        length = struct.unpack("!I", header)[0]
        if length > MAX_RECORD_SIZE:
            raise TinyTLSRecordError("record too large")
        return self._recv_exact(length)

    def _recv_exact(self, n):
        """Receive exactly _n_ bytes from the socket."""
        buf = bytearray()
        while len(buf) < n:
            chunk = self._sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("connection closed")
            buf.extend(chunk)
        return bytes(buf)

    def _send_handshake(self, msg):
        """JSON-encode and send a handshake message, appending to transcript."""
        data = json.dumps(msg, sort_keys=True).encode()
        self._transcript += data
        self._send_msg(data)

    def _recv_handshake(self):
        """Receive and JSON-decode a handshake message, appending to transcript."""
        data = self._recv_msg()
        self._transcript += data
        return json.loads(data)

    @staticmethod
    def _derive_keys(shared_secret_bytes, client_random, server_random):
        """
        Derive directional encryption and MAC keys from the DH shared secret
        using HMAC-SHA512/256.

        Returns (client_enc_key, server_enc_key, client_mac_key, server_mac_key).
        """
        nonces = client_random + server_random
        client_enc_key = _hmac(shared_secret_bytes, b"client enc" + nonces)
        server_enc_key = _hmac(shared_secret_bytes, b"server enc" + nonces)
        client_mac_key = _hmac(shared_secret_bytes, b"client mac" + nonces)
        server_mac_key = _hmac(shared_secret_bytes, b"server mac" + nonces)
        return client_enc_key, server_enc_key, client_mac_key, server_mac_key


    def handshake_server(self):
        """
        Perform the server side of the TLS-like handshake.

        Requires _server_rsa_keys_ to have been set in __init__.

        Steps:
        1. Receive ClientHello
        2. Send ServerHello with DH parameters + RSA signature
        3. Receive ClientKeyExchange
        4. Derive session keys
        5. Exchange Finished messages
        """
        e, d, n = self._server_rsa_keys
        dhgroup = dh.GROUPS[DH_GROUP_ID]

        # 1. ClientHello
        client_hello = self._recv_handshake()
        if client_hello.get("type") != MsgType.CLIENT_HELLO.value:
            raise TinyTLSHandshakeError("expected ClientHello")
        if client_hello.get("version") != PROTOCOL_VERSION:
            raise TinyTLSHandshakeError("unsupported protocol version")
        client_random = bytes.fromhex(client_hello["random"])

        # 2. ServerHello: generate DH key pair and sign the parameters
        server_random = urandom(RANDOM_SIZE)
        dh_private = dh.generate_private_key(DH_KEY_SIZE)
        dh_public = dh.generate_public_key(dhgroup.g, dhgroup.p, dh_private)

        # sign: DH group id + DH public key + client_random + server_random
        sign_data = _dh_sign_payload(DH_GROUP_ID, dh_public, client_random,
                                     server_random)
        sig_io = BytesIO()
        rsa.sign(BytesIO(sign_data), sig_io, d, n)
        signature = sig_io.getvalue()

        self._send_handshake({
            "type": MsgType.SERVER_HELLO.value,
            "version": PROTOCOL_VERSION,
            "random": server_random.hex(),
            "rsa_n": hex(n),
            "rsa_e": hex(e),
            "dh_group": DH_GROUP_ID,
            "dh_public": hex(dh_public),
            "signature": signature.hex(),
        })

        # 3. ClientKeyExchange
        client_kex = self._recv_handshake()
        if client_kex.get("type") != MsgType.CLIENT_KEY_EXCHANGE.value:
            raise TinyTLSHandshakeError("expected ClientKeyExchange")
        client_dh_public = int(client_kex["dh_public"], 16)

        # validate the client's DH public key
        if not dh.check_public_key(dhgroup.p, client_dh_public):
            raise TinyTLSHandshakeError("invalid client DH public key")

        # 4. Derive session keys
        shared_secret = dh.generate_shared_secret(
            dhgroup.p, dh_private, client_dh_public, check=False)
        if shared_secret < 2:
            raise TinyTLSHandshakeError("degenerate shared secret")
        shared_secret_bytes = shared_secret.to_bytes(
            max(1, ceil(shared_secret.bit_length() / 8)), "big")
        c_enc, s_enc, c_mac, s_mac = self._derive_keys(
            shared_secret_bytes, client_random, server_random)
        self._send_enc_key = s_enc
        self._recv_enc_key = c_enc
        self._send_mac_key = s_mac
        self._recv_mac_key = c_mac

        # 5. Finished: verify client's HMAC of transcript then send ours
        transcript_len = len(self._transcript)
        client_finished = self._recv_handshake()
        if client_finished.get("type") != MsgType.CLIENT_FINISHED.value:
            raise TinyTLSHandshakeError("expected ClientFinished")
        expected_client_verify = _hmac(c_mac, self._transcript[:transcript_len])
        if not _constant_time_compare(
                bytes.fromhex(client_finished["verify"]),
                expected_client_verify):
            raise TinyTLSHandshakeError("ClientFinished verification failed")

        # send our own Finished
        transcript_before_sf = self._transcript
        server_verify = _hmac(s_mac, transcript_before_sf)
        self._send_handshake({
            "type": MsgType.SERVER_FINISHED.value,
            "verify": server_verify.hex(),
        })

    def handshake_client(self, server_rsa_n, server_rsa_e):
        """
        Perform the client side of the TLS-like handshake.

        The client must know the server's RSA public key (n, e) in advance
        (analogous to a pinned/CA-trusted certificate).

        Steps:
        1. Send ClientHello
        2. Receive ServerHello, verify RSA signature on DH params
        3. Generate DH keypair, send ClientKeyExchange
        4. Derive session keys
        5. Exchange Finished messages
        """
        dhgroup = dh.GROUPS[DH_GROUP_ID]

        # 1. ClientHello
        client_random = urandom(RANDOM_SIZE)
        self._send_handshake({
            "type": MsgType.CLIENT_HELLO.value,
            "version": PROTOCOL_VERSION,
            "random": client_random.hex(),
        })

        # 2. ServerHello
        server_hello = self._recv_handshake()
        if server_hello.get("type") != MsgType.SERVER_HELLO.value:
            raise TinyTLSHandshakeError("expected ServerHello")
        if server_hello.get("version") != PROTOCOL_VERSION:
            raise TinyTLSHandshakeError("unsupported protocol version")

        server_random = bytes.fromhex(server_hello["random"])
        srv_n = int(server_hello["rsa_n"], 16)
        srv_e = int(server_hello["rsa_e"], 16)

        # verify the server's identity matches the pinned public key
        if srv_n != server_rsa_n or srv_e != server_rsa_e:
            raise TinyTLSHandshakeError("server RSA public key mismatch")

        dh_group_id = server_hello["dh_group"]
        server_dh_public = int(server_hello["dh_public"], 16)
        signature = bytes.fromhex(server_hello["signature"])

        # verify the RSA signature over the DH parameters
        sign_data = _dh_sign_payload(dh_group_id, server_dh_public,
                                     client_random, server_random)
        if not rsa.verify(BytesIO(sign_data), signature, srv_e, srv_n):
            raise TinyTLSHandshakeError("DH parameter signature verification failed")

        # validate the server's DH public key
        if not dh.check_public_key(dhgroup.p, server_dh_public):
            raise TinyTLSHandshakeError("invalid server DH public key")

        # 3. ClientKeyExchange: generate our DH key pair
        dh_private = dh.generate_private_key(DH_KEY_SIZE)
        dh_public = dh.generate_public_key(dhgroup.g, dhgroup.p, dh_private)

        self._send_handshake({
            "type": MsgType.CLIENT_KEY_EXCHANGE.value,
            "dh_public": hex(dh_public),
        })

        # 4. Derive session keys
        shared_secret = dh.generate_shared_secret(
            dhgroup.p, dh_private, server_dh_public, check=False)
        if shared_secret < 2:
            raise TinyTLSHandshakeError("degenerate shared secret")
        shared_secret_bytes = shared_secret.to_bytes(
            max(1, ceil(shared_secret.bit_length() / 8)), "big")
        c_enc, s_enc, c_mac, s_mac = self._derive_keys(
            shared_secret_bytes, client_random, server_random)
        self._send_enc_key = c_enc
        self._recv_enc_key = s_enc
        self._send_mac_key = c_mac
        self._recv_mac_key = s_mac

        # 5. Finished: send our HMAC of transcript, then verify server's
        transcript_before_cf = self._transcript
        client_verify = _hmac(c_mac, transcript_before_cf)
        self._send_handshake({
            "type": MsgType.CLIENT_FINISHED.value,
            "verify": client_verify.hex(),
        })

        transcript_len = len(self._transcript)
        server_finished = self._recv_handshake()
        if server_finished.get("type") != MsgType.SERVER_FINISHED.value:
            raise TinyTLSHandshakeError("expected ServerFinished")
        expected_server_verify = _hmac(s_mac, self._transcript[:transcript_len])
        if not _constant_time_compare(
                bytes.fromhex(server_finished["verify"]),
                expected_server_verify):
            raise TinyTLSHandshakeError("ServerFinished verification failed")

    def send(self, data):
        """
        Encrypt _data_ with AES-CBC and authenticate with
        HMAC-SHA512/256 (encrypt-then-MAC), then send over the socket.

        Record format: [4-byte length][ciphertext][32-byte HMAC]
        The ciphertext includes the IV prepended by aes.encrypt (CBC mode).
        The HMAC covers the sequence number (8 bytes) + ciphertext.
        """
        if self._send_enc_key is None:
            raise TinyTLSRecordError("handshake not completed")
        if len(data) > MAX_DATA_SIZE:
            raise TinyTLSRecordError(
                "data too large ({} bytes, max {})".format(
                    len(data), MAX_DATA_SIZE))

        # encrypt
        pt_io = BytesIO(data)
        ct_io = BytesIO()
        aes.encrypt(pt_io, ct_io, self._send_enc_key, moo=aes.MoO.CBC)
        ciphertext = ct_io.getvalue()

        # MAC over sequence number + ciphertext (encrypt-then-MAC)
        seq_bytes = struct.pack("!Q", self._send_seq)
        mac = _hmac(self._send_mac_key, seq_bytes + ciphertext)
        self._send_seq += 1

        self._send_msg(ciphertext + mac)

    def recv(self):
        """
        Receive a record, verify its HMAC, and decrypt the ciphertext.

        Returns the decrypted plaintext bytes.
        """
        if self._recv_enc_key is None:
            raise TinyTLSRecordError("handshake not completed")

        data = self._recv_msg()
        mac_size = HMAC_SIZE
        if len(data) <= mac_size:
            raise TinyTLSRecordError("record too short")

        ciphertext = data[:-mac_size]
        received_mac = data[-mac_size:]

        # verify MAC (sequence number + ciphertext)
        seq_bytes = struct.pack("!Q", self._recv_seq)
        expected_mac = _hmac(self._recv_mac_key, seq_bytes + ciphertext)
        if not _constant_time_compare(received_mac, expected_mac):
            raise TinyTLSRecordError("MAC verification failed")
        self._recv_seq += 1

        # decrypt
        ct_io = BytesIO(ciphertext)
        pt_io = BytesIO()
        aes.decrypt(ct_io, pt_io, self._recv_enc_key, moo=aes.MoO.CBC)
        return pt_io.getvalue()

    def close(self):
        """Close the underlying socket."""
        self._sock.close()

def _hmac(key, data):
    """Compute HMAC-SHA512/256 of _data_ using _key_."""
    return hmac.digest(BytesIO(data), key, digestcls=HMAC_DIGEST)


def _constant_time_compare(a, b):
    """Compare two byte strings in constant time to prevent timing attacks."""
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    return result == 0


def _dh_sign_payload(dh_group_id, dh_public, client_random, server_random):
    """
    Construct the payload to be signed/verified for DH parameter
    authentication.
    """
    return (str(dh_group_id).encode() + b":" +
            hex(dh_public).encode() + b":" +
            client_random + server_random)


def _io_loop(tlsc, server_sock=None):
    """
    Bidirectional forwarding: stdin -> remote, remote -> stdout.

    Reads raw bytes from stdin and sends them over the encrypted channel.
    Receives data from the encrypted channel and writes raw bytes to stdout.

    Works both interactively and when piped.
    Exits when either side closes.
    """
    import os
    import select
    import sys
    import threading

    BUF_SIZE = 4096
    # pipe used to wake up the stdin select() when the remote side closes
    wake_r, wake_w = os.pipe()
    stop = threading.Event()

    def recv_loop():
        try:
            while not stop.is_set():
                data = tlsc.recv()
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
        except (ConnectionError, TinyTLSRecordError):
            pass
        finally:
            stop.set()
            os.write(wake_w, b"\x00")

    t = threading.Thread(target=recv_loop, daemon=True)
    t.start()

    try:
        stdin_fd = sys.stdin.buffer.fileno()
        while not stop.is_set():
            readable, _, _ = select.select([stdin_fd, wake_r], [], [])
            if wake_r in readable or stop.is_set():
                break
            data = sys.stdin.buffer.read1(BUF_SIZE)
            if not data:
                break
            tlsc.send(data)
    except (KeyboardInterrupt, BrokenPipeError):
        pass
    finally:
        stop.set()
        os.close(wake_r)
        os.close(wake_w)
        tlsc.close()
        if server_sock:
            server_sock.close()


if __name__ == "__main__":
    import sys
    import threading

    if len(sys.argv) < 2:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "genkeys":
        p_line = sys.stdin.readline().strip()
        q_line = sys.stdin.readline().strip()
        if not p_line or not q_line:
            print("error: expected two large primes as input (one per line)",
                  file=sys.stderr)
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)
        p = int(p_line)
        q = int(q_line)
        e, d, n = rsa.genkeys(p, q)

        with open(rsa.PUBKEY_FILE, "w") as f:
            f.write(rsa.dumpkey(n, e))
        with open(rsa.PRIVKEY_FILE, "w") as f:
            # store n, e, d so the server can recover e without guessing
            f.write("{} {} {}".format(hex(n), hex(e), hex(d)))
        print("wrote keys to {} and {}".format(rsa.PUBKEY_FILE,
                                               rsa.PRIVKEY_FILE),
              file=sys.stderr)

    elif sys.argv[1] == "server":
        if len(sys.argv) < 5:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        host, port, keyfile = sys.argv[2], int(sys.argv[3]), sys.argv[4]
        with open(keyfile) as f:
            n, e, d = [int(v, 16) for v in f.read().split()]

        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((host, port))
        srv.listen(1)
        print("[server] listening on {}:{}".format(host, port),
              file=sys.stderr)

        conn, addr = srv.accept()
        print("[server] connection from {}".format(addr), file=sys.stderr)

        tlsc = TinyTLSConnection(conn, server_rsa_keys=(e, d, n))
        tlsc.handshake_server()
        print("[server] handshake complete", file=sys.stderr)

        _io_loop(tlsc, srv)

    elif sys.argv[1] == "client":
        if len(sys.argv) < 5:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        host, port, keyfile = sys.argv[2], int(sys.argv[3]), sys.argv[4]
        with open(keyfile) as f:
            n, e = rsa.loadkey(f.read())

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("[client] connected to {}:{}".format(host, port),
              file=sys.stderr)

        tlsc = TinyTLSConnection(sock)
        tlsc.handshake_client(n, e)
        print("[client] handshake complete", file=sys.stderr)

        _io_loop(tlsc)

    else:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
