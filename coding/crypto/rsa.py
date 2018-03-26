"""
usage: {0} <mode> [<options>]

modes:
  genkeys < PRIMES  # takes two primes as input (one per line)
  encrypt PUBKEY_FILE  < FILE > ENC_FILE
  decrypt PRIVKEY_FILE < ENC_FILE > FILE
  sign    PRIVKEY_FILE < FILE > SIG_FILE
  verify  PUBKEY_FILE SIG_FILE < FILE

examples:
  # generate the RSA key pair (the key.priv and key.pub files)
  {{ openssl prime --generate --bits 1024 \\
  & openssl prime --generate --bits 1024; }} | python {0} genkeys

  # encrypt a file
  python {0} encrypt key.pub < file.txt > file.txt.enc

  # decrypt a file
  python {0} decrypt key.priv < file.txt.enc

  # sign a file
  python {0} sign key.priv < file.txt > file.txt.sig

  # verify a signature
  python {0} verify key.pub file.sig < file.txt.sig

note: the encryption algorithm is using AES and the signature one SHA-2
"""
# see https://en.wikipedia.org/wiki/RSA_(cryptosystem)
#     https://www.emc.com/collateral/white-papers/h11300-pkcs-1v2-2-rsa-cryptography-standard-wp.pdf

from math import ceil
from io import BytesIO

PUBKEY_FILE = "key.pub"
PRIVKEY_FILE = "key.priv"
AES_KEY_SIZE = 256
SHA2_DIGEST = "SHA512_256"
BUF_SIZE = 4096


def _egcd(b, n):
    """
    Returns the Euler's totient (Φ)

    see https://en.wikipedia.org/wiki/Euler%27s_totient_function,
        https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
    """
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0


def _modinv(b, n):
    """
    Returns the modular multiplicative inverse

    see https://en.wikipedia.org/wiki/Modular_multiplicative_inverse
        https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
    """
    g, x, _ = _egcd(b, n)
    if g == 1:
        return x % n


def _bytesize(n):
    """
    Get the size (in bytes) necessary to store numbers that are smaller than
    the modulus (n)
    """
    return ceil(n.bit_length() / 8)


def dumpkey(n, x):
    """
    Dumps an RSA public/private key (modulus _n_ and exponent _x_) as a string
    """
    return "{} {}".format(hex(n), hex(x))


def loadkey(s):
    """
    Loads RSA public/private key modulus and exponent from a string
    """
    return [int(v, 16) for v in s.split()]


def genkeys(p, q):
    """
    Generate RSA modulus and public/private exponent
    """
    if p == q:
        raise ValueError

    n = p * q  # modulus

    e = 65537  # public exponent (see https://crypto.stackexchange.com/a/3113)
    # calculate the exponent using Euler's totient (Φ) instead of the
    # Carmichael (λ) one (easier implementation)
    # see https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation
    d = _modinv(e, (p - 1) * (q - 1))  # private exponent

    return [e, d, n]


