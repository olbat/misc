"""
usage: {0} <mode> [<options>]

modes:
  list-groups
  genkeys   GROUP SIZE > KEYS
  gensecret KEYS OTHERS_KEYS > SECRET

examples:
  # list the available DH groups
  python {0} list-groups

  # generate a first key pair
  python {0} genkeys 8 256 > keys1

  # generate a second key pair
  python {0} genkeys 8 256 > keys2

  # generate the shared secret
  python {0} gensecret keys1 keys2

  # extra test
  cmp <(python {0} gensecret keys1 keys2) \\
      <(python {0} gensecret keys2 keys1)
"""
# see https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
#     http://people.csail.mit.edu/vinodv/COURSES/MAT302-S13/MerklePuzzlepaper.pdf
#     http://www.ietf.org/rfc/rfc3526.txt
#     http://www.ietf.org/rfc/rfc5114.txt


from collections import namedtuple
from random import getrandbits

DHGroup = namedtuple('DHGroup', ['g', 'p', 'desc'])

GROUPS = (
    DHGroup(
        desc='1536-bit MODP Group (RFC 3526)',
        g=2,
        p=int(
            "FFFFFFFF" "FFFFFFFF" "C90FDAA2" "2168C234" "C4C6628B" "80DC1CD1"
            "29024E08" "8A67CC74" "020BBEA6" "3B139B22" "514A0879" "8E3404DD"
            "EF9519B3" "CD3A431B" "302B0A6D" "F25F1437" "4FE1356D" "6D51C245"
            "E485B576" "625E7EC6" "F44C42E9" "A637ED6B" "0BFF5CB6" "F406B7ED"
            "EE386BFB" "5A899FA5" "AE9F2411" "7C4B1FE6" "49286651" "ECE45B3D"
            "C2007CB8" "A163BF05" "98DA4836" "1C55D39A" "69163FA8" "FD24CF5F"
            "83655D23" "DCA3AD96" "1C62F356" "208552BB" "9ED52907" "7096966D"
            "670C354E" "4ABC9804" "F1746C08" "CA237327" "FFFFFFFF" "FFFFFFFF",
            16
        )
    ),
    DHGroup(
        desc='2048-bit MODP Group (RFC 3526)',
        g=2,
        p=int(
            "FFFFFFFF" "FFFFFFFF" "C90FDAA2" "2168C234" "C4C6628B" "80DC1CD1"
            "29024E08" "8A67CC74" "020BBEA6" "3B139B22" "514A0879" "8E3404DD"
            "EF9519B3" "CD3A431B" "302B0A6D" "F25F1437" "4FE1356D" "6D51C245"
            "E485B576" "625E7EC6" "F44C42E9" "A637ED6B" "0BFF5CB6" "F406B7ED"
            "EE386BFB" "5A899FA5" "AE9F2411" "7C4B1FE6" "49286651" "ECE45B3D"
            "C2007CB8" "A163BF05" "98DA4836" "1C55D39A" "69163FA8" "FD24CF5F"
            "83655D23" "DCA3AD96" "1C62F356" "208552BB" "9ED52907" "7096966D"
            "670C354E" "4ABC9804" "F1746C08" "CA18217C" "32905E46" "2E36CE3B"
            "E39E772C" "180E8603" "9B2783A2" "EC07A28F" "B5C55DF0" "6F4C52C9"
            "DE2BCBF6" "95581718" "3995497C" "EA956AE5" "15D22618" "98FA0510"
            "15728E5A" "8AACAA68" "FFFFFFFF" "FFFFFFFF",
            16
        )
    ),
    DHGroup(
        desc='3072-bit MODP Group (RFC 3526)',
        g=2,
        p=int(
            "FFFFFFFF" "FFFFFFFF" "C90FDAA2" "2168C234" "C4C6628B" "80DC1CD1"
            "29024E08" "8A67CC74" "020BBEA6" "3B139B22" "514A0879" "8E3404DD"
            "EF9519B3" "CD3A431B" "302B0A6D" "F25F1437" "4FE1356D" "6D51C245"
            "E485B576" "625E7EC6" "F44C42E9" "A637ED6B" "0BFF5CB6" "F406B7ED"
            "EE386BFB" "5A899FA5" "AE9F2411" "7C4B1FE6" "49286651" "ECE45B3D"
            "C2007CB8" "A163BF05" "98DA4836" "1C55D39A" "69163FA8" "FD24CF5F"
            "83655D23" "DCA3AD96" "1C62F356" "208552BB" "9ED52907" "7096966D"
            "670C354E" "4ABC9804" "F1746C08" "CA18217C" "32905E46" "2E36CE3B"
            "E39E772C" "180E8603" "9B2783A2" "EC07A28F" "B5C55DF0" "6F4C52C9"
            "DE2BCBF6" "95581718" "3995497C" "EA956AE5" "15D22618" "98FA0510"
            "15728E5A" "8AAAC42D" "AD33170D" "04507A33" "A85521AB" "DF1CBA64"
            "ECFB8504" "58DBEF0A" "8AEA7157" "5D060C7D" "B3970F85" "A6E1E4C7"
            "ABF5AE8C" "DB0933D7" "1E8C94E0" "4A25619D" "CEE3D226" "1AD2EE6B"
            "F12FFA06" "D98A0864" "D8760273" "3EC86A64" "521F2B18" "177B200C"
            "BBE11757" "7A615D6C" "770988C0" "BAD946E2" "08E24FA0" "74E5AB31"
            "43DB5BFC" "E0FD108E" "4B82D120" "A93AD2CA" "FFFFFFFF" "FFFFFFFF",
            16
        )
    ),
    DHGroup(
        desc='4096-bit MODP Group (RFC 3526)',
        g=2,
        p=int(
            "FFFFFFFF" "FFFFFFFF" "C90FDAA2" "2168C234" "C4C6628B" "80DC1CD1"
            "29024E08" "8A67CC74" "020BBEA6" "3B139B22" "514A0879" "8E3404DD"
            "EF9519B3" "CD3A431B" "302B0A6D" "F25F1437" "4FE1356D" "6D51C245"
            "E485B576" "625E7EC6" "F44C42E9" "A637ED6B" "0BFF5CB6" "F406B7ED"
            "EE386BFB" "5A899FA5" "AE9F2411" "7C4B1FE6" "49286651" "ECE45B3D"
            "C2007CB8" "A163BF05" "98DA4836" "1C55D39A" "69163FA8" "FD24CF5F"
            "83655D23" "DCA3AD96" "1C62F356" "208552BB" "9ED52907" "7096966D"
            "670C354E" "4ABC9804" "F1746C08" "CA18217C" "32905E46" "2E36CE3B"
            "E39E772C" "180E8603" "9B2783A2" "EC07A28F" "B5C55DF0" "6F4C52C9"
            "DE2BCBF6" "95581718" "3995497C" "EA956AE5" "15D22618" "98FA0510"
            "15728E5A" "8AAAC42D" "AD33170D" "04507A33" "A85521AB" "DF1CBA64"
            "ECFB8504" "58DBEF0A" "8AEA7157" "5D060C7D" "B3970F85" "A6E1E4C7"
            "ABF5AE8C" "DB0933D7" "1E8C94E0" "4A25619D" "CEE3D226" "1AD2EE6B"
            "F12FFA06" "D98A0864" "D8760273" "3EC86A64" "521F2B18" "177B200C"
            "BBE11757" "7A615D6C" "770988C0" "BAD946E2" "08E24FA0" "74E5AB31"
            "43DB5BFC" "E0FD108E" "4B82D120" "A9210801" "1A723C12" "A787E6D7"
            "88719A10" "BDBA5B26" "99C32718" "6AF4E23C" "1A946834" "B6150BDA"
            "2583E9CA" "2AD44CE8" "DBBBC2DB" "04DE8EF9" "2E8EFC14" "1FBECAA6"
            "287C5947" "4E6BC05D" "99B2964F" "A090C3A2" "233BA186" "515BE7ED"
            "1F612970" "CEE2D7AF" "B81BDD76" "2170481C" "D0069127" "D5B05AA9"
            "93B4EA98" "8D8FDDC1" "86FFB7DC" "90A6C08F" "4DF435C9" "34063199"
            "FFFFFFFF" "FFFFFFFF",
            16
        )
    ),
    DHGroup(
        desc='6144-bit MODP Group (RFC 3526)',
        g=2,
        p=int(
            "FFFFFFFF" "FFFFFFFF" "C90FDAA2" "2168C234" "C4C6628B" "80DC1CD1"
            "29024E08" "8A67CC74" "020BBEA6" "3B139B22" "514A0879" "8E3404DD"
            "EF9519B3" "CD3A431B" "302B0A6D" "F25F1437" "4FE1356D" "6D51C245"
            "E485B576" "625E7EC6" "F44C42E9" "A637ED6B" "0BFF5CB6" "F406B7ED"
            "EE386BFB" "5A899FA5" "AE9F2411" "7C4B1FE6" "49286651" "ECE45B3D"
            "C2007CB8" "A163BF05" "98DA4836" "1C55D39A" "69163FA8" "FD24CF5F"
            "83655D23" "DCA3AD96" "1C62F356" "208552BB" "9ED52907" "7096966D"
            "670C354E" "4ABC9804" "F1746C08" "CA18217C" "32905E46" "2E36CE3B"
            "E39E772C" "180E8603" "9B2783A2" "EC07A28F" "B5C55DF0" "6F4C52C9"
            "DE2BCBF6" "95581718" "3995497C" "EA956AE5" "15D22618" "98FA0510"
            "15728E5A" "8AAAC42D" "AD33170D" "04507A33" "A85521AB" "DF1CBA64"
            "ECFB8504" "58DBEF0A" "8AEA7157" "5D060C7D" "B3970F85" "A6E1E4C7"
            "ABF5AE8C" "DB0933D7" "1E8C94E0" "4A25619D" "CEE3D226" "1AD2EE6B"
            "F12FFA06" "D98A0864" "D8760273" "3EC86A64" "521F2B18" "177B200C"
            "BBE11757" "7A615D6C" "770988C0" "BAD946E2" "08E24FA0" "74E5AB31"
            "43DB5BFC" "E0FD108E" "4B82D120" "A9210801" "1A723C12" "A787E6D7"
            "88719A10" "BDBA5B26" "99C32718" "6AF4E23C" "1A946834" "B6150BDA"
            "2583E9CA" "2AD44CE8" "DBBBC2DB" "04DE8EF9" "2E8EFC14" "1FBECAA6"
            "287C5947" "4E6BC05D" "99B2964F" "A090C3A2" "233BA186" "515BE7ED"
            "1F612970" "CEE2D7AF" "B81BDD76" "2170481C" "D0069127" "D5B05AA9"
            "93B4EA98" "8D8FDDC1" "86FFB7DC" "90A6C08F" "4DF435C9" "34028492"
            "36C3FAB4" "D27C7026" "C1D4DCB2" "602646DE" "C9751E76" "3DBA37BD"
            "F8FF9406" "AD9E530E" "E5DB382F" "413001AE" "B06A53ED" "9027D831"
            "179727B0" "865A8918" "DA3EDBEB" "CF9B14ED" "44CE6CBA" "CED4BB1B"
            "DB7F1447" "E6CC254B" "33205151" "2BD7AF42" "6FB8F401" "378CD2BF"
            "5983CA01" "C64B92EC" "F032EA15" "D1721D03" "F482D7CE" "6E74FEF6"
            "D55E702F" "46980C82" "B5A84031" "900B1C9E" "59E7C97F" "BEC7E8F3"
            "23A97A7E" "36CC88BE" "0F1D45B7" "FF585AC5" "4BD407B2" "2B4154AA"
            "CC8F6D7E" "BF48E1D8" "14CC5ED2" "0F8037E0" "A79715EE" "F29BE328"
            "06A1D58B" "B7C5DA76" "F550AA3D" "8A1FBFF0" "EB19CCB1" "A313D55C"
            "DA56C9EC" "2EF29632" "387FE8D7" "6E3C0468" "043E8F66" "3F4860EE"
            "12BF2D5B" "0B7474D6" "E694F91E" "6DCC4024" "FFFFFFFF" "FFFFFFFF",
            16
        )
    ),
    DHGroup(
        desc='8192-bit MODP Group (RFC 3526)',
        g=2,
        p=int(
            "FFFFFFFF" "FFFFFFFF" "C90FDAA2" "2168C234" "C4C6628B" "80DC1CD1"
            "29024E08" "8A67CC74" "020BBEA6" "3B139B22" "514A0879" "8E3404DD"
            "EF9519B3" "CD3A431B" "302B0A6D" "F25F1437" "4FE1356D" "6D51C245"
            "E485B576" "625E7EC6" "F44C42E9" "A637ED6B" "0BFF5CB6" "F406B7ED"
            "EE386BFB" "5A899FA5" "AE9F2411" "7C4B1FE6" "49286651" "ECE45B3D"
            "C2007CB8" "A163BF05" "98DA4836" "1C55D39A" "69163FA8" "FD24CF5F"
            "83655D23" "DCA3AD96" "1C62F356" "208552BB" "9ED52907" "7096966D"
            "670C354E" "4ABC9804" "F1746C08" "CA18217C" "32905E46" "2E36CE3B"
            "E39E772C" "180E8603" "9B2783A2" "EC07A28F" "B5C55DF0" "6F4C52C9"
            "DE2BCBF6" "95581718" "3995497C" "EA956AE5" "15D22618" "98FA0510"
            "15728E5A" "8AAAC42D" "AD33170D" "04507A33" "A85521AB" "DF1CBA64"
            "ECFB8504" "58DBEF0A" "8AEA7157" "5D060C7D" "B3970F85" "A6E1E4C7"
            "ABF5AE8C" "DB0933D7" "1E8C94E0" "4A25619D" "CEE3D226" "1AD2EE6B"
            "F12FFA06" "D98A0864" "D8760273" "3EC86A64" "521F2B18" "177B200C"
            "BBE11757" "7A615D6C" "770988C0" "BAD946E2" "08E24FA0" "74E5AB31"
            "43DB5BFC" "E0FD108E" "4B82D120" "A9210801" "1A723C12" "A787E6D7"
            "88719A10" "BDBA5B26" "99C32718" "6AF4E23C" "1A946834" "B6150BDA"
            "2583E9CA" "2AD44CE8" "DBBBC2DB" "04DE8EF9" "2E8EFC14" "1FBECAA6"
            "287C5947" "4E6BC05D" "99B2964F" "A090C3A2" "233BA186" "515BE7ED"
            "1F612970" "CEE2D7AF" "B81BDD76" "2170481C" "D0069127" "D5B05AA9"
            "93B4EA98" "8D8FDDC1" "86FFB7DC" "90A6C08F" "4DF435C9" "34028492"
            "36C3FAB4" "D27C7026" "C1D4DCB2" "602646DE" "C9751E76" "3DBA37BD"
            "F8FF9406" "AD9E530E" "E5DB382F" "413001AE" "B06A53ED" "9027D831"
            "179727B0" "865A8918" "DA3EDBEB" "CF9B14ED" "44CE6CBA" "CED4BB1B"
            "DB7F1447" "E6CC254B" "33205151" "2BD7AF42" "6FB8F401" "378CD2BF"
            "5983CA01" "C64B92EC" "F032EA15" "D1721D03" "F482D7CE" "6E74FEF6"
            "D55E702F" "46980C82" "B5A84031" "900B1C9E" "59E7C97F" "BEC7E8F3"
            "23A97A7E" "36CC88BE" "0F1D45B7" "FF585AC5" "4BD407B2" "2B4154AA"
            "CC8F6D7E" "BF48E1D8" "14CC5ED2" "0F8037E0" "A79715EE" "F29BE328"
            "06A1D58B" "B7C5DA76" "F550AA3D" "8A1FBFF0" "EB19CCB1" "A313D55C"
            "DA56C9EC" "2EF29632" "387FE8D7" "6E3C0468" "043E8F66" "3F4860EE"
            "12BF2D5B" "0B7474D6" "E694F91E" "6DBE1159" "74A3926F" "12FEE5E4"
            "38777CB6" "A932DF8C" "D8BEC4D0" "73B931BA" "3BC832B6" "8D9DD300"
            "741FA7BF" "8AFC47ED" "2576F693" "6BA42466" "3AAB639C" "5AE4F568"
            "3423B474" "2BF1C978" "238F16CB" "E39D652D" "E3FDB8BE" "FC848AD9"
            "22222E04" "A4037C07" "13EB57A8" "1A23F0C7" "3473FC64" "6CEA306B"
            "4BCBC886" "2F8385DD" "FA9D4B7F" "A2C087E8" "79683303" "ED5BDD3A"
            "062B3CF5" "B3A278A6" "6D2A13F8" "3F44F82D" "DF310EE0" "74AB6A36"
            "4597E899" "A0255DC1" "64F31CC5" "0846851D" "F9AB4819" "5DED7EA1"
            "B1D510BD" "7EE74D73" "FAF36BC3" "1ECFA268" "359046F4" "EB879F92"
            "4009438B" "481C6CD7" "889A002E" "D5EE382B" "C9190DA6" "FC026E47"
            "9558E447" "5677E9AA" "9E3050E2" "765694DF" "C81F56E8" "80B96E71"
            "60C980DD" "98EDD3DF" "FFFFFFFF" "FFFFFFFF",
            16
        )
    ),
    DHGroup(
        desc='1024-bit MODP Group with 160-bit Prime Order Subgroup (RFC 5114)',
        g=int(
            "A4D1CBD5" "C3FD3412" "6765A442" "EFB99905" "F8104DD2" "58AC507F"
            "D6406CFF" "14266D31" "266FEA1E" "5C41564B" "777E690F" "5504F213"
            "160217B4" "B01B886A" "5E91547F" "9E2749F4" "D7FBD7D3" "B9A92EE1"
            "909D0D22" "63F80A76" "A6A24C08" "7A091F53" "1DBF0A01" "69B6A28A"
            "D662A4D1" "8E73AFA3" "2D779D59" "18D08BC8" "858F4DCE" "F97C2A24"
            "855E6EEB" "22B3B2E5",
            16
        ),
        p=int(
            "B10B8F96" "A080E01D" "DE92DE5E" "AE5D54EC" "52C99FBC" "FB06A3C6"
            "9A6A9DCA" "52D23B61" "6073E286" "75A23D18" "9838EF1E" "2EE652C0"
            "13ECB4AE" "A9061123" "24975C3C" "D49B83BF" "ACCBDD7D" "90C4BD70"
            "98488E9C" "219A7372" "4EFFD6FA" "E5644738" "FAA31A4F" "F55BCCC0"
            "A151AF5F" "0DC8B4BD" "45BF37DF" "365C1A65" "E68CFDA7" "6D4DA708"
            "DF1FB2BC" "2E4A4371",
            16
        )
    ),
    DHGroup(
        desc='2048-bit MODP Group with 224-bit Prime Order Subgroup (RFC 5114)',
        g=int(
            "AC4032EF" "4F2D9AE3" "9DF30B5C" "8FFDAC50" "6CDEBE7B" "89998CAF"
            "74866A08" "CFE4FFE3" "A6824A4E" "10B9A6F0" "DD921F01" "A70C4AFA"
            "AB739D77" "00C29F52" "C57DB17C" "620A8652" "BE5E9001" "A8D66AD7"
            "C1766910" "1999024A" "F4D02727" "5AC1348B" "B8A762D0" "521BC98A"
            "E2471504" "22EA1ED4" "09939D54" "DA7460CD" "B5F6C6B2" "50717CBE"
            "F180EB34" "118E98D1" "19529A45" "D6F83456" "6E3025E3" "16A330EF"
            "BB77A86F" "0C1AB15B" "051AE3D4" "28C8F8AC" "B70A8137" "150B8EEB"
            "10E183ED" "D19963DD" "D9E263E4" "770589EF" "6AA21E7F" "5F2FF381"
            "B539CCE3" "409D13CD" "566AFBB4" "8D6C0191" "81E1BCFE" "94B30269"
            "EDFE72FE" "9B6AA4BD" "7B5A0F1C" "71CFFF4C" "19C418E1" "F6EC0179"
            "81BC087F" "2A7065B3" "84B890D3" "191F2BFA",
            16
        ),
        p=int(
            "AD107E1E" "9123A9D0" "D660FAA7" "9559C51F" "A20D64E5" "683B9FD1"
            "B54B1597" "B61D0A75" "E6FA141D" "F95A56DB" "AF9A3C40" "7BA1DF15"
            "EB3D688A" "309C180E" "1DE6B85A" "1274A0A6" "6D3F8152" "AD6AC212"
            "9037C9ED" "EFDA4DF8" "D91E8FEF" "55B7394B" "7AD5B7D0" "B6C12207"
            "C9F98D11" "ED34DBF6" "C6BA0B2C" "8BBC27BE" "6A00E0A0" "B9C49708"
            "B3BF8A31" "70918836" "81286130" "BC8985DB" "1602E714" "415D9330"
            "278273C7" "DE31EFDC" "7310F712" "1FD5A074" "15987D9A" "DC0A486D"
            "CDF93ACC" "44328387" "315D75E1" "98C641A4" "80CD86A1" "B9E587E8"
            "BE60E69C" "C928B2B9" "C52172E4" "13042E9B" "23F10B0E" "16E79763"
            "C9B53DCF" "4BA80A29" "E3FB73C1" "6B8E75B9" "7EF363E2" "FFA31F71"
            "CF9DE538" "4E71B81C" "0AC4DFFE" "0C10E64F",
            16
        )
    ),
    DHGroup(
        desc='2048-bit MODP Group with 256-bit Prime Order Subgroup (RFC 5114)',
        g=int(
            "3FB32C9B" "73134D0B" "2E775066" "60EDBD48" "4CA7B18F" "21EF2054"
            "07F4793A" "1A0BA125" "10DBC150" "77BE463F" "FF4FED4A" "AC0BB555"
            "BE3A6C1B" "0C6B47B1" "BC3773BF" "7E8C6F62" "901228F8" "C28CBB18"
            "A55AE313" "41000A65" "0196F931" "C77A57F2" "DDF463E5" "E9EC144B"
            "777DE62A" "AAB8A862" "8AC376D2" "82D6ED38" "64E67982" "428EBC83"
            "1D14348F" "6F2F9193" "B5045AF2" "767164E1" "DFC967C1" "FB3F2E55"
            "A4BD1BFF" "E83B9C80" "D052B985" "D182EA0A" "DB2A3B73" "13D3FE14"
            "C8484B1E" "052588B9" "B7D2BBD2" "DF016199" "ECD06E15" "57CD0915"
            "B3353BBB" "64E0EC37" "7FD02837" "0DF92B52" "C7891428" "CDC67EB6"
            "184B523D" "1DB246C3" "2F630784" "90F00EF8" "D647D148" "D4795451"
            "5E2327CF" "EF98C582" "664B4C0F" "6CC41659",
            16
        ),
        p=int(
            "87A8E61D" "B4B6663C" "FFBBD19C" "65195999" "8CEEF608" "660DD0F2"
            "5D2CEED4" "435E3B00" "E00DF8F1" "D61957D4" "FAF7DF45" "61B2AA30"
            "16C3D911" "34096FAA" "3BF4296D" "830E9A7C" "209E0C64" "97517ABD"
            "5A8A9D30" "6BCF67ED" "91F9E672" "5B4758C0" "22E0B1EF" "4275BF7B"
            "6C5BFC11" "D45F9088" "B941F54E" "B1E59BB8" "BC39A0BF" "12307F5C"
            "4FDB70C5" "81B23F76" "B63ACAE1" "CAA6B790" "2D525267" "35488A0E"
            "F13C6D9A" "51BFA4AB" "3AD83477" "96524D8E" "F6A167B5" "A41825D9"
            "67E144E5" "14056425" "1CCACB83" "E6B486F6" "B3CA3F79" "71506026"
            "C0B857F6" "89962856" "DED4010A" "BD0BE621" "C3A3960A" "54E710C3"
            "75F26375" "D7014103" "A4B54330" "C198AF12" "6116D227" "6E11715F"
            "693877FA" "D7EF09CA" "DB094AE9" "1E1A1597",
            16
        )
    ),
)


