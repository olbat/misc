import unittest
from io import BytesIO
from collections import namedtuple
import codecs
import aes


class TestAES(unittest.TestCase):
    # test vectors from https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values
    TestVector = namedtuple('TestVector',
                            ['moo', 'key', 'iv', 'text', 'cipher'])
    TEST_VECTORS = (
        # AES128-ECB
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '2B7E1516' '28AED2A6' 'ABF71588' '09CF4F3C',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '6BC1BEE2' '2E409F96' 'E93D7E11' '7393172A'
                'AE2D8A57' '1E03AC9C' '9EB76FAC' '45AF8E51'
                '30C81C46' 'A35CE411' 'E5FBC119' '1A0A52EF'
                'F69F2445' 'DF4F9B17' 'AD2B417B' 'E66C3710',
                'hex',
            ),
            cipher=codecs.decode(
                '3AD77BB4' '0D7A3660' 'A89ECAF3' '2466EF97'
                'F5D3D585' '03B9699D' 'E785895A' '96FDBAAF'
                '43B1CD7F' '598ECE23' '881B00E3' 'ED030688'
                '7B0C785E' '27E8AD3F' '82232071' '04725DD4'
                'A254BE88E037DDD9D79FB6411C3F9DF8',  # padding
                'hex',
            ),
        ),
        # AES192-ECB
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '8E73B0F7' 'DA0E6452' 'C810F32B' '809079E5'
                '62F8EAD2' '522C6B7B',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '6BC1BEE2' '2E409F96' 'E93D7E11' '7393172A'
                'AE2D8A57' '1E03AC9C' '9EB76FAC' '45AF8E51'
                '30C81C46' 'A35CE411' 'E5FBC119' '1A0A52EF'
                'F69F2445' 'DF4F9B17' 'AD2B417B' 'E66C3710',
                'hex',
            ),
            cipher=codecs.decode(
                'BD334F1D' '6E45F25F' 'F712A214' '571FA5CC'
                '97410484' '6D0AD3AD' '7734ECB3' 'ECEE4EEF'
                'EF7AFD22' '70E2E60A' 'DCE0BA2F' 'ACE6444E'
                '9A4B41BA' '738D6C72' 'FB166916' '03C18E0E'
                'DAA0AF074BD8083C8A32D4FC563C55CC',  # padding
                'hex',
            ),
        ),
        # AES256-ECB
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '603DEB10' '15CA71BE' '2B73AEF0' '857D7781'
                '1F352C07' '3B6108D7' '2D9810A3' '0914DFF4',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '6BC1BEE2' '2E409F96' 'E93D7E11' '7393172A'
                'AE2D8A57' '1E03AC9C' '9EB76FAC' '45AF8E51'
                '30C81C46' 'A35CE411' 'E5FBC119' '1A0A52EF'
                'F69F2445' 'DF4F9B17' 'AD2B417B' 'E66C3710',
                'hex',
            ),
            cipher=codecs.decode(
                'F3EED1BD' 'B5D2A03C' '064B5A7E' '3DB181F8'
                '591CCB10' 'D410ED26' 'DC5BA74A' '31362870'
                'B6ED21B9' '9CA6F4F9' 'F153E7B1' 'BEAFED1D'
                '23304B7A' '39F9F3FF' '067D8D8F' '9E24ECC7'
                '4C45DFB3B3B484EC35B0512DC8C1C4D6',  # padding
                'hex',
            ),
        ),
        # AES128-CBC
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                '2B7E1516' '28AED2A6' 'ABF71588' '09CF4F3C',
                'hex',
            ),
            iv=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F',
                'hex',
            ),
            text=codecs.decode(
                '6BC1BEE2' '2E409F96' 'E93D7E11' '7393172A'
                'AE2D8A57' '1E03AC9C' '9EB76FAC' '45AF8E51'
                '30C81C46' 'A35CE411' 'E5FBC119' '1A0A52EF'
                'F69F2445' 'DF4F9B17' 'AD2B417B' 'E66C3710',
                'hex',
            ),
            cipher=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F'
                '7649ABAC' '8119B246' 'CEE98E9B' '12E9197D'
                '5086CB9B' '507219EE' '95DB113A' '917678B2'
                '73BED6B8' 'E3C1743B' '7116E69E' '22229516'
                '3FF1CAA1' '681FAC09' '120ECA30' '7586E1A7'
                'A254BE88E037DDD9D79FB6411C3F9DF8',  # padding block
                'hex',
            ),
        ),
        # AES192-CBC
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                '8E73B0F7' 'DA0E6452' 'C810F32B' '809079E5'
                '62F8EAD2' '522C6B7B',
                'hex',
            ),
            iv=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F',
                'hex',
            ),
            text=codecs.decode(
                '6BC1BEE2' '2E409F96' 'E93D7E11' '7393172A'
                'AE2D8A57' '1E03AC9C' '9EB76FAC' '45AF8E51'
                '30C81C46' 'A35CE411' 'E5FBC119' '1A0A52EF'
                'F69F2445' 'DF4F9B17' 'AD2B417B' 'E66C3710',
                'hex',
            ),
            cipher=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F'
                '4F021DB2' '43BC633D' '7178183A' '9FA071E8'
                'B4D9ADA9' 'AD7DEDF4' 'E5E73876' '3F69145A'
                '571B2420' '12FB7AE0' '7FA9BAAC' '3DF102E0'
                '08B0E279' '88598881' 'D920A9E6' '4F5615CD'
                'DAA0AF074BD8083C8A32D4FC563C55CC',  # padding
                'hex',
            ),
        ),
        # AES256-CBC
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                '603DEB10' '15CA71BE' '2B73AEF0' '857D7781'
                '1F352C07' '3B6108D7' '2D9810A3' '0914DFF4',
                'hex',
            ),
            iv=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F',
                'hex',
            ),
            text=codecs.decode(
                '6BC1BEE2' '2E409F96' 'E93D7E11' '7393172A'
                'AE2D8A57' '1E03AC9C' '9EB76FAC' '45AF8E51'
                '30C81C46' 'A35CE411' 'E5FBC119' '1A0A52EF'
                'F69F2445' 'DF4F9B17' 'AD2B417B' 'E66C3710',
                'hex',
            ),
            cipher=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F'
                'F58C4C04' 'D6E5F1BA' '779EABFB' '5F7BFBD6'
                '9CFC4E96' '7EDB808D' '679F777B' 'C6702C7D'
                '39F23369' 'A9D9BACF' 'A530E263' '04231461'
                'B2EB05E2' 'C39BE9FC' 'DA6C1907' '8C6A9D1B'
                '4C45DFB3B3B484EC35B0512DC8C1C4D6',  # padding
                'hex',
            ),
        ),
     )

    def test_encrypt(self):
        iio = BytesIO()
        oio = BytesIO()
        for tv in self.__class__.TEST_VECTORS:
            iio.truncate(0)
            iio.seek(0)
            oio.truncate(0)
            oio.seek(0)

            iio.write(tv.text)
            iio.seek(0)
            aes.encrypt(iio, oio, tv.key, tv.moo, tv.iv)
            oio.seek(0)

            self.assertEqual(tv.cipher.hex(), oio.read().hex())

    def test_decrypt(self):
        iio = BytesIO()
        oio = BytesIO()
        for tv in self.__class__.TEST_VECTORS:
            iio.truncate(0)
            iio.seek(0)
            oio.truncate(0)
            oio.seek(0)

            iio.write(tv.cipher)
            iio.seek(0)
            aes.decrypt(iio, oio, tv.key, tv.moo)
            oio.seek(0)

            self.assertEqual(tv.text.hex(), oio.read().hex())

    def test_encrypt_decrypt(self):
        iio = BytesIO()
        oio = BytesIO()
        for tv in self.__class__.TEST_VECTORS:
            iio.truncate(0)
            iio.seek(0)
            oio.truncate(0)
            oio.seek(0)

            iio.write(tv.text)
            iio.seek(0)
            aes.encrypt(iio, oio, tv.key, tv.moo, tv.iv)

            iio.truncate(0)
            iio.seek(0)
            oio.seek(0)
            aes.decrypt(oio, iio, tv.key, tv.moo)
            iio.seek(0)

            self.assertEqual(tv.text.hex(), iio.read().hex())


if __name__ == '__main__':
    unittest.main()
