import unittest
from io import BytesIO

import rsa


def _gen_test_rsa_keys():
    """
    Generate RSA keys for testing using a probabilistic primality test
    (Miller-Rabin), avoiding external dependencies.
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

    p = gen_prime(512)
    q = gen_prime(512)
    while p == q:
        q = gen_prime(512)
    e, d, n = rsa.genkeys(p, q)
    return e, d, n, p, q


# Generate keys once for all tests (1024-bit modulus)
_E, _D, _N, _P, _Q = _gen_test_rsa_keys()


class TestHelpers(unittest.TestCase):
    """Test module-level helper functions.

    No NIST test vectors exist for textbook RSA without padding; these tests
    verify the helper arithmetic directly.
    """

    def test_bytesize(self):
        self.assertEqual(rsa._bytesize(255), 1)
        self.assertEqual(rsa._bytesize(256), 2)
        self.assertEqual(rsa._bytesize(65535), 2)
        self.assertEqual(rsa._bytesize(65536), 3)
        self.assertEqual(rsa._bytesize(2 ** 256 - 1), 32)
        self.assertEqual(rsa._bytesize(2 ** 256), 33)

    def test_modinv(self):
        # 3 * 7 = 21 ≡ 1 (mod 10)
        self.assertEqual(rsa._modinv(3, 10), 7)
        # verify private exponent: e * d ≡ 1 (mod φ(n))
        phi = (_P - 1) * (_Q - 1)
        self.assertEqual((rsa.RSA_STANDARD_PUBLIC_EXPONENT * _D) % phi, 1)

    def test_dumpkey_loadkey(self):
        for x in (_E, _D):
            s = rsa.dumpkey(_N, x)
            n, v = rsa.loadkey(s)
            self.assertEqual(n, _N)
            self.assertEqual(v, x)


class TestKeyGeneration(unittest.TestCase):
    """Test RSA key generation."""

    def test_modulus(self):
        self.assertEqual(_N, _P * _Q)

    def test_public_exponent(self):
        self.assertEqual(_E, rsa.RSA_STANDARD_PUBLIC_EXPONENT)

    def test_key_relationship(self):
        # e * d ≡ 1 (mod φ(n))
        phi = (_P - 1) * (_Q - 1)
        self.assertEqual((_E * _D) % phi, 1)

    def test_equal_primes_rejected(self):
        with self.assertRaises(ValueError):
            rsa.genkeys(65537, 65537)


class TestStandaloneEncrypt(unittest.TestCase):
    """Test byte-by-byte RSA encryption (encrypt_standalone / decrypt_standalone).

    No NIST test vectors exist for textbook RSA without padding.
    """

    def test_roundtrip(self):
        plaintext = b"Hello"
        iio = BytesIO(plaintext)
        oio = BytesIO()
        rsa.encrypt_standalone(iio, oio, _E, _N)

        oio.seek(0)
        dec = BytesIO()
        rsa.decrypt_standalone(oio, dec, _D, _N)
        dec.seek(0)
        self.assertEqual(dec.read(), plaintext)

    def test_roundtrip_empty(self):
        iio = BytesIO(b"")
        oio = BytesIO()
        rsa.encrypt_standalone(iio, oio, _E, _N)

        oio.seek(0)
        dec = BytesIO()
        rsa.decrypt_standalone(oio, dec, _D, _N)
        dec.seek(0)
        self.assertEqual(dec.read(), b"")

    def test_roundtrip_all_bytes(self):
        plaintext = bytes(range(256))
        iio = BytesIO(plaintext)
        oio = BytesIO()
        rsa.encrypt_standalone(iio, oio, _E, _N)

        oio.seek(0)
        dec = BytesIO()
        rsa.decrypt_standalone(oio, dec, _D, _N)
        dec.seek(0)
        self.assertEqual(dec.read(), plaintext)

    def test_ciphertext_differs_from_plaintext(self):
        plaintext = b"\x41\x42\x43\x44"
        iio = BytesIO(plaintext)
        oio = BytesIO()
        rsa.encrypt_standalone(iio, oio, _E, _N)
        # ciphertext must not equal plaintext (would need n < 256 to collide)
        self.assertNotEqual(oio.getvalue(), plaintext)


if __name__ == '__main__':
    unittest.main()
