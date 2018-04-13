import unittest
from collections import namedtuple
from io import BytesIO
import codecs
import sha2
import hmac


class TestSHA2(unittest.TestCase):
    # test vectors from https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values
    TestVector = namedtuple('TestVector', ['digestcls', 'text', 'key', 'mac'])
    TEST_VECTORS = (
        # SHA-224 based HMACs
        TestVector(
            digestcls=sha2.SHA224,
            text=b'Sample message for keylen=blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F'
                '10111213' '14151617' '18191A1B' '1C1D1E1F'
                '20212223' '24252627' '28292A2B' '2C2D2E2F'
                '30313233' '34353637' '38393A3B' '3C3D3E3F',
                'hex',
            ),
            mac=codecs.decode(
                'C7405E3A' 'E058E8CD' '30B08B41' '40248581' 'ED174CB3'
                '4E1224BC' 'C1EFC81B',
                'hex',
            ),
        ),
        TestVector(
            digestcls=sha2.SHA224,
            text=b'Sample message for keylen<blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F' '10111213'
                '14151617' '18191A1B',
                'hex',
            ),
            mac=codecs.decode(
                'E3D249A8' 'CFB67EF8' 'B7A169E9' 'A0A59971' '4A2CECBA'
                '65999A51' 'BEB8FBBE',
                'hex',
            ),
        ),
        TestVector(
            digestcls=sha2.SHA224,
            text=b'Sample message for keylen=blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F' '10111213'
                '14151617' '18191A1B' '1C1D1E1F' '20212223' '24252627'
                '28292A2B' '2C2D2E2F' '30313233' '34353637' '38393A3B'
                '3C3D3E3F' '40414243' '44454647' '48494A4B' '4C4D4E4F'
                '50515253' '54555657' '58595A5B' '5C5D5E5F' '60616263',
                'hex',
            ),
            mac=codecs.decode(
                '91C52509' 'E5AF8531' '601AE623' '0099D90B' 'EF88AAEF'
                'B961F408' '0ABC014D',
                'hex',
            ),
        ),
        # SHA-256 based HMACs
        TestVector(
            digestcls=sha2.SHA256,
            text=b'Sample message for keylen=blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F10111213' '14151617'
                '18191A1B' '1C1D1E1F' '20212223' '2425262728292A2B' '2C2D2E2F'
                '30313233' '34353637' '38393A3B' '3C3D3E3F',
                'hex',
            ),
            mac=codecs.decode(
                '8BB9A1DB' '9806F20DF7F77B82' '138C7914' 'D174D59E' '13DC4D01'
                '69C9057B' '133E1D62',
                'hex',
            ),
        ),
        TestVector(
            digestcls=sha2.SHA256,
            text=b'Sample message for keylen<blocklen',
            key=codecs.decode(
                '00010203' '0405060708090A0B' '0C0D0E0F' '10111213' '14151617'
                '18191A1B' '1C1D1E1F',
                'hex',
            ),
            mac=codecs.decode(
                'A28CF431' '30EE696A98F14A37' '678B56BC' 'FCBDD9E5' 'CF69717F'
                'ECF5480F' '0EBDF790',
                'hex',
            ),
        ),
        TestVector(
            digestcls=sha2.SHA256,
            text=b'Sample message for keylen=blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F' '10111213'
                '14151617' '18191A1B' '1C1D1E1F' '20212223' '24252627'
                '28292A2B' '2C2D2E2F' '30313233' '34353637' '38393A3B'
                '3C3D3E3F' '40414243' '44454647' '48494A4B' '4C4D4E4F'
                '50515253' '54555657' '58595A5B' '5C5D5E5F' '60616263',
                'hex',
            ),
            mac=codecs.decode(
                'BDCCB6C7' '2DDEADB5' '00AE7683' '86CB38CC' '41C63DBB'
                '0878DDB9' 'C7A38A43' '1B78378D',
                'hex',
            ),
        ),
        # SHA-384 based HMACs
        TestVector(
            digestcls=sha2.SHA384,
            text=b'Sample message for keylen=blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F' '10111213'
                '14151617' '18191A1B' '1C1D1E1F' '20212223' '24252627'
                '28292A2B' '2C2D2E2F' '30313233' '34353637' '38393A3B'
                '3C3D3E3F' '40414243' '44454647' '48494A4B' '4C4D4E4F'
                '50515253' '54555657' '58595A5B' '5C5D5E5F' '60616263'
                '64656667' '68696A6B' '6C6D6E6F' '70717273' '74757677'
                '78797A7B' '7C7D7E7F',
                'hex',
            ),
            mac=codecs.decode(
                '63C5DAA5' 'E651847C' 'A897C958' '14AB830B' 'EDEDC7D2'
                '5E83EEF9' '195CD458' '57A37F44' '8947858F' '5AF50CC2'
                'B1B730DD' 'F29671A9',
                'hex',
            ),
        ),
        TestVector(
            digestcls=sha2.SHA384,
            text=b'Sample message for keylen<blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F' '10111213'
                '1415161718191A1B' '1C1D1E1F' '20212223' '24252627' '28292A2B'
                '2C2D2E2F',
                'hex',
            ),
            mac=codecs.decode(
                '6EB242BD' 'BB582CA1' '7BEBFA48' '1B1E2321' '1464D2B7'
                'F8C20B9FF2201637' 'B93646AF' '5AE9AC31' '6E98DB45' 'D9CAE773'
                '675EEED0',
                'hex',
            ),
        ),
        TestVector(
            digestcls=sha2.SHA384,
            text=b'Sample message for keylen=blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F' '10111213'
                '14151617' '18191A1B' '1C1D1E1F' '20212223' '24252627'
                '28292A2B' '2C2D2E2F' '30313233' '34353637' '38393A3B'
                '3C3D3E3F' '40414243' '44454647' '48494A4B' '4C4D4E4F'
                '50515253' '54555657' '58595A5B' '5C5D5E5F' '60616263'
                '64656667' '68696A6B' '6C6D6E6F' '70717273' '74757677'
                '78797A7B' '7C7D7E7F' '80818283' '84858687' '88898A8B'
                '8C8D8E8F' '90919293' '94959697' '98999A9B' '9C9D9E9F'
                'A0A1A2A3' 'A4A5A6A7' 'A8A9AAAB' 'ACADAEAF' 'B0B1B2B3'
                'B4B5B6B7' 'B8B9BABB' 'BCBDBEBF' 'C0C1C2C3' 'C4C5C6C7',
                'hex',
            ),
            mac=codecs.decode(
                '5B664436' 'DF69B0CA' '22551231' 'A3F0A3D5' 'B4F97991'
                '713CFA84' 'BFF4D079' '2EFF96C2' '7DCCBBB6' 'F79B65D5'
                '48B40E85' '64CEF594',
                'hex',
            ),
        ),
        # SHA-512 based HMACs
        TestVector(
            digestcls=sha2.SHA512,
            text=b'Sample message for keylen=blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F' '10111213'
                '14151617' '18191A1B' '1C1D1E1F' '20212223' '24252627'
                '28292A2B' '2C2D2E2F' '30313233' '34353637' '38393A3B'
                '3C3D3E3F' '40414243' '44454647' '48494A4B' '4C4D4E4F'
                '50515253' '54555657' '58595A5B' '5C5D5E5F' '60616263'
                '64656667' '68696A6B' '6C6D6E6F' '70717273' '74757677'
                '78797A7B' '7C7D7E7F',
                'hex',
            ),
            mac=codecs.decode(
                'FC25E240' '658CA785' 'B7A811A8' 'D3F7B4CA' '48CFA26A'
                '8A366BF2' 'CD1F836B' '05FCB024' 'BD368530' '81811D6C'
                'EA4216EB' 'AD79DA1C' 'FCB95EA4' '586B8A0C' 'E356596A'
                '55FB1347',
                'hex',
            ),
        ),
        TestVector(
            digestcls=sha2.SHA512,
            text=b'Sample message for keylen<blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F' '10111213'
                '14151617' '18191A1B' '1C1D1E1F' '20212223' '24252627'
                '28292A2B' '2C2D2E2F' '30313233' '34353637' '38393A3B'
                '3C3D3E3F',
                'hex',
            ),
            mac=codecs.decode(
                'FD44C18B' 'DA0BB0A6' 'CE0E82B0' '31BF2818' 'F6539BD5'
                '6EC00BDC' '10A8A2D7' '30B3634D' 'E2545D63' '9B0F2CF7'
                '10D0692C' '72A1896F' '1F211C2B' '922D1A96' 'C392E07E'
                '7EA9FEDC',
                'hex',
            ),
        ),
        TestVector(
            digestcls=sha2.SHA512,
            text=b'Sample message for keylen=blocklen',
            key=codecs.decode(
                '00010203' '04050607' '08090A0B' '0C0D0E0F' '10111213'
                '14151617' '18191A1B' '1C1D1E1F' '20212223' '24252627'
                '28292A2B' '2C2D2E2F' '30313233' '34353637' '38393A3B'
                '3C3D3E3F' '40414243' '44454647' '48494A4B' '4C4D4E4F'
                '50515253' '54555657' '58595A5B' '5C5D5E5F' '60616263'
                '64656667' '68696A6B' '6C6D6E6F' '70717273' '74757677'
                '78797A7B' '7C7D7E7F' '80818283' '84858687' '88898A8B'
                '8C8D8E8F' '90919293' '94959697' '98999A9B' '9C9D9E9F'
                'A0A1A2A3' 'A4A5A6A7' 'A8A9AAAB' 'ACADAEAF' 'B0B1B2B3'
                'B4B5B6B7' 'B8B9BABB' 'BCBDBEBF' 'C0C1C2C3' 'C4C5C6C7',
                'hex',
            ),
            mac=codecs.decode(
                'D93EC8D2' 'DE1AD2A9' '957CB9B8' '3F14E76A' 'D6B5E0CC'
                'E285079A' '127D3B14' 'BCCB7AA7' '286D4AC0' 'D4CE6421'
                '5F2BC9E6' '870B33D9' '7438BE4A' 'AA20CDA5' 'C5A912B4'
                '8B8E27F3',
                'hex',
            ),
        ),
    )

    def test_hmac(self):
        iio = BytesIO()
        for tv in self.__class__.TEST_VECTORS:
            iio.truncate(0)
            iio.seek(0)

            iio.write(tv.text)
            iio.seek(0)
            digest = hmac.digest(iio, tv.key, digestcls=tv.digestcls)

            self.assertEqual(tv.mac, digest,
                             "{}{}".format(tv.digestcls, tv.text))


if __name__ == '__main__':
    unittest.main()
