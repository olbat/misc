"""
usage: {0} TYPE < FILE

types: 224, 256, 384, 512
"""
# see https://en.wikipedia.org/wiki/SHA-2
#     http://nvlpubs.nist.gov/nistpubs/fips/nist.fips.180-4.pdf


class SHA256():
    '''
    see FIPS 180-4 section 6.2
    '''
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
        if cls.CHUNK_SIZE == 64:
            mz = 55
            sz = 8
        else:
            mz = 111
            sz = 16

        return bytes([1 << 7]) \
            + bytes([0 for _ in range((mz - s) % cls.CHUNK_SIZE)]) \
            + int.to_bytes(s * 8, sz, 'big', signed=False)

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


class SHA224(SHA256):
    '''
    see FIPS 180-4 section 6.3
    '''
    H = (
        0xc1059ed8, 0x367cd507, 0x3070dd17, 0xf70e5939,
        0xffc00b31, 0x68581511, 0x64f98fa7, 0xbefa4fa4
    )

    @classmethod
    def digest(cls, *args):
        return super().digest(*args)[0:224//8]


class SHA512(SHA256):
    '''
    see FIPS 180-4 section 6.4
    '''
    H = (
        0x6a09e667f3bcc908, 0xbb67ae8584caa73b, 0x3c6ef372fe94f82b,
        0xa54ff53a5f1d36f1, 0x510e527fade682d1, 0x9b05688c2b3e6c1f,
        0x1f83d9abfb41bd6b, 0x5be0cd19137e2179
    )
    K = (
        0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f,
        0xe9b5dba58189dbbc, 0x3956c25bf348b538, 0x59f111f1b605d019,
        0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242,
        0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
        0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235,
        0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3,
        0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 0x2de92c6f592b0275,
        0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
        0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f,
        0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
        0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc,
        0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
        0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6,
        0x92722c851482353b, 0xa2bfe8a14cf10364, 0xa81a664bbc423001,
        0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218,
        0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
        0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99,
        0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb,
        0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc,
        0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
        0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915,
        0xc67178f2e372532b, 0xca273eceea26619c, 0xd186b8c721c0c207,
        0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba,
        0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
        0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc,
        0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a,
        0x5fcb6fab3ad6faec, 0x6c44198c4a475817
    )
    ROUNDS = 80
    CHUNK_SIZE = 128
    WSIZE = 64
    MOD = pow(2, WSIZE)

    @classmethod
    def _sigma0(cls, x):
        '''
        see FIPS 180-4 section 4.
        '''
        return cls._rotr(x, 1) ^ cls._rotr(x, 8) ^ cls._shr(x, 7)

    @classmethod
    def _sigma1(cls, x):
        '''
        see FIPS 180-4 section 4.
        '''
        return cls._rotr(x, 19) ^ cls._rotr(x, 61) ^ cls._shr(x, 6)

    @classmethod
    def _bigsigma0(cls, x):
        '''
        see FIPS 180-4 section 4.
        '''
        return cls._rotr(x, 28) ^ cls._rotr(x, 34) ^ cls._rotr(x, 39)

    @classmethod
    def _bigsigma1(cls, x):
        '''
        see FIPS 180-4 section 4.
        '''
        return cls._rotr(x, 14) ^ cls._rotr(x, 18) ^ cls._rotr(x, 41)


class SHA384(SHA512):
    '''
    see FIPS 180-4 section 6.5
    '''
    H = (
        0xcbbb9d5dc1059ed8, 0x629a292a367cd507, 0x9159015a3070dd17,
        0x152fecd8f70e5939, 0x67332667ffc00b31, 0x8eb44a8768581511,
        0xdb0c2e0d64f98fa7, 0x47b5481dbefa4fa4
    )

    @classmethod
    def digest(cls, *args):
        return super().digest(*args)[0:384//8]


# main program
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    cls = globals()["SHA{}".format(sys.argv[1])]
    sys.stdout.write(cls.digest(sys.stdin.buffer).hex() + '\n')
