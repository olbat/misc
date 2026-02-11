import socket
import struct
import threading
import unittest

import aes
import rsa
import tls


def _gen_test_rsa_keys():
    """
    Generate RSA keys using Python's built-in pow and random.

    Uses a probabilistic primality test (Miller-Rabin) to find primes,
    avoiding external dependencies like sympy.
    """
    from random import getrandbits, randrange

    def is_probable_prime(n, k=20):
        if n < 2:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        # write n-1 as 2^r * d
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        # Miller-Rabin witnesses
        for _ in range(k):
            a = randrange(2, n - 1)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    def gen_prime(bits):
        while True:
            p = getrandbits(bits) | (1 << (bits - 1)) | 1
            if is_probable_prime(p):
                return p

    p = gen_prime(1024)
    q = gen_prime(1024)
    e, d, n = rsa.genkeys(p, q)
    return e, d, n


# Generate keys once for all tests
_E, _D, _N = _gen_test_rsa_keys()


class TestKeyDerivation(unittest.TestCase):
    """Test that key derivation produces deterministic, distinct keys."""

    def test_derive_keys_deterministic(self):
        secret = b"shared secret material"
        cr = b"\x01" * tls.RANDOM_SIZE
        sr = b"\x02" * tls.RANDOM_SIZE

        keys1 = tls.TinyTLSConnection._derive_keys(secret, cr, sr)
        keys2 = tls.TinyTLSConnection._derive_keys(secret, cr, sr)

        self.assertEqual(keys1, keys2)

    def test_derive_keys_distinct(self):
        secret = b"shared secret material"
        cr = b"\x01" * tls.RANDOM_SIZE
        sr = b"\x02" * tls.RANDOM_SIZE

        c_enc, s_enc, c_mac, s_mac = tls.TinyTLSConnection._derive_keys(
            secret, cr, sr)
        keys = [c_enc, s_enc, c_mac, s_mac]

        for k in keys:
            self.assertEqual(len(k), tls.HMAC_SIZE)
        # all four keys must be pairwise distinct
        self.assertEqual(len(set(keys)), 4)

    def test_derive_keys_different_inputs(self):
        cr = b"\x01" * tls.RANDOM_SIZE
        sr = b"\x02" * tls.RANDOM_SIZE

        keys_a = tls.TinyTLSConnection._derive_keys(b"secret A", cr, sr)
        keys_b = tls.TinyTLSConnection._derive_keys(b"secret B", cr, sr)

        for ka, kb in zip(keys_a, keys_b):
            self.assertNotEqual(ka, kb)


class TestRecordProtocol(unittest.TestCase):
    """Test send/recv round-trip over a socket pair."""

    def _make_connected_pair(self):
        """Create a pair of TinyTLSConnections with pre-shared keys."""
        s1, s2 = socket.socketpair()
        tls1 = tls.TinyTLSConnection(s1)
        tls2 = tls.TinyTLSConnection(s2)

        # manually set directional session keys (bypass handshake)
        enc_a = aes.genkey(tls.AES_KEY_SIZE)
        enc_b = aes.genkey(tls.AES_KEY_SIZE)
        mac_a = b"\xab" * tls.HMAC_SIZE
        mac_b = b"\xcd" * tls.HMAC_SIZE

        # tls1 sends with keys "a", tls2 receives with keys "a"
        tls1._send_enc_key = enc_a
        tls1._recv_enc_key = enc_b
        tls1._send_mac_key = mac_a
        tls1._recv_mac_key = mac_b

        tls2._send_enc_key = enc_b
        tls2._recv_enc_key = enc_a
        tls2._send_mac_key = mac_b
        tls2._recv_mac_key = mac_a

        return tls1, tls2, s1, s2

    def test_send_recv_roundtrip(self):
        tls1, tls2, s1, s2 = self._make_connected_pair()
        try:
            plaintext = b"Hello, TLS!"
            tls1.send(plaintext)
            received = tls2.recv()
            self.assertEqual(received, plaintext)
        finally:
            s1.close()
            s2.close()

    def test_send_recv_empty(self):
        tls1, tls2, s1, s2 = self._make_connected_pair()
        try:
            # AES-CBC with PKCS7 padding handles empty messages
            # (produces one block of padding)
            tls1.send(b"")
            received = tls2.recv()
            self.assertEqual(received, b"")
        finally:
            s1.close()
            s2.close()

    def test_send_recv_large(self):
        tls1, tls2, s1, s2 = self._make_connected_pair()
        try:
            plaintext = b"A" * 4096
            tls1.send(plaintext)
            received = tls2.recv()
            self.assertEqual(received, plaintext)
        finally:
            s1.close()
            s2.close()

    def test_send_recv_multiple(self):
        tls1, tls2, s1, s2 = self._make_connected_pair()
        try:
            messages = [b"first", b"second", b"third"]
            for msg in messages:
                tls1.send(msg)
            for msg in messages:
                received = tls2.recv()
                self.assertEqual(received, msg)
        finally:
            s1.close()
            s2.close()

    def test_tampered_mac_rejected(self):
        tls1, tls2, s1, s2 = self._make_connected_pair()
        try:
            plaintext = b"sensitive data"
            tls1.send(plaintext)

            # intercept the raw message and tamper with the MAC
            header = tls2._recv_exact(4)
            length = struct.unpack("!I", header)[0]
            data = tls2._recv_exact(length)

            # flip a byte in the MAC (last 32 bytes)
            tampered = bytearray(data)
            tampered[-1] ^= 0xff
            tampered = bytes(tampered)

            # re-inject the tampered message into a new socket pair
            s3, s4 = socket.socketpair()
            tls3 = tls.TinyTLSConnection(s4)
            tls3._recv_enc_key = tls2._recv_enc_key
            tls3._recv_mac_key = tls2._recv_mac_key

            # send the tampered data with proper length header
            s3.sendall(struct.pack("!I", len(tampered)) + tampered)
            s3.close()

            with self.assertRaises(tls.TinyTLSRecordError):
                tls3.recv()

            s4.close()
        finally:
            s1.close()
            s2.close()

    def test_recv_before_handshake(self):
        s1, s2 = socket.socketpair()
        try:
            conn = tls.TinyTLSConnection(s1)
            with self.assertRaises(tls.TinyTLSRecordError):
                conn.recv()
        finally:
            s1.close()
            s2.close()


