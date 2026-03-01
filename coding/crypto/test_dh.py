import unittest
from collections import namedtuple

import dh


class TestDH(unittest.TestCase):
    # test vectors from https://www.rfc-editor.org/rfc/rfc5114 Appendix A
    TestVector = namedtuple('TestVector', ['group_idx', 'xa', 'ya', 'xb', 'yb', 'secret'])
    TEST_VECTORS = (
        TestVector(
            group_idx=6,  # 1024-bit MODP Group with 160-bit Prime Order Subgroup
            xa=int(
                'B9A3B3AE' '8FEFC1A2' '93049650' '7086F845' '5D48943E',
                16,
            ),
            ya=int(
                '2A853B3D' '92197501' 'B9015B2D' 'EB3ED84F' '5E021DCC'
                '3E52F109' 'D3273D2B' '7521281C' 'BABE0E76' 'FF5727FA'
                '8ACCE269' '56BA9A1F' 'CA26F202' '28D8693F' 'EB10841D'
                '84A73600' '54ECE5A7' 'F5B7A61A' 'D3DFB3C6' '0D2E4310'
                '6D8727DA' '37DF9CCE' '95B47875' '5D06BCEA' '8F9D4596'
                '5F75A5F3' 'D1DF3701' '165FC9E5' '0C4279CE' 'B07F9895'
                '40AE96D5' 'D88ED776',
                16,
            ),
            xb=int(
                '9392C9F9' 'EB6A7A6A' '9022F7D8' '3E7223C6' '835BBDDA',
                16,
            ),
            yb=int(
                '717A6CB0' '53371FF4' 'A3B93294' '1C1E5663' 'F861A1D6'
                'AD34AE66' '576DFB98' 'F6C6CBF9' 'DDD5A56C' '7833F6BC'
                'FDFF0955' '82AD868E' '440E8D09' 'FD769E3C' 'ECCDC3D3'
                'B1E4CFA0' '57776CAA' 'F9739B6A' '9FEE8E74' '11F8D6DA'
                'C09D6A4E' 'DB46CC2B' '5D520309' '0EAE6126' '311E53FD'
                '2C14B574' 'E6A3109A' '3DA1BE41' 'BDCEAA18' '6F5CE067'
                '16A2B6A0' '7B3C33FE',
                16,
            ),
            secret=int(
                '5C804F45' '4D30D9C4' 'DF85271F' '93528C91' 'DF6B48AB'
                '5F80B3B5' '9CAAC1B2' '8F8ACBA9' 'CD3E39F3' 'CB614525'
                'D9521D2E' '644C53B8' '07B810F3' '40062F25' '7D7D6FBF'
                'E8D5E8F0' '72E9B6E9' 'AFDA9413' 'EAFB2E8B' '0699B1FB'
                '5A0CACED' 'DEAEAD7E' '9CFBB36A' 'E2B42083' '5BD83A19'
                'FB0B5E96' 'BF8FA4D0' '9E345525' '167ECD91' '55416F46'
                'F408ED31' 'B63C6E6D',
                16,
            ),
        ),
        TestVector(
            group_idx=7,  # 2048-bit MODP Group with 224-bit Prime Order Subgroup
            xa=int(
                '22E62601' 'DBFFD067' '08A680F7' '47F361F7' '6D8F4F72' '1A0548E4'
                '83294B0C',
                16,
            ),
            ya=int(
                '1B3A6345' '1BD886E6' '99E67B49' '4E288BD7' 'F8E0D370' 'BADDA7A0'
                'EFD2FDE7' 'D8F66145' 'CC9F2804' '19975EB8' '08877C8A' '4C0C8E0B'
                'D48D4A54' '01EB1E87' '76BFEEE1' '34C03831' 'AC273CD9' 'D635AB0C'
                'E006A42A' '887E3F52' 'FB8766B6' '50F38078' 'BC8EE858' '0CEFE243'
                '968CFC4F' '8DC3DB08' '4554171D' '41BF2E86' '1B7BB4D6' '9DD0E01E'
                'A387CBAA' '5CA672AF' 'CBE8BDB9' 'D62D4CE1' '5F17DD36' 'F91ED1EE'
                'DD65CA4A' '06455CB9' '4CD40A52' 'EC360E84' 'B3C926E2' '2C4380A3'
                'BF309D56' '849768B7' 'F52CFDF6' '55FD053A' '7EF70697' '9E7E5806'
                'B17DFAE5' '3AD2A5BC' '568EBB52' '9A7A61D6' '8D256F8F' 'C97C074A'
                '861D827E' '2EBC8C61' '34553115' 'B70E7103' '920AA16D' '85E52BCB'
                'AB8D786A' '68178FA8' 'FF7C2F5C' '71648D6F',
                16,
            ),
            xb=int(
                '4FF3BC96' 'C7FC6A6D' '71D3B363' '800A7CDF' 'EF6FC41B' '4417EA15'
                '353B7590',
                16,
            ),
            yb=int(
                '4DCEE992' 'A9762A13' 'F2F83844' 'AD3D77EE' '0E31C971' '8B3DB6C2'
                '035D3961' '182C3E0B' 'A247EC41' '82D760CD' '48D99599' '970622A1'
                '881BBA2D' 'C822939C' '78C3912C' '6661FA54' '38B20766' '222B75E2'
                '4C2E3AD0' 'C7287236' '129525EE' '15B5DD79' '98AA04C4' 'A9696CAC'
                'D7172083' 'A97A8166' '4EAD2C47' '9E444E4C' '0654CC19' 'E28D7703'
                'CEE8DACD' '6126F5D6' '65EC52C6' '7255DB92' '014B037E' 'B621A2AC'
                '8E365DE0' '71FFC140' '0ACF077A' '12913DD8' 'DE894734' '37AB7BA3'
                '46743C1B' '215DD9C1' '2164A7E4' '053118D1' '99BEC8EF' '6FC56117'
                '0C84C87D' '10EE9A67' '4A1FA8FF' 'E13BDFBA' '1D44DE48' '946D68DC'
                '0CDD7776' '35A7AB5B' 'FB1E4BB7' 'B856F968' '27734C18' '4138E915'
                'D9C3002E' 'BCE53120' '546A7E20' '02142B6C',
                16,
            ),
            secret=int(
                '34D9BDDC' '1B42176C' '313FEA03' '4C21034D' '074A6313' 'BB4ECDB3'
                '703FFF42' '4567A46B' 'DF75530E' 'DE0A9DA5' '229DE7D7' '6732286C'
                'BC0F91DA' '4C3C852F' 'C099C679' '531D94C7' '8AB03D9D' 'ECB0A4E4'
                'CA8B2BB4' '591C4021' 'CF8CE3A2' '0A541D33' '994017D0' '200AE2C9'
                '516E2FF5' '14577926' '9E862B0F' 'B474A2D5' '6DC31ED5' '69A7700B'
                '4C4AB16B' '22A45513' '531EF523' 'D7121207' '7B5A169B' 'DEFFAD7A'
                'D9608284' 'C7795B6D' '5A5183B8' '7066DE17' 'D8D671C9' 'EBD8EC89'
                '544D45EC' '061593D4' '42C62AB9' 'CE3B1CB9' '943A1D23' 'A5EA3BCF'
                '21A01471' 'E67E003E' '7F8A69C7' '28BE490B' '2FC88CFE' 'B92DB6A2'
                '15E5D03C' '17C464C9' 'AC1A46E2' '03E13F95' '2995FB03' 'C69D3CC4'
                '7FCB510B' '6998FFD3' 'AA6DE73C' 'F9F63869',
                16,
            ),
        ),
        TestVector(
            group_idx=8,  # 2048-bit MODP Group with 256-bit Prime Order Subgroup
            xa=int(
                '0881382C' 'DB87660C' '6DC13E61' '4938D5B9' 'C8B2F248' '581CC5E3'
                '1B354543' '97FCE50E',
                16,
            ),
            ya=int(
                '2E9380C8' '323AF975' '45BC4941' 'DEB0EC37' '42C62FE0' 'ECE824A6'
                'ABDBE66C' '59BEE024' '2911BFB9' '67235CEB' 'A35AE13E' '4EC752BE'
                '630B92DC' '4BDE2847' 'A9C62CB8' '15274542' '1FB7EB60' 'A63C0FE9'
                '159FCCE7' '26CE7CD8' '523D7450' '667EF840' 'E4919121' 'EB5F01C8'
                'C9B0D3D6' '48A93BFB' '75689E82' '44AC134A' 'F544711C' 'E79A02DC'
                'C3422668' '4780DDDC' 'B4985941' '06C37F5B' 'C7985648' '7AF5AB02'
                '2A2E5E42' 'F09897C1' 'A85A11EA' '0212AF04' 'D9B4CEBC' '937C3C1A'
                '3E15A8A0' '342E3376' '15C84E7F' 'E3B8B9B8' '7FB1E73A' '15AF12A3'
                '0D746E06' 'DFC34F29' '0D797CE5' '1AA13AA7' '85BF6658' 'AFF5E4B0'
                '93003CBE' 'AF665B3C' '2E113A3A' '4E905269' '341DC071' '1426685F'
                '4EF37E86' '8A8126FF' '3F2279B5' '7CA67E29',
                16,
            ),
            xb=int(
                '7D62A7E3' 'EF36DE61' '7B13D1AF' 'B82C780D' '83A23BD4' 'EE670564'
                '5121F371' 'F546A53D',
                16,
            ),
            yb=int(
                '575F0351' 'BD2B1B81' '7448BDF8' '7A6C362C' '1E289D39' '03A30B98'
                '32C5741F' 'A250363E' '7ACBC7F7' '7F3DACBC' '1F131ADD' '8E03367E'
                'FF8FBBB3' 'E1C57844' '24809B25' 'AFE4D226' '2A1A6FD2' 'FAB64105'
                'CA30A674' 'E07F7809' '85208863' '2FC04923' '3791AD4E' 'DD083A97'
                '8B883EE6' '18BC5E0D' 'D047415F' '2D95E683' 'CF14826B' '5FBE10D3'
                'CE41C6C1' '20C78AB2' '0008C698' 'BF7F0BCA' 'B9D7F407' 'BED0F43A'
                'FB2970F5' '7F8D1204' '3963E66D' 'DD320D59' '9AD9936C' '8F44137C'
                '08B180EC' '5E985CEB' 'E186F3D5' '49677E80' '607331EE' '17AF3380'
                'A725B078' '2317D7DD' '43F59D7A' 'F9568A9B' 'B63A84D3' '65F92244'
                'ED120988' '219302F4' '2924C7CA' '90B89D24' 'F71B0AB6' '97823D7D'
                'EB1AFF5B' '0E8E4A45' 'D49F7F53' '757E1913',
                16,
            ),
            secret=int(
                '86C70BF8' 'D0BB81BB' '01078A17' '219CB7D2' '7203DB2A' '19C877F1'
                'D1F19FD7' 'D77EF225' '46A68F00' '5AD52DC8' '4553B78F' 'C60330BE'
                '51EA7C06' '72CAC151' '5E4B35C0' '47B9A551' 'B88F39DC' '26DA14A0'
                '9EF74774' 'D47C762D' 'D177F9ED' '5BC2F11E' '52C879BD' '95098504'
                'CD9EECD8' 'A8F9B3EF' 'BD1F008A' 'C5853097' 'D9D1837F' '2B18F77C'
                'D7BE01AF' '80A7C7B5' 'EA3CA54C' 'C02D0C11' '6FEE3F95' 'BB873993'
                '85875D7E' '86747E67' '6E728938' 'ACBFF709' '8E05BE4D' 'CFB24052'
                'B83AEFFB' '14783F02' '9ADBDE7F' '53FAE920' '84224090' 'E007CEE9'
                '4D4BF2BA' 'CE9FFD4B' '57D2AF7C' '724D0CAA' '19BF0501' 'F6F17B4A'
                'A10F425E' '3EA76080' 'B4B9D6B3' 'CEFEA115' 'B2CEB878' '9BB8A3B0'
                'EA87FEBE' '63B6C8F8' '46EC6DB0' 'C26C5D7C',
                16,
            ),
        ),
    )

    def test_generate_public_key(self):
        for tv in self.__class__.TEST_VECTORS:
            g = dh.GROUPS[tv.group_idx]
            ya = dh.generate_public_key(g.g, g.p, tv.xa)
            self.assertEqual(ya, tv.ya, "group {}".format(tv.group_idx))

            yb = dh.generate_public_key(g.g, g.p, tv.xb)
            self.assertEqual(yb, tv.yb, "group {}".format(tv.group_idx))

    def test_generate_shared_secret(self):
        for tv in self.__class__.TEST_VECTORS:
            g = dh.GROUPS[tv.group_idx]
            # RFC 5114 groups have non-safe prime p; skip DDH check
            sa = dh.generate_shared_secret(g.p, tv.xa, tv.yb, check=False)
            sb = dh.generate_shared_secret(g.p, tv.xb, tv.ya, check=False)
            self.assertEqual(sa, sb, "group {}".format(tv.group_idx))
            self.assertEqual(sa, tv.secret, "group {}".format(tv.group_idx))


