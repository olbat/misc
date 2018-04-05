"""
usage: {0} KEY_FILE [HASH_TYPE] < FILE
"""
# see https://en.wikipedia.org/wiki/HMAC
#     http://www.ietf.org/rfc/rfc2104.txt
#     https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.198-1.pdf

from io import BytesIO
import sha2

DEFAULT_DIGEST = sha2.SHA512_256


def prepare_key(key, digestcls=DEFAULT_DIGEST):
    """
    Generates a key of a specified size using the input key

    (see RFC 2104 section 2, FIPS-198-1 section 4)
    """
    if len(key) > digestcls.block_size():
        io = BytesIO()
        io.write(key)
        io.seek(0)
        key = digestcls.digest(io)

    if len(key) < digestcls.block_size():
        key += bytes(0x00 for _ in range(digestcls.block_size() - len(key)))

    return key


def digest(readable, key, digestcls=DEFAULT_DIGEST):
    """
    Generates the HMAC of the message from _readable_ using _key_

    (see RFC 2104 section 2, FIPS-198-1 section 4
    """
    # FIXME: process using an IO instead of a message
    key = prepare_key(key, digestcls=digestcls)
    assert(len(key) == digestcls.block_size())

    kipad = bytes((b ^ 0x36) for b in key)
    kopad = bytes((b ^ 0x5c) for b in key)

    # 1st pass
    def read(size, *args, **kwargs):  # allows to prepend kipad to the stream
        read.pos += size
        if read.pos <= len(kipad):
            return kipad[read.pos-size:read.pos]
        elif ((read.pos - size) < len(kipad)) and (read.pos > len(kipad)):
            raise ValueError  # reading overlapping data
        else:
            return readable.read(size, *args, **kwargs)
    read.pos = 0
    obj = type('', (object,), {"read": read})  # create an anon readable object
    d = digestcls.digest(obj)

    # 2nd pass
    io = BytesIO()
    io.write(kopad)
    io.write(d)
    io.seek(0)

    return digestcls.digest(io)


# main program
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'rb') as f:
        k = f.read()

    if len(sys.argv) >= 3:
        digestcls = getattr(sha2, sys.argv[2])
    else:
        digestcls = DEFAULT_DIGEST

    print(digest(sys.stdin.buffer, k, digestcls=digestcls).hex())
