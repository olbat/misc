"""
usage: <mode> [<options>]
modes:
  genkey  < primes.txt  # will generate the key.priv and key.pub files
  encrypt key.pub  < file > encfile
  decrypt key.priv < encfile > file
  sign    key.priv < file > sig
  verify  key.pub sig < file
"""

from math import ceil
from io import BytesIO
from random import sample
from hashlib import sha256

PUBKEY_FILE = "key.pub"
PRIVKEY_FILE = "key.priv"


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


def genkey(primes):
    """
    Generate RSA modulus and public/private exponent
    Random primes numbers are picked from the _primes_ list to simplify
    the implementation
    """
    p, q = sample(primes, 2)
    n = p * q  # modulus

    e = 65537  # public exponent (see https://crypto.stackexchange.com/a/3113)
    # calculate the exponent using Euler's totient (Φ) instead of the
    # Carmichael (λ) one (easier implementation)
    # see https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation
    d = _modinv(e, (p - 1) * (q - 1))  # private exponent

    return [e, d, n]


def encrypt(m, e, n):
    """
    Encrypt the _m_ message using the public exponent _e_ and the modulus _n_

    Note: the message is encrypted byte-per-byte using RSA instead of a
          symetric cypher. This is not secure and very inefficient but it
          allows to simplify the implementation as well as encrypting messages
          bigger than the modulus.
          (see https://security.stackexchange.com/questions/33445)
    """
    m = bytearray(m, "utf-8")  # assume that the message is UTF-8 encoded
    s = _bytesize(n)
    r = BytesIO()  # size = len(m) * s

    # handle message byte-per-byte: very spece-inefficient, time consuming
    # and insecure but easy to implement (no need for a symetric cypher, allows
    # to work with small primes/modulus) and there is no need for padding
    for b in m:
        v = pow(b, e, n)
        r.write(v.to_bytes(s, byteorder='little', signed=False))

    return r.getvalue()


def decrypt(m, d, n):
    """
    Decrypt the _m_ message using the private exponent _d_ and the modulus _n_
    """
    s = _bytesize(n)
    if (len(m) % s) != 0:
        raise ValueError
    r = BytesIO()
    m = BytesIO(m)

    for b in iter(lambda: m.read(s), b""):
        v = int.from_bytes(b, byteorder='little', signed=False)
        b = pow(v, d, n)
        r.write(b.to_bytes(1, byteorder='little'))

    return r.getvalue().decode("utf-8")


def sign(m, d, n):
    """
    Returns the signature of the the _m_ message using the private exponent _d_
    and the modulus _n_
    """
    m = bytes(m, 'utf-8')  # assume that the message is UTF-8 encoded

    # encrypt a string version of the digest since encrypt needs an UTF-8 str
    # and since it allows to work with a modulus smaller than the digest (= to
    # work with small primes).
    # (see https://en.wikipedia.org/wiki/Digital_signature#How_they_work)
    h = sha256(m).hexdigest()

    return encrypt(h, d, n)


def verify(m, s, e, n):
    """
    Verify the signature _s_ of the message _m_ using the public exponent _d_
    and the modulus _n_
    """
    m = bytes(m, 'utf-8')  # assume that the message is UTF-8 encoded
    return sha256(m).hexdigest() == decrypt(s, e, n)


# main program
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "genkey":
        primes = []
        for line in sys.stdin:
            primes.append(int(line.strip()))

        e, d, n = genkey(primes)

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

        sys.stdout.buffer.write(encrypt(sys.stdin.read(), e, n))

    elif sys.argv[1] == "decrypt":
        if len(sys.argv) < 3:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2]) as f:
            n, d = loadkey(f.read())

        sys.stdout.write(decrypt(sys.stdin.buffer.read(), d, n))

    elif sys.argv[1] == "sign":
        if len(sys.argv) < 3:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2]) as f:
            n, d = loadkey(f.read())

        sys.stdout.buffer.write(sign(sys.stdin.read(), d, n))

    elif sys.argv[1] == "verify":
        if len(sys.argv) < 4:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2]) as f:
            n, e = loadkey(f.read())
        with open(sys.argv[3], 'rb') as f:
            s = f.read()

        if verify(sys.stdin.read(), s, e, n):
            print("signature ok")
            sys.exit(0)
        else:
            print("bad signature !")
            sys.exit(1)

    else:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