class TestPublicKeyCheck(unittest.TestCase):
    """Test DDH-based public key validation (check_public_key)."""

    def test_invalid_keys_rejected(self):
        # test against the first RFC 3526 safe-prime group (1536-bit)
        p = dh.GROUPS[0].p
        for bad in (0, 1, 2, p - 1, p, p + 1):
            self.assertFalse(dh.check_public_key(p, bad),
                             "expected False for key={}".format(bad))

    def test_rfc3526_generated_key_accepted(self):
        # a key generated using a RFC 3526 safe-prime group must pass the check
        g = dh.GROUPS[0]  # 1536-bit MODP Group
        priv = dh.generate_private_key(256)
        pub = dh.generate_public_key(g.g, g.p, priv)
        self.assertTrue(dh.check_public_key(g.p, pub))


class TestKeyExchange(unittest.TestCase):
    """Test that both parties derive the same shared secret."""

    def test_shared_secret_symmetric_rfc3526(self):
        # use the 1536-bit RFC 3526 group (MODP safe prime, check=True is valid)
        g = dh.GROUPS[0]
        xa = dh.generate_private_key(256)
        xb = dh.generate_private_key(256)
        ya = dh.generate_public_key(g.g, g.p, xa)
        yb = dh.generate_public_key(g.g, g.p, xb)
        sa = dh.generate_shared_secret(g.p, xa, yb)
        sb = dh.generate_shared_secret(g.p, xb, ya)
        self.assertEqual(sa, sb)

    def test_shared_secret_symmetric_rfc5114(self):
        # use the 1024-bit RFC 5114 group with skip of DDH check (non-safe prime)
        g = dh.GROUPS[6]
        xa = dh.generate_private_key(160)
        xb = dh.generate_private_key(160)
        ya = dh.generate_public_key(g.g, g.p, xa)
        yb = dh.generate_public_key(g.g, g.p, xb)
        sa = dh.generate_shared_secret(g.p, xa, yb, check=False)
        sb = dh.generate_shared_secret(g.p, xb, ya, check=False)
        self.assertEqual(sa, sb)

    def test_invalid_public_key_rejected(self):
        g = dh.GROUPS[0]
        xa = dh.generate_private_key(256)
        with self.assertRaises(ValueError):
            dh.generate_shared_secret(g.p, xa, 1)

    def test_different_private_keys_give_same_secret(self):
        # sanity check: g^(xa*xb) == g^(xb*xa) mod p
        g = dh.GROUPS[6]
        xa = dh.generate_private_key(160)
        xb = dh.generate_private_key(160)
        ya = dh.generate_public_key(g.g, g.p, xa)
        yb = dh.generate_public_key(g.g, g.p, xb)
        self.assertEqual(
            dh.generate_shared_secret(g.p, xa, yb, check=False),
            dh.generate_shared_secret(g.p, xb, ya, check=False),
        )


class TestPrivateKey(unittest.TestCase):
    """Test private key generation."""

    def test_private_key_is_integer(self):
        key = dh.generate_private_key(256)
        self.assertIsInstance(key, int)

    def test_private_key_positive(self):
        key = dh.generate_private_key(256)
        self.assertGreater(key, 0)

    def test_private_key_bit_length(self):
        for bits in (128, 160, 224, 256):
            key = dh.generate_private_key(bits)
            self.assertLessEqual(key.bit_length(), bits,
                                 "key too large for {} bits".format(bits))

    def test_private_keys_are_distinct(self):
        keys = [dh.generate_private_key(256) for _ in range(4)]
        self.assertEqual(len(set(keys)), 4)


if __name__ == '__main__':
    unittest.main()