class TestHandshake(unittest.TestCase):
    """Test full handshake over a socket pair."""

    def test_full_handshake_and_communication(self):
        s1, s2 = socket.socketpair()
        server_conn = tls.TinyTLSConnection(s1, server_rsa_keys=(_E, _D, _N))
        client_conn = tls.TinyTLSConnection(s2)

        errors = []

        def server_side():
            try:
                server_conn.handshake_server()
            except Exception as exc:
                errors.append(exc)

        t = threading.Thread(target=server_side)
        t.start()

        try:
            client_conn.handshake_client(_N, _E)
            t.join(timeout=30)

            self.assertEqual(errors, [], "server handshake errors: {}".format(
                errors))

            # directional keys must be cross-matched
            self.assertEqual(server_conn._send_enc_key,
                             client_conn._recv_enc_key)
            self.assertEqual(server_conn._recv_enc_key,
                             client_conn._send_enc_key)
            self.assertEqual(server_conn._send_mac_key,
                             client_conn._recv_mac_key)
            self.assertEqual(server_conn._recv_mac_key,
                             client_conn._send_mac_key)

            # test bidirectional communication
            client_conn.send(b"hello from client")
            self.assertEqual(server_conn.recv(), b"hello from client")

            server_conn.send(b"hello from server")
            self.assertEqual(client_conn.recv(), b"hello from server")

        finally:
            s1.close()
            s2.close()

    def test_wrong_server_key_rejected(self):
        """Client rejects a server whose RSA key doesn't match the pinned one."""
        s1, s2 = socket.socketpair()
        server_conn = tls.TinyTLSConnection(s1, server_rsa_keys=(_E, _D, _N))

        # generate a different RSA key pair for the client to expect
        other_e, other_d, other_n = _gen_test_rsa_keys()

        errors = []

        def server_side():
            try:
                server_conn.handshake_server()
            except Exception as exc:
                errors.append(exc)

        t = threading.Thread(target=server_side)
        t.start()

        try:
            with self.assertRaises(tls.TinyTLSHandshakeError):
                client_conn = tls.TinyTLSConnection(s2)
                # client expects different RSA key -> should fail
                client_conn.handshake_client(other_n, other_e)
        finally:
            s1.close()
            s2.close()
            t.join(timeout=10)


class TestHelpers(unittest.TestCase):
    """Test module-level helper functions."""

    def test_hmac_deterministic(self):
        key = b"test key"
        data = b"test data"
        h1 = tls._hmac(key, data)
        h2 = tls._hmac(key, data)
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), tls.HMAC_SIZE)

    def test_hmac_different_inputs(self):
        key = b"test key"
        h1 = tls._hmac(key, b"data A")
        h2 = tls._hmac(key, b"data B")
        self.assertNotEqual(h1, h2)

    def test_dh_sign_payload(self):
        payload = tls._dh_sign_payload(1, 0xABCD, b"\x01" * 32, b"\x02" * 32)
        self.assertIsInstance(payload, bytes)
        self.assertIn(b"1:", payload)
        self.assertIn(b"0xabcd:", payload)


if __name__ == "__main__":
    unittest.main()