def generate_private_key(size):
    '''
    Generate a private key of _size_ bits
    '''
    return getrandbits(size)


def generate_public_key(g, p, private_key):
    '''
    Generate the public key corresponding to a private one using a generator _g_
    and a prime _p_

    see https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
    '''
    return pow(g, private_key, p)


def check_public_key(p, public_key):
    '''
    Check a public key (DDH asumption) using a prime _p_

    see https://en.wikipedia.org/wiki/Decisional_Diffie%E2%80%93Hellman_assumption
    '''
    if (public_key > 2) and (public_key < p - 1):
        if pow(public_key, (p - 1) // 2, p) == 1:
            return True
    return False


def generate_shared_secret(p, private_key, other_public_key, check=True):
    '''
    Generate the shared secret following the Diffie-Hellman-Merkle key exchange

    see https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
    '''
    if check and not check_public_key(p, other_public_key):
        raise ValueError
    return pow(other_public_key, private_key, p)


# main program
if __name__ == "__main__":
    import sys
    from math import ceil

    if len(sys.argv) < 2:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    if sys.argv[1] == "list-groups":
        print(*["[{}] {}".format(i, g.desc) for i, g in enumerate(GROUPS)],
              sep='\n')

    elif sys.argv[1] == "genkeys":
        if len(sys.argv) < 4:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        dhgroup = GROUPS[int(sys.argv[2])]
        priv_key = generate_private_key(int(sys.argv[3]))
        pub_key = generate_public_key(dhgroup.g, dhgroup.p, priv_key)

        print(dhgroup.g, dhgroup.p, priv_key, pub_key)

    elif sys.argv[1] == "gensecret":
        if len(sys.argv) < 4:
            print(__doc__.format(sys.argv[0]), file=sys.stderr)
            sys.exit(1)

        with open(sys.argv[2]) as f:
            _, p, priv_key, _ = f.readline().split()

        with open(sys.argv[3]) as f:
            _, _, _, pub_key = f.readline().split()

        secret = generate_shared_secret(int(p), int(priv_key), int(pub_key))
        secret = secret.to_bytes(ceil(secret.bit_length() / 8), 'little')
        sys.stdout.buffer.write(secret)

    else:
        print(__doc__.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