def encrypt(iio, oio, e, n):
    """
    Encrypt message from _iio_ to _oio_ using the public exponent_e_,
    the modulus _n_ and the AES algorithm
    """
    import aes
    s = _bytesize(n)
    # the RSA modulus is too small to encrypt the AES key
    if s < (AES_KEY_SIZE // 8):
        raise ValueError

    # generate the key for the AES algorithm
    k = aes.genkey(AES_KEY_SIZE)

    # encrypt and save it using the RSA algorithm
    b = int.from_bytes(k, byteorder='little', signed=False)
    v = pow(b, e, n)
    oio.write(v.to_bytes(s, byteorder='little', signed=False))

    # encrypt the message from the input IO using AES
    aes.encrypt(iio, oio, k)


def decrypt(iio, oio, d, n):
    """
    Decrypt message from _iio_ to _oio_ using the private exponent _d_,
    the modulus _n_ and the AES algorithm
    """
    import aes
    s = _bytesize(n)

    # read and decrypt the AES key using the RSA algorithm
    v = int.from_bytes(iio.read(s), byteorder='little', signed=False)
    b = pow(v, d, n)
    k = b.to_bytes(AES_KEY_SIZE // 8, byteorder='little')

    # decrypt the message from the input IO using AES
    aes.decrypt(iio, oio, k)


def sign(iio, oio, d, n):
    """
    Returns the signature of the message from _iio_ to _oio_ using the private
    exponent _d_, the modulus _n_ and the SHA-2 algorithm

    (see https://en.wikipedia.org/wiki/Digital_signature#How_they_work)
    """
    import sha2

    hc = getattr(sha2, SHA2_DIGEST)
    hio = BytesIO()
    hio.write(hc.digest(iio))
    hio.seek(0)

    return encrypt(hio, oio, d, n)


def verify(iio, s, e, n):
    """
    Verify the signature _s_ of the message from _iio_ using the public
    exponent _d_, the modulus _n_ and the SHA-2 algorithm

    (see https://en.wikipedia.org/wiki/Digital_signature#How_they_work)
    """
    import sha2

    # compute the expected hash
    hc = getattr(sha2, SHA2_DIGEST)
    exph = BytesIO()
    exph.write(hc.digest(iio))
    exph.seek(0)
    exph = exph.read()

    # extract (decrypt) the hash from the signature
    sigio = BytesIO()
    sigio.write(s)
    sigio.seek(0)
    sigh = BytesIO()
    decrypt(sigio, sigh, e, n)
    sigh.seek(0)
    sigh = sigh.read()

    return exph == sigh


def encrypt_standalone(iio, oio, e, n):
    """
    Encrypt message from _iio_ to _oio_ using the public exponent _e_
    and the modulus _n_

    Note: the message is encrypted byte-per-byte using RSA instead of a
          symetric cypher. This is not secure and very inefficient but it
          allows to simplify the implementation as well as encrypting messages
          bigger than the modulus.
          (see https://security.stackexchange.com/questions/33445)
    """
    s = _bytesize(n)

    # handle message byte-per-byte: very spece-inefficient, time consuming
    # and insecure but easy to implement (no need for a symetric cypher, allows
    # to work with small primes/modulus) and there is no need for padding
    for b in iter(lambda: iio.read(1), b""):
        b = int.from_bytes(b, byteorder='little', signed=False)
        v = pow(b, e, n)
        oio.write(v.to_bytes(s, byteorder='little', signed=False))


def decrypt_standalone(iio, oio, d, n):
    """
    Decrypt message from _iio_ to _oio_ using the private exponent _d_ and the
    modulus _n_

    Note: the message is decrypted byte-per-byte using RSA instead of a
          symetric cypher. This is not secure and very inefficient but it
          allows to simplify the implementation as well as encrypting messages
          bigger than the modulus.
          (see https://security.stackexchange.com/questions/33445)
    """
    s = _bytesize(n)

    # handle message byte-per-byte: very spece-inefficient, time consuming
    # and insecure but easy to implement (no need for a symetric cypher, allows
    # to work with small primes/modulus) and there is no need for padding
    for b in iter(lambda: iio.read(s), b""):
        v = int.from_bytes(b, byteorder='little', signed=False)
        b = pow(v, d, n)
        oio.write(b.to_bytes(1, byteorder='little'))


def sign_standalone(iio, oio, d, n):
    """
    Returns the signature of the message from _iio_ to _oio_ using the private
    exponent _d_, the modulus _n_ and the SHA-2 algorithm

    (see https://en.wikipedia.org/wiki/Digital_signature#How_they_work)
    """
    import hashlib

    hf = getattr(hashlib, SHA2_DIGEST.lower().split("_", 2)[0])
    h = hf()
    for bs in iter(lambda: iio.read(BUF_SIZE), b""):
        h.update(bs)

    hio = BytesIO()
    hio.write(h.digest())
    hio.seek(0)

    return encrypt(hio, oio, d, n)


def verify_standalone(iio, s, e, n):
    """
    Verify the signature _s_ of the message from _iio_ using the public
    exponent _d_, the modulus _n_ and the SHA-2 algorithm

    (see https://en.wikipedia.org/wiki/Digital_signature#How_they_work)
    """
    import hashlib

    # compute the expected hash
    hf = getattr(hashlib, SHA2_DIGEST.lower().split("_", 2)[0])
    exph = hf()
    for bs in iter(lambda: iio.read(BUF_SIZE), b""):
        exph.update(bs)
    exph = exph.digest()

    # extract (decrypt) the hash from the signature
    sigio = BytesIO()
    sigio.write(s)
    sigio.seek(0)
    sigh = BytesIO()
    decrypt(sigio, sigh, e, n)
    sigh.seek(0)
    sigh = sigh.read()

    return exph == sigh


# main program
if __name__ == "__main__":
    import sys
    import importlib.util

    if len(sys.argv) < 2:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "genkeys":
        p = int(sys.stdin.readline())
        q = int(sys.stdin.readline())

        e, d, n = genkeys(p, q)

        with open(PUBKEY_FILE, 'w+') as f:
            f.write(dumpkey(n, e))
        with open(PRIVKEY_FILE, 'w+') as f:
            f.write(dumpkey(n, d))

        print("wrote keys to {} and {}".format(PUBKEY_FILE, PRIVKEY_FILE))

    elif sys.argv[1] == "encrypt":
        if len(sys.argv) < 3:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2]) as f:
            n, e = loadkey(f.read())

        if importlib.util.find_spec("aes"):
            encrypt(sys.stdin.buffer, sys.stdout.buffer, e, n)
        else:
            print("WARNING: no AES implementation available, using RSA",
                  file=sys.stderr)
            encrypt_standalone(sys.stdin.buffer, sys.stdout.buffer, e, n)

    elif sys.argv[1] == "decrypt":
        if len(sys.argv) < 3:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2]) as f:
            n, d = loadkey(f.read())

        if importlib.util.find_spec("aes"):
            decrypt(sys.stdin.buffer, sys.stdout.buffer, d, n)
        else:
            print("WARNING: no AES implementation available, using RSA",
                  file=sys.stderr)
            decrypt_standalone(sys.stdin.buffer, sys.stdout.buffer, d, n)

    elif sys.argv[1] == "sign":
        if len(sys.argv) < 3:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2]) as f:
            n, d = loadkey(f.read())

        if importlib.util.find_spec("sha2"):
            sign(sys.stdin.buffer, sys.stdout.buffer, d, n)
        else:
            sign_standalone(sys.stdin.buffer, sys.stdout.buffer, d, n)

    elif sys.argv[1] == "verify":
        if len(sys.argv) < 4:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2]) as f:
            n, e = loadkey(f.read())
        with open(sys.argv[3], 'rb') as f:
            s = f.read()

        if importlib.util.find_spec("sha2"):
            signok = verify(sys.stdin.buffer, s, e, n)
        else:
            signok = verify_standalone(sys.stdin.buffer, s, e, n)

        if signok:
            print("signature ok")
            sys.exit(0)
        else:
            print("bad signature !")
            sys.exit(1)

    else:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
