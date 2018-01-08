"""
usage: <mode> [<options>]
modes:
  genkey  < primes.txt  # will generate the key.priv and key.pub files
  encrypt key.pub  < file > encfile
  decrypt key.priv < encfile > file
"""

import sys
import struct
import random

PUBKEY_FILE = "key.pub"
PRIVKEY_FILE = "key.priv"
INT_SIZE = 8
PACK_SYM = {
    1: "B",
    2: "H",
    4: "I",
    8: "Q",
}


def _egcd(b, n):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0


def _modinv(b, n):
    g, x, _ = _egcd(b, n)
    if g == 1:
        return x % n


def genkey(primes):
    p, q = random.sample(primes, 2)
    n = p * q  # modulus
    e = 65537  # public exponent (see https://crypto.stackexchange.com/a/3113)
    d = _modinv(e, (p - 1) * (q - 1))  # private exponent
    return [e, d, n]


def encrypt(m, e, n):
    m = bytearray(m, "utf-8")
    r = bytearray(len(m) * INT_SIZE)
    o = 0
    for b in m:
        struct.pack_into(PACK_SYM[INT_SIZE], r, o, pow(b, e, n))
        o += INT_SIZE
    return bytes(r)


def decrypt(m, d, n):
    m = bytearray(m)
    r = bytearray(int(len(m) / INT_SIZE))
    o = 0
    while o < len(m):
        b = struct.unpack_from(PACK_SYM[INT_SIZE], m, o)[0]
        r.append(pow(b, d, n))
        o += INT_SIZE
    return bytes(r)


if len(sys.argv) < 2:
    print(__doc__.format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

if sys.argv[1] == "genkey":
    primes = []
    for line in sys.stdin:
        primes.append(int(line.strip()))

    e, d, n = genkey(primes)

    with open(PUBKEY_FILE, 'w+') as f:
        f.write(hex(n) + "\n")
        f.write(hex(e) + "\n")
    with open(PRIVKEY_FILE, 'w+') as f:
        f.write(hex(n) + "\n")
        f.write(hex(d) + "\n")

    print("done, wrote keys to {} and {}".format(PUBKEY_FILE, PRIVKEY_FILE))

elif sys.argv[1] == "encrypt":
    if len(sys.argv) < 3:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[2]) as f:
        n = int(f.readline(), 16)
        e = int(f.readline(), 16)

    sys.stdout.buffer.write(encrypt(sys.stdin.read(), e, n))

elif sys.argv[1] == "decrypt":
    if len(sys.argv) < 3:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[2]) as f:
        n = int(f.readline(), 16)
        d = int(f.readline(), 16)

    sys.stdout.buffer.write(decrypt(sys.stdin.buffer.read(), d, n))
else:
    print(__doc__.format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)
