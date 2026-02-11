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
        # NIST SP 800-38A CFB128 test vectors
        # (see https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-38a.pdf
        #  Appendix F.3)
        # AES128-CFB
        TestVector(
            moo=aes.MoO.CFB,
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
                '3B3FD92E' 'B72DAD20' '333449F8' 'E83CFB4A'
                'C8A64537' 'A0B3A93F' 'CDE3CDAD' '9F1CE58B'
                '26751F67' 'A3CBB140' 'B1808CF1' '87A4F4DF'
                'C04B0535' '7C5D1C0E' 'EAC4C66F' '9FF7F2E6',
                'hex',
            ),
        ),
        # AES192-CFB
        TestVector(
            moo=aes.MoO.CFB,
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
                'CDC80D6F' 'DDF18CAB' '34C25909' 'C99A4174'
                '67CE7F7F' '81173621' '961A2B70' '171D3D7A'
                '2E1E8A1D' 'D59B88B1' 'C8E60FED' '1EFAC4C9'
                'C05F9F9C' 'A9834FA0' '42AE8FBA' '584B09FF',
                'hex',
            ),
        ),
        # AES256-CFB
        TestVector(
            moo=aes.MoO.CFB,
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
                'DC7E84BF' 'DA79164B' '7ECD8486' '985D3860'
                '39FFED14' '3B28B1C8' '32113C63' '31E5407B'
                'DF101324' '15E54B92' 'A13ED0A8' '267AE2F9'
                '75A38574' '1AB9CEF8' '2031623D' '55B1E471',
                'hex',
            ),
        ),
        # NIST SP 800-38A OFB test vectors
        # (see https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-38a.pdf
        #  Appendix F.4)
        # AES128-OFB
        TestVector(
            moo=aes.MoO.OFB,
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
                '3B3FD92E' 'B72DAD20' '333449F8' 'E83CFB4A'
                '7789508D' '16918F03' 'F53C52DA' 'C54ED825'
                '9740051E' '9C5FECF6' '4344F7A8' '2260EDCC'
                '304C6528' 'F659C778' '66A510D9' 'C1D6AE5E',
                'hex',
            ),
        ),
        # AES192-OFB
        TestVector(
            moo=aes.MoO.OFB,
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
                'CDC80D6F' 'DDF18CAB' '34C25909' 'C99A4174'
                'FCC28B8D' '4C63837C' '09E81700' 'C1100401'
                '8D9A9AEA' 'C0F6596F' '559C6D4D' 'AF59A5F2'
                '6D9F2008' '57CA6C3E' '9CAC524B' 'D9ACC92A',
                'hex',
            ),
        ),
        # AES256-OFB
        TestVector(
            moo=aes.MoO.OFB,
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
                'DC7E84BF' 'DA79164B' '7ECD8486' '985D3860'
                '4FEBDC67' '40D20B3A' 'C88F6AD8' '2A4FB08D'
                '71AB47A0' '86E86EED' 'F39D1C5B' 'BA97C408'
                '0126141D' '67F37BE8' '538F5A8B' 'E740E484',
                'hex',
            ),
        ),
        # NIST SP 800-38A CTR test vectors
        # (see https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-38a.pdf
        #  Appendix F.5)
        # AES128-CTR
        TestVector(
            moo=aes.MoO.CTR,
            key=codecs.decode(
                '2B7E1516' '28AED2A6' 'ABF71588' '09CF4F3C',
                'hex',
            ),
            iv=codecs.decode(
                'F0F1F2F3' 'F4F5F6F7' 'F8F9FAFB' 'FCFDFEFF',
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
                'F0F1F2F3' 'F4F5F6F7' 'F8F9FAFB' 'FCFDFEFF'
                '874D6191' 'B620E326' '1BEF6864' '990DB6CE'
                '9806F66B' '7970FDFF' '8617187B' 'B9FFFDFF'
                '5AE4DF3E' 'DBD5D35E' '5B4F0902' '0DB03EAB'
                '1E031DDA' '2FBE03D1' '792170A0' 'F3009CEE',
                'hex',
            ),
        ),
        # AES192-CTR
        TestVector(
            moo=aes.MoO.CTR,
            key=codecs.decode(
                '8E73B0F7' 'DA0E6452' 'C810F32B' '809079E5'
                '62F8EAD2' '522C6B7B',
                'hex',
            ),
            iv=codecs.decode(
                'F0F1F2F3' 'F4F5F6F7' 'F8F9FAFB' 'FCFDFEFF',
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
                'F0F1F2F3' 'F4F5F6F7' 'F8F9FAFB' 'FCFDFEFF'
                '1ABC9324' '17521CA2' '4F2B0459' 'FE7E6E0B'
                '090339EC' '0AA6FAEF' 'D5CCC2C6' 'F4CE8E94'
                '1E36B26B' 'D1EBC670' 'D1BD1D66' '5620ABF7'
                '4F78A7F6' 'D2980958' '5A97DAEC' '58C6B050',
                'hex',
            ),
        ),
        # AES256-CTR
        TestVector(
            moo=aes.MoO.CTR,
            key=codecs.decode(
                '603DEB10' '15CA71BE' '2B73AEF0' '857D7781'
                '1F352C07' '3B6108D7' '2D9810A3' '0914DFF4',
                'hex',
            ),
            iv=codecs.decode(
                'F0F1F2F3' 'F4F5F6F7' 'F8F9FAFB' 'FCFDFEFF',
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
                'F0F1F2F3' 'F4F5F6F7' 'F8F9FAFB' 'FCFDFEFF'
                '601EC313' '775789A5' 'B7A7F504' 'BBF3D228'
                'F443E3CA' '4D62B59A' 'CA84E990' 'CACAF5C5'
                '2B0930DA' 'A23DE94C' 'E87017BA' '2D84988D'
                'DFC9C58D' 'B67AADA6' '13C2DD08' '457941A6',
                'hex',
            ),
        ),
        # NIST CAVP test vectors
        # (see https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/block-ciphers
        #  KAT_AES.zip: GFSbox, aesmmt.zip: MMT multi-block message tests)
        #
        # CAVP CFB128 GFSbox128 (zero key, varying IV)
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                'F34481EC' '3CC627BA' 'CD5DC3FB' '08F273E6',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                'F34481EC' '3CC627BA' 'CD5DC3FB' '08F273E6'
                '0336763E' '966D9259' '5A567CC9' 'CE537F5E',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '9798C464' '0BAD75C7' 'C3227DB9' '10174E72',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '9798C464' '0BAD75C7' 'C3227DB9' '10174E72'
                'A9A1631B' 'F4996954' 'EBC09395' '7B234589',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '96AB5C2F' 'F612D9DF' 'AAE8C31F' '30C42168',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '96AB5C2F' 'F612D9DF' 'AAE8C31F' '30C42168'
                'FF4F8391' 'A6A40CA5' 'B25D23BE' 'DD44A597',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '6A118A87' '4519E64E' '9963798A' '503F1D35',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '6A118A87' '4519E64E' '9963798A' '503F1D35'
                'DC43BE40' 'BE0E5371' '2F7E2BF5' 'CA707209',
                'hex',
            ),
        ),
        # CAVP CFB128 GFSbox192 (zero key, varying IV)
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '1B077A6A' 'F4B7F982' '29DE786D' '7516B639',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '1B077A6A' 'F4B7F982' '29DE786D' '7516B639'
                '275CFC04' '13D8CCB7' '0513C385' '9B1D0F72',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '9C2D8842' 'E5F48F57' '648205D3' '9A239AF1',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '9C2D8842' 'E5F48F57' '648205D3' '9A239AF1'
                'C9B8135F' 'F1B5ADC4' '13DFD053' 'B21BD96D',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                'BFF52510' '095F518E' 'CCA60AF4' '205444BB',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                'BFF52510' '095F518E' 'CCA60AF4' '205444BB'
                '4A3650C3' '371CE2EB' '35E389A1' '71427440',
                'hex',
            ),
        ),
        # CAVP CFB128 GFSbox256 (zero key, varying IV)
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '014730F8' '0AC625FE' '84F026C6' '0BFD547D',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '014730F8' '0AC625FE' '84F026C6' '0BFD547D'
                '5C9D844E' 'D46F9885' '085E5D6A' '4F94C7D7',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '0B24AF36' '193CE466' '5F2825D7' 'B4749C98',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '0B24AF36' '193CE466' '5F2825D7' 'B4749C98'
                'A9FF75BD' '7CF6613D' '3731C77C' '3B6D0C04',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '761C1FE4' '1A18ACF2' '0D241650' '611D90F1',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '761C1FE4' '1A18ACF2' '0D241650' '611D90F1'
                '623A52FC' 'EA5D443E' '48D9181A' 'B32C7421',
                'hex',
            ),
        ),
        # CAVP CFB128 MMT128 (multi-block, 2 blocks)
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '701CCC4C' '0E36E512' 'CE077F5A' 'F6CCB957',
                'hex',
            ),
            iv=codecs.decode(
                '5337DDEA' 'F89A00DD' '4D58D860' 'DE968469',
                'hex',
            ),
            text=codecs.decode(
                'CC1172F2' 'F80866D0' '768B25F7' '0FCF6361'
                'AAB7C627' 'C8488F97' '525D7D88' '949BEEEA',
                'hex',
            ),
            cipher=codecs.decode(
                '5337DDEA' 'F89A00DD' '4D58D860' 'DE968469'
                'CDCF093B' 'B7840DF2' '25683B58' 'A479B00D'
                '5DE5553A' '7E85EAE4' 'B70BF46D' 'C729DD31',
                'hex',
            ),
        ),
        # CAVP CFB128 MMT192 (multi-block, 2 blocks)
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                '69F9D298' '85743826' 'D7C5AFC5' '3637E6B1'
                'FA9512A1' '0EEA9CA9',
                'hex',
            ),
            iv=codecs.decode(
                '3743793C' '7144A755' '768437F4' 'EF5A33C8',
                'hex',
            ),
            text=codecs.decode(
                'F84EBF42' 'A758971C' '369949E2' '88F775C9'
                'CF6A82AB' '51B28657' '6B45652C' 'D68C3CE6',
                'hex',
            ),
            cipher=codecs.decode(
                '3743793C' '7144A755' '768437F4' 'EF5A33C8'
                'A3BD28BB' '817BDB3F' '6492827F' '2AA3E6E1'
                '34C25412' '9D8F20DB' 'C92389B7' 'D89702D6',
                'hex',
            ),
        ),
        # CAVP CFB128 MMT256 (multi-block, 2 blocks)
        TestVector(
            moo=aes.MoO.CFB,
            key=codecs.decode(
                'AE59254C' '66D8F533' 'E7F5002C' 'ED480C33'
                '984A421D' '7816E27B' 'E66C34C1' '9BFBC2A8',
                'hex',
            ),
            iv=codecs.decode(
                '821DD216' '53ECE3AF' '675CD25D' '26017AE3',
                'hex',
            ),
            text=codecs.decode(
                '3CB4F17E' '775C2D6D' '06DD60F1' '5D6C3A10'
                '3E513172' '7F9C6CB8' '0D13E00F' '316EB904',
                'hex',
            ),
            cipher=codecs.decode(
                '821DD216' '53ECE3AF' '675CD25D' '26017AE3'
                'AE375DB9' 'F28148C4' '60F6C6B6' '665FCC2F'
                'F6B50B8E' 'AF82C64B' 'BA8C649E' 'FD4731BC',
                'hex',
            ),
        ),
        # CAVP OFB GFSbox128 (zero key, varying IV)
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                'F34481EC' '3CC627BA' 'CD5DC3FB' '08F273E6',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                'F34481EC' '3CC627BA' 'CD5DC3FB' '08F273E6'
                '0336763E' '966D9259' '5A567CC9' 'CE537F5E',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '9798C464' '0BAD75C7' 'C3227DB9' '10174E72',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '9798C464' '0BAD75C7' 'C3227DB9' '10174E72'
                'A9A1631B' 'F4996954' 'EBC09395' '7B234589',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '96AB5C2F' 'F612D9DF' 'AAE8C31F' '30C42168',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '96AB5C2F' 'F612D9DF' 'AAE8C31F' '30C42168'
                'FF4F8391' 'A6A40CA5' 'B25D23BE' 'DD44A597',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '6A118A87' '4519E64E' '9963798A' '503F1D35',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '6A118A87' '4519E64E' '9963798A' '503F1D35'
                'DC43BE40' 'BE0E5371' '2F7E2BF5' 'CA707209',
                'hex',
            ),
        ),
        # CAVP OFB GFSbox192 (zero key, varying IV)
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '1B077A6A' 'F4B7F982' '29DE786D' '7516B639',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '1B077A6A' 'F4B7F982' '29DE786D' '7516B639'
                '275CFC04' '13D8CCB7' '0513C385' '9B1D0F72',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '9C2D8842' 'E5F48F57' '648205D3' '9A239AF1',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '9C2D8842' 'E5F48F57' '648205D3' '9A239AF1'
                'C9B8135F' 'F1B5ADC4' '13DFD053' 'B21BD96D',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                'BFF52510' '095F518E' 'CCA60AF4' '205444BB',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                'BFF52510' '095F518E' 'CCA60AF4' '205444BB'
                '4A3650C3' '371CE2EB' '35E389A1' '71427440',
                'hex',
            ),
        ),
        # CAVP OFB GFSbox256 (zero key, varying IV)
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '014730F8' '0AC625FE' '84F026C6' '0BFD547D',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '014730F8' '0AC625FE' '84F026C6' '0BFD547D'
                '5C9D844E' 'D46F9885' '085E5D6A' '4F94C7D7',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '0B24AF36' '193CE466' '5F2825D7' 'B4749C98',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '0B24AF36' '193CE466' '5F2825D7' 'B4749C98'
                'A9FF75BD' '7CF6613D' '3731C77C' '3B6D0C04',
                'hex',
            ),
        ),
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '00000000' '00000000' '00000000' '00000000'
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            iv=codecs.decode(
                '761C1FE4' '1A18ACF2' '0D241650' '611D90F1',
                'hex',
            ),
            text=codecs.decode(
                '00000000' '00000000' '00000000' '00000000',
                'hex',
            ),
            cipher=codecs.decode(
                '761C1FE4' '1A18ACF2' '0D241650' '611D90F1'
                '623A52FC' 'EA5D443E' '48D9181A' 'B32C7421',
                'hex',
            ),
        ),
        # CAVP OFB MMT128 (multi-block, 2 blocks)
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                'C9F4CE21' 'B4C7DAAA' '4F93E292' 'DC605BC5',
                'hex',
            ),
            iv=codecs.decode(
                '5E5A8CF2' '808C720E' '01C1ED92' 'D470A45D',
                'hex',
            ),
            text=codecs.decode(
                '8E19C5CA' 'CD015A66' '2E7F40CD' 'ECADBF79'
                'A68081C0' '6D9544B4' '1C2DD248' 'E77633B4',
                'hex',
            ),
            cipher=codecs.decode(
                '5E5A8CF2' '808C720E' '01C1ED92' 'D470A45D'
                '885DC48A' 'DD7EE6A1' '839BC5C5' 'E03BEAE0'
                '71301ECF' '91A01115' '20CDE0D3' 'A112F5D2',
                'hex',
            ),
        ),
        # CAVP OFB MMT192 (multi-block, 2 blocks)
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                '6A32B19F' 'C5F048A2' '9EFE9792' '7E8F91DF'
                '23390278' 'D4FC81EB',
                'hex',
            ),
            iv=codecs.decode(
                '39776BF5' 'D8965C7B' '795E3C6F' '23115CAC',
                'hex',
            ),
            text=codecs.decode(
                'E8BC8453' 'A7D47DE7' 'A9CCD943' '85B00869'
                '3E4645F3' '179311B4' 'A9A1E09C' '328012DC',
                'hex',
            ),
            cipher=codecs.decode(
                '39776BF5' 'D8965C7B' '795E3C6F' '23115CAC'
                '18132430' 'A50B89C6' '4C72C5D9' '092D8BFB'
                '84429179' '9D701516' '90CA8583' '7D89A79D',
                'hex',
            ),
        ),
        # CAVP OFB MMT256 (multi-block, 2 blocks)
        TestVector(
            moo=aes.MoO.OFB,
            key=codecs.decode(
                'A9257760' '7968DBEE' 'E135A24E' 'DC2F3263'
                '926D9714' '1F2C6D9F' '96C0012F' '45D1B3B0',
                'hex',
            ),
            iv=codecs.decode(
                '97BFEBEC' '0C2E7704' 'D002DC6A' '1FD36901',
                'hex',
            ),
            text=codecs.decode(
                'BB28705E' 'F9E5151A' 'FC73E388' '6F25F521'
                '75DBB57A' 'E36EACC5' 'AC4E989B' '9D69BFF9',
                'hex',
            ),
            cipher=codecs.decode(
                '97BFEBEC' '0C2E7704' 'D002DC6A' '1FD36901'
                '944169B5' '10B28255' '05A14B22' 'EABA744C'
                '19EE30DA' '6ED697E3' 'B879425F' '26808289',
                'hex',
            ),
        ),
    )

    def _vectors_for_moo(self, moo):
        return [tv for tv in self.__class__.TEST_VECTORS if tv.moo == moo]

    def _test_encrypt(self, moo):
        iio = BytesIO()
        oio = BytesIO()
        for tv in self._vectors_for_moo(moo):
            iio.truncate(0)
            iio.seek(0)
            oio.truncate(0)
            oio.seek(0)

            iio.write(tv.text)
            iio.seek(0)
            aes.encrypt(iio, oio, tv.key, tv.moo, tv.iv)
            oio.seek(0)

            self.assertEqual(tv.cipher.hex(), oio.read().hex())

    def _test_decrypt(self, moo):
        iio = BytesIO()
        oio = BytesIO()
        for tv in self._vectors_for_moo(moo):
            iio.truncate(0)
            iio.seek(0)
            oio.truncate(0)
            oio.seek(0)

            iio.write(tv.cipher)
            iio.seek(0)
            aes.decrypt(iio, oio, tv.key, tv.moo)
            oio.seek(0)

            self.assertEqual(tv.text.hex(), oio.read().hex())

    def _test_encrypt_decrypt(self, moo):
        iio = BytesIO()
        oio = BytesIO()
        for tv in self._vectors_for_moo(moo):
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

    def test_ecb_encrypt(self):
        self._test_encrypt(aes.MoO.ECB)

    def test_ecb_decrypt(self):
        self._test_decrypt(aes.MoO.ECB)

    def test_ecb_encrypt_decrypt(self):
        self._test_encrypt_decrypt(aes.MoO.ECB)

    def test_cbc_encrypt(self):
        self._test_encrypt(aes.MoO.CBC)

    def test_cbc_decrypt(self):
        self._test_decrypt(aes.MoO.CBC)

    def test_cbc_encrypt_decrypt(self):
        self._test_encrypt_decrypt(aes.MoO.CBC)

    def test_cfb_encrypt(self):
        self._test_encrypt(aes.MoO.CFB)

    def test_cfb_decrypt(self):
        self._test_decrypt(aes.MoO.CFB)

    def test_cfb_encrypt_decrypt(self):
        self._test_encrypt_decrypt(aes.MoO.CFB)

    def test_ofb_encrypt(self):
        self._test_encrypt(aes.MoO.OFB)

    def test_ofb_decrypt(self):
        self._test_decrypt(aes.MoO.OFB)

    def test_ofb_encrypt_decrypt(self):
        self._test_encrypt_decrypt(aes.MoO.OFB)

    def test_ctr_encrypt(self):
        self._test_encrypt(aes.MoO.CTR)

    def test_ctr_decrypt(self):
        self._test_decrypt(aes.MoO.CTR)

    def test_ctr_encrypt_decrypt(self):
        self._test_encrypt_decrypt(aes.MoO.CTR)


if __name__ == '__main__':
    unittest.main()
