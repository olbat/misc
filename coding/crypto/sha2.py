"""
usage: {0} < FILE
"""
# see https://en.wikipedia.org/wiki/SHA-2
#     http://nvlpubs.nist.gov/nistpubs/fips/nist.fips.180-4.pdf


class SHA256():
    H = (
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    )
    K = (
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1,
        0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786,
        0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147,
        0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b,
        0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a,
        0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    )
    ROUNDS = 64
    CHUNK_SIZE = 64
    WSIZE = 32
    MOD = pow(2, WSIZE)

    @classmethod
    def _shr(cls, x, n):
        '''
        see FIPS 180-4 section 3.2
        '''
        return (x >> n)

    @classmethod
    def _rotr(cls, x, n):
        '''
        see FIPS 180-4 section 3.2
        '''
        return (x >> n) | ((x << (cls.WSIZE - n)) & (cls.MOD - 1))

    @classmethod
    def _sigma0(cls, x):
        '''
        see FIPS 180-4 section 4.
        '''
        return cls._rotr(x, 7) ^ cls._rotr(x, 18) ^ cls._shr(x, 3)

    @classmethod
    def _sigma1(cls, x):
        '''
        see FIPS 180-4 section 4.
        '''
        return cls._rotr(x, 17) ^ cls._rotr(x, 19) ^ cls._shr(x, 10)

    @classmethod
    def _bigsigma0(cls, x):
        '''
        see FIPS 180-4 section 4.
        '''
        return cls._rotr(x, 2) ^ cls._rotr(x, 13) ^ cls._rotr(x, 22)

    @classmethod
    def _bigsigma1(cls, x):
        '''
        see FIPS 180-4 section 4.
        '''
        return cls._rotr(x, 6) ^ cls._rotr(x, 11) ^ cls._rotr(x, 25)

    @staticmethod
    def _ch(x, y, z):
        '''
        see FIPS 180-4 section 4.
        '''
        return (x & y) ^ (~x & z)

    @staticmethod
    def _maj(x, y, z):
        '''
        see FIPS 180-4 section 4.
        '''
        return (x & y) ^ (x & z) ^ (y & z)

    @classmethod
    def _pad(cls, s):
        '''
        see FIPS 180-4 section 5.
        '''
        return bytes([1 << 7]) \
            + bytes([0 for _ in range((55 - s) % cls.CHUNK_SIZE)]) \
            + int.to_bytes(s * 8, 8, 'big', signed=False)

    @classmethod
    def _chunk_digest(cls, chunk, H):
        m = cls.WSIZE // 8
        w = [0 for _ in range(cls.ROUNDS)]

        for i in range(cls.ROUNDS):
            if i < 16:
                w[i] = int.from_bytes(
                    chunk[i*m:(i+1)*m], byteorder='big', signed=False)
            else:
                w[i] = (cls._sigma1(w[i-2]) + w[i-7]
                        + cls._sigma0(w[i-15]) + w[i-16]) % cls.MOD

        a, b, c, d, e, f, g, h = H

        for i in range(cls.ROUNDS):
            t1 = (
              h + cls._bigsigma1(e) + cls._ch(e, f, g) + cls.K[i] + w[i]
            ) % cls.MOD
            t2 = (cls._bigsigma0(a) + cls._maj(a, b, c)) % cls.MOD
            h = g
            g = f
            f = e
            e = (d + t1) % cls.MOD
            d = c
            c = b
            b = a
            a = (t1 + t2) % cls.MOD

        H[0] = (a + H[0]) % cls.MOD
        H[1] = (b + H[1]) % cls.MOD
        H[2] = (c + H[2]) % cls.MOD
        H[3] = (d + H[3]) % cls.MOD
        H[4] = (e + H[4]) % cls.MOD
        H[5] = (f + H[5]) % cls.MOD
        H[6] = (g + H[6]) % cls.MOD
        H[7] = (h + H[7]) % cls.MOD

        return H

    @classmethod
    def digest(cls, iio):
        count = 0
        chunk = None
        H = list(cls.H)

        for chunk in iter(lambda: iio.read(cls.CHUNK_SIZE), b""):
            count += len(chunk)
            if len(chunk) < cls.CHUNK_SIZE:  # incomplete block, stop & padding
                break
            H = cls._chunk_digest(chunk, H)

        # last block: padding
        if (count % cls.CHUNK_SIZE) == 0:
            chunk = cls._pad(count)
        else:
            chunk += cls._pad(count)
        H = cls._chunk_digest(chunk, H)

        # convert array of numbers to bytes
        hg = (int.to_bytes(b, cls.WSIZE // 8, 'big', signed=False) for b in H)
        return b"".join(hg)


# main program
if __name__ == "__main__":
    import sys
    sys.stdout.write(SHA256.digest(sys.stdin.buffer).hex() + '\n')
