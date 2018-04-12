import unittest
from collections import namedtuple
from io import BytesIO
import codecs
import sha2


class TestSHA2(unittest.TestCase):
    # test vectors from https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values
    TestVector = namedtuple('TestVector', ['cls', 'text', 'digest'])
    TEST_VECTORS = (
        TestVector(
            cls=sha2.SHA224,
            text=b'abc',
            digest=codecs.decode(
                '23097D22' '3405D822' '8642A477' 'BDA255B3'
                '2AADBCE4' 'BDA0B3F7' 'E36C9DA7',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA224,
            text=b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq',
            digest=codecs.decode(
                '75388B16' '512776CC' '5DBA5DA1' 'FD890150'
                'B0C6455C' 'B4F58B19' '52522525',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA256,
            text=b'abc',
            digest=codecs.decode(
                'BA7816BF' '8F01CFEA' '414140DE' '5DAE2223'
                'B00361A3' '96177A9C' 'B410FF61' 'F20015AD',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA256,
            text=b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq',
            digest=codecs.decode(
                '248D6A61' 'D20638B8' 'E5C02693' '0C3E6039'
                'A33CE459' '64FF2167' 'F6ECEDD4' '19DB06C1',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA384,
            text=b'abc',
            digest=codecs.decode(
                'CB00753F' '45A35E8B' 'B5A03D69' '9AC65007'
                '272C32AB' '0EDED163' '1A8B605A' '43FF5BED'
                '8086072B' 'A1E7CC23' '58BAECA1' '34C825A7',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA384,
            text=(b'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmn'
                  b'hijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu'),
            digest=codecs.decode(
                '09330C33' 'F71147E8' '3D192FC7' '82CD1B47'
                '53111B17' '3B3B05D2' '2FA08086' 'E3B0F712'
                'FCC7C71A' '557E2DB9' '66C3E9FA' '91746039',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA512,
            text=b'abc',
            digest=codecs.decode(
                'DDAF35A1' '93617ABA' 'CC417349' 'AE204131'
                '12E6FA4E' '89A97EA2' '0A9EEEE6' '4B55D39A'
                '2192992A' '274FC1A8' '36BA3C23' 'A3FEEBBD'
                '454D4423' '643CE80E' '2A9AC94F' 'A54CA49F',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA512,
            text=(b'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmn'
                  b'hijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu'),
            digest=codecs.decode(
                '8E959B75' 'DAE313DA' '8CF4F728' '14FC143F'
                '8F7779C6' 'EB9F7FA1' '7299AEAD' 'B6889018'
                '501D289E' '4900F7E4' '331B99DE' 'C4B5433A'
                'C7D329EE' 'B6DD2654' '5E96E55B' '874BE909',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA512_224,
            text=b'abc',
            digest=codecs.decode(
                '4634270F' '707B6A54' 'DAAE7530' '460842E2'
                '0E37ED26' '5CEEE9A4' '3E8924AA',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA512_224,
            text=(b'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnh'
                  b'ijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu'),
            digest=codecs.decode(
                '23FEC5BB' '94D60B23' '30819264' '0B0C4533'
                '35D66473' '4FE40E72' '68674AF9',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA512_256,
            text=b'abc',
            digest=codecs.decode(
                '53048E26' '81941EF9' '9B2E29B7' '6B4C7DAB'
                'E4C2D0C6' '34FC6D46' 'E0E2F131' '07E7AF23',
                'hex',
            ),
        ),
        TestVector(
            cls=sha2.SHA512_256,
            text=(b'abcdefghbcdefghicdefghijdefghijkefghijklfghijklmghijklmnh'
                  b'ijklmnoijklmnopjklmnopqklmnopqrlmnopqrsmnopqrstnopqrstu'),
            digest=codecs.decode(
                '3928E184' 'FB8690F8' '40DA3988' '121D31BE'
                '65CB9D3E' 'F83EE614' '6FEAC861' 'E19B563A',
                'hex',
            ),
        ),
    )

    def test_digest(self):
        iio = BytesIO()
        for tv in self.__class__.TEST_VECTORS:
            iio.truncate(0)
            iio.seek(0)

            iio.write(tv.text)
            iio.seek(0)
            digest = tv.cls.digest(iio)

            self.assertEqual(tv.digest, digest, "{}{}".format(tv.cls, tv.text))


if __name__ == '__main__':
    unittest.main()
