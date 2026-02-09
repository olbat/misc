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
                '8CB82807230E1321D3FAE00D18CC2012',  # padding
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
                '612CCD79224B350935D45DD6A98F8176',  # padding
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
                '3F461796D6B0D6B2E0C2A72B4D80E644',  # padding
                'hex',
            ),
        ),
        # NIST CAVP test vectors
        # (see https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/block-ciphers
        #  KAT_AES.zip: GFSbox, KeySbox, VarKey, VarTxt
        #  aesmmt.zip: MMT multi-block message tests)
        #
        # CAVP ECB GFSbox128 (zero key, varying plaintext)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                'F34481EC' '3CC627BA' 'CD5DC3FB' '08F273E6',
                'hex',
            ),
            cipher=codecs.decode(
                '0336763E' '966D9259' '5A567CC9' 'CE537F5E'
                '0143DB63EE66B0CDFF9F69917680151E',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '9798C464' '0BAD75C7' 'C3227DB9' '10174E72',
                'hex',
            ),
            cipher=codecs.decode(
                'A9A1631B' 'F4996954' 'EBC09395' '7B234589'
                '0143DB63EE66B0CDFF9F69917680151E',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '6A118A87' '4519E64E' '9963798A' '503F1D35',
                'hex',
            ),
            cipher=codecs.decode(
                'DC43BE40' 'BE0E5371' '2F7E2BF5' 'CA707209'
                '0143DB63EE66B0CDFF9F69917680151E',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                'CB9FCEEC' '81286CA3' 'E989BD97' '9B0CB284',
                'hex',
            ),
            cipher=codecs.decode(
                '92BEEDAB' '1895A94F' 'AA69B632' 'E5CC47CE'
                '0143DB63EE66B0CDFF9F69917680151E',  # padding
                'hex',
            ),
        ),
        # CAVP ECB GFSbox192 (zero key, varying plaintext)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '1B077A6A' 'F4B7F982' '29DE786D' '7516B639',
                'hex',
            ),
            cipher=codecs.decode(
                '275CFC04' '13D8CCB7' '0513C385' '9B1D0F72'
                '02BB292527E726FD51EB29894D6F0AAD',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '9C2D8842' 'E5F48F57' '648205D3' '9A239AF1',
                'hex',
            ),
            cipher=codecs.decode(
                'C9B8135F' 'F1B5ADC4' '13DFD053' 'B21BD96D'
                '02BB292527E726FD51EB29894D6F0AAD',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '51719783' 'D3185A53' '5BD75ADC' '65071CE1',
                'hex',
            ),
            cipher=codecs.decode(
                '4F354592' 'FF7C8847' 'D2D0870C' 'A9481B7C'
                '02BB292527E726FD51EB29894D6F0AAD',  # padding
                'hex',
            ),
        ),
        # CAVP ECB GFSbox256 (zero key, varying plaintext)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '014730F8' '0AC625FE' '84F026C6' '0BFD547D',
                'hex',
            ),
            cipher=codecs.decode(
                '5C9D844E' 'D46F9885' '085E5D6A' '4F94C7D7'
                '1F788FE6D86C317549697FBF0C07FA43',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '0B24AF36' '193CE466' '5F2825D7' 'B4749C98',
                'hex',
            ),
            cipher=codecs.decode(
                'A9FF75BD' '7CF6613D' '3731C77C' '3B6D0C04'
                '1F788FE6D86C317549697FBF0C07FA43',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '8A560769' 'D605868A' 'D80D819B' 'DBA03771',
                'hex',
            ),
            cipher=codecs.decode(
                '38F2C7AE' '10612415' 'D27CA190' 'D27DA8B4'
                '1F788FE6D86C317549697FBF0C07FA43',  # padding
                'hex',
            ),
        ),
        # CAVP ECB KeySbox128 (varying key, zero plaintext)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '10A58869' 'D74BE5A3' '74CF867C' 'FB473859',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '6D251E69' '44B051E0' '4EAA6FB4' 'DBF78465'
                'B7A91C23C918915E2817064A220AFE19',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                'CAEA65CD' 'BB75E916' '9ECD22EB' 'E6E54675',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '6E292011' '90152DF4' 'EE058139' 'DEF610BB'
                'E514DBC1772C4E4348C63B3DB87E0CC9',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                'A2E2FA9B' 'AF7D2082' '2CA9F054' '2F764A41',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                'C3B44B95' 'D9D2F256' '70EEE9A0' 'DE099FA3'
                '70F20FFB0418919DB9E5F04E99A657DB',  # padding
                'hex',
            ),
        ),
        # CAVP ECB KeySbox192 (varying key, zero plaintext)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                'E9F065D7' 'C1357358' '7F787535' '7DFBB16C'
                '53489F6A' '4BD0F7CD',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '0956259C' '9CD5CFD0' '181CCA53' '380CDE06'
                '7CB1A4DE3BAA01E33330587C38191959',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '15D20F6E' 'BC7E649F' 'D95B76B1' '07E6DABA'
                '967C8A94' '84797F29',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '8E4E1842' '4E591A3D' '5B6F0876' 'F16F8594'
                'DA9FAF43A68AA2FFB633276AA1EBDB3D',  # padding
                'hex',
            ),
        ),
        # CAVP ECB KeySbox256 (varying key, zero plaintext)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                'C47B0294' 'DBBBEE0F' 'EC4757F2' '2FFEEE35'
                '87CA4730' 'C3D33B69' '1DF38BAB' '076BC558',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '46F2FB34' '2D6F0AB4' '77476FC5' '01242C5F'
                'B1AAD7F42738127ADED5E41A344EF682',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '28D46CFF' 'A1585331' '94214A91' 'E712FC2B'
                '45B51807' '6675AFFD' '910EDECA' '5F41AC64',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '4BF3B0A6' '9AEB6657' '794F2901' 'B1440AD4'
                '8DCBE1B398C5ECDB408D8D9A69F1341F',  # padding
                'hex',
            ),
        ),
        # CAVP ECB VarKey128 (single bit walks through key)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '80000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '0EDD33D3' 'C621E546' '455BD8BA' '1418BEC8'
                'AD745364CDCE28F146F26DDC4C6EC21A',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                'C0000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '4BC3F883' '450C113C' '64CA42E1' '112A9E87'
                '8D5C09720F7CA531C773829C248FAB0B',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                'E0000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '72A1DA77' '0F5D7AC4' 'C9EF94D8' '22AFFD97'
                '3750B749B0E1105F196D285F3819B96B',  # padding
                'hex',
            ),
        ),
        # CAVP ECB VarTxt128 (single bit walks through plaintext)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '80000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '3AD78E72' '6C1EC02B' '7EBFE92B' '23D9EC34'
                '0143DB63EE66B0CDFF9F69917680151E',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                'C0000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                'AAE5939C' '8EFDF2F0' '4E60B9FE' '7117B2C2'
                '0143DB63EE66B0CDFF9F69917680151E',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                'F0000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '96D9FD5C' 'C4F07441' '727DF0F3' '3E401A36'
                '0143DB63EE66B0CDFF9F69917680151E',  # padding
                'hex',
            ),
        ),
        # CAVP ECB MMT128 (multi-block, 2 blocks)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '7723D87D' '773A8BBF' 'E1AE5B08' '1235B566',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '1B0A69B7' 'BC534C16' 'CECFFAE0' '2CC53231'
                '90CEB413' 'F1DB3E9F' '0F79BA65' '4C54B60E',
                'hex',
            ),
            cipher=codecs.decode(
                'AD5B0895' '15E78210' '87C61652' 'DC477AB1'
                'F2CC6331' 'A70DFC59' 'C9FFB0C7' '23C682F6'
                '2CB90E7912C7C42662A651DB32A313A5',  # padding
                'hex',
            ),
        ),
        # CAVP ECB MMT192 (multi-block, 2 blocks)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                'C9C86A51' '224E5F19' '16D3F33A' '602F697A'
                'FC852A2C' '44D30D5F',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '64145E61' 'E61CD96F' '796B1874' '64FABBDE'
                '6F42E693' 'F501F1D7' '3B3C606F' '00801506',
                'hex',
            ),
            cipher=codecs.decode(
                '502A73E4' '051CFAC8' 'FE634321' '1A129F5A'
                '5F56710C' '41B32C84' 'DA978DDA' '2CEC34AD'
                'EC2BB2A9E2251F87C1059721AA06AD4D',  # padding
                'hex',
            ),
        ),
        # CAVP ECB MMT256 (multi-block, 2 blocks)
        TestVector(
            moo=aes.MoO.ECB,
            key=codecs.decode(
                '7A52E4D3' '42AA0725' '5A7E7C34' '266CF730'
                '2ABE2D4D' 'D7EC4468' 'A46187EE' '61825FFA',
                'hex',
            ),
            iv=None,
            text=codecs.decode(
                '7E771C6E' 'E4B26DB8' '9050E982' 'BA7E9803'
                'C8DA3460' '6434DD85' 'D2910E53' '8076D001',
                'hex',
            ),
            cipher=codecs.decode(
                'A91D8B2D' 'DF37520B' 'C469470A' 'D0DD6394'
                '923143CE' '55386BEB' '1F9C4BD5' '1584658E'
                '285ACECE46D6AC4ECAC2B38567E623EB',  # padding
                'hex',
            ),
        ),
        # CAVP CBC GFSbox128 (zero key, zero IV, varying plaintext)
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            text=codecs.decode(
                'F34481EC' '3CC627BA' 'CD5DC3FB' '08F273E6',
                'hex',
            ),
            cipher=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '0336763E' '966D9259' '5A567CC9' 'CE537F5E'
                'F1A80D711806421A109873DEF502863E',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            text=codecs.decode(
                '9798C464' '0BAD75C7' 'C3227DB9' '10174E72',
                'hex',
            ),
            cipher=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                'A9A1631B' 'F4996954' 'EBC09395' '7B234589'
                '3D88600058210E3CE7E1EE4605181F01',  # padding
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            text=codecs.decode(
                '96AB5C2F' 'F612D9DF' 'AAE8C31F' '30C42168',
                'hex',
            ),
            cipher=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                'FF4F8391' 'A6A40CA5' 'B25D23BE' 'DD44A597'
                'D607C2DC12AEDFFE19BA25A86E25D346',  # padding
                'hex',
            ),
        ),
        # CAVP CBC MMT128 (single block)
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                '1F8E4973' '953F3FB0' 'BD6B1666' '2E9A3C17',
                'hex',
            ),
            iv=codecs.decode(
                '2FE2B333' 'CEDA8F98' 'F4A99B40' 'D2CD34A8',
                'hex',
            ),
            text=codecs.decode(
                '45CF1296' '4FC824AB' '76616AE2' 'F4BF0822',
                'hex',
            ),
            cipher=codecs.decode(
                '2FE2B333' 'CEDA8F98' 'F4A99B40' 'D2CD34A8'
                '0F61C4D4' '4C5147C0' '3C195AD7' 'E2CC12B2'
                '4C3237FC66A07F6A7D2B267BDE1CF290',  # padding
                'hex',
            ),
        ),
        # CAVP CBC MMT128 (two blocks)
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                '0700D603' 'A1C514E4' '6B6191BA' '430A3A0C',
                'hex',
            ),
            iv=codecs.decode(
                'AAD1583C' 'D91365E3' 'BB2F0C34' '30D065BB',
                'hex',
            ),
            text=codecs.decode(
                '068B25C7' 'BFB1F8BD' 'D4CFC908' 'F69DFFC5'
                'DDC726A1' '97F0E5F7' '20F73039' '3279BE91',
                'hex',
            ),
            cipher=codecs.decode(
                'AAD1583C' 'D91365E3' 'BB2F0C34' '30D065BB'
                'C4DC61D9' '725967A3' '020104A9' '738F2386'
                '8527CE83' '9AAB1752' 'FD8BDB95' 'A82C4D00'
                '4231D12830D34B8E3BDE7380C81F493F',  # padding
                'hex',
            ),
        ),
        # CAVP CBC MMT192 (single block)
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                'BA75F4D1' 'D9D7CF7F' '551445D5' '6CC1A8AB'
                '2A078E15' 'E049DC2C',
                'hex',
            ),
            iv=codecs.decode(
                '531CE781' '76401666' 'AA30DB94' 'EC4A30EB',
                'hex',
            ),
            text=codecs.decode(
                'C51FC276' '774DAD94' 'BCDC1D28' '91EC8668',
                'hex',
            ),
            cipher=codecs.decode(
                '531CE781' '76401666' 'AA30DB94' 'EC4A30EB'
                '70DD95A1' '4EE975E2' '39DF36FF' '4AEE1D5D'
                '07F1AF01FC47E8ED8E9A37C7DA7E7B88',  # padding
                'hex',
            ),
        ),
        # CAVP CBC MMT192 (two blocks)
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                'EAB3B19C' '581AA873' 'E1981C83' 'AB8D83BB'
                'F8025111' 'FB2E6B21',
                'hex',
            ),
            iv=codecs.decode(
                'F3D6667E' '8D4D791E' '60F7505B' 'A383EB05',
                'hex',
            ),
            text=codecs.decode(
                '9D4E4CCC' 'D1682321' '856DF069' 'E3F1C6FA'
                '391A083A' '9FB02D59' 'DB74C140' '81B3ACC4',
                'hex',
            ),
            cipher=codecs.decode(
                'F3D6667E' '8D4D791E' '60F7505B' 'A383EB05'
                '51D44779' 'F90D40A8' '0048276C' '035CB49C'
                'A2A47BCB' '9B9CF727' '0B914479' '3787D53F'
                'C8B004400EFB95D53A9DA861C0E80447',  # padding
                'hex',
            ),
        ),
        # CAVP CBC MMT256 (single block)
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                '6ED76D2D' '97C69FD1' '33958952' '3931F2A6'
                'CFF554B1' '5F738F21' 'EC72DD97' 'A7330907',
                'hex',
            ),
            iv=codecs.decode(
                '851E8764' '776E6796' 'AAB722DB' 'B644ACE8',
                'hex',
            ),
            text=codecs.decode(
                '6282B8C0' '5C5C1530' 'B97D4816' 'CA434762',
                'hex',
            ),
            cipher=codecs.decode(
                '851E8764' '776E6796' 'AAB722DB' 'B644ACE8'
                '6ACC0414' '2E100A65' 'F51B97AD' 'F5172C41'
                '7435A6D53AADCB16AEF9EF582161CE6D',  # padding
                'hex',
            ),
        ),
        # CAVP CBC MMT256 (two blocks)
        TestVector(
            moo=aes.MoO.CBC,
            key=codecs.decode(
                'DCE26C6B' '4CFB2865' '10DA4EEC' 'D2CFFE6C'
                'DF430F33' 'DB9B5F77' 'B460679B' 'D49D13AE',
                'hex',
            ),
            iv=codecs.decode(
                'FDEAA134' 'C8D7379D' '457175FD' '1A57D3FC',
                'hex',
            ),
            text=codecs.decode(
                '50E9EEE1' 'AC528009' 'E8CBCD35' '6975881F'
                '957254B1' '3F91D7C6' '662D1031' '2052EB00',
                'hex',
            ),
            cipher=codecs.decode(
                'FDEAA134' 'C8D7379D' '457175FD' '1A57D3FC'
                '2FA0DF72' '2A9FD3B6' '4CB18FB2' 'B3DB55FF'
                '22674227' '57289413' 'F8F65750' '7412A64C'
                'DAFAE0644A2751BB47322995A88B9858',  # padding
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
