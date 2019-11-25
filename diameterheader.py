from struct import pack, unpack
from binascii import hexlify, unhexlify


"""
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |    Version    |                 Message Length                |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 | Command Flags |                  Command Code                 |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                         Application-ID                        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                      Hop-by-Hop Identifier                    |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                      End-to-End Identifier                    |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

4 Octets = 4 * 8 bits = 32 bytes

Version => 8 bits
MessageLength => 24 bits = 3 bytes
CommandFlags => 8 bits
CommandCode => 24 bits = 3 bytes
Application-ID => 32 bits = 4 bytes
Hop-By-Hop Identifier => 32 bits = 4 bytes
End-to-End Identifier => 32 bits = 4 bytes
"""


class Header:
    def __init__(self,
                 version,
                 msglength,
                 cmdflags,
                 cmdcode,
                 appId,
                 hopByHopId,
                 endToEndId):
        self._version = version
        self._msglength = msglength
        self._headerlength = 20
        self._cmdflags = cmdflags
        self._cmdcode = cmdcode
        self._appId = appId
        self._hopByhopId = hopByHopId
        self._endToEndId = endToEndId

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, val):
        self._version = val

    @staticmethod
    def getLength():
        return 20

    def encode(self):
        encoded = bytearray()
        encoded[0:] = pack('>B', self._version)
        encoded[1:] = int(self._msglength).to_bytes(3, byteorder='big')
        encoded[5:] = pack('>B',  self._cmdflags)
        encoded[6:] = int(self._cmdcode).to_bytes(3, byteorder='big')
        encoded[9:] = pack('>I', self._appId)
        encoded[13:] = pack('>I', self._hopByhopId)
        encoded[17:] = pack('>I', self._endToEndId)
        return encoded

    def decode(self, buff):
        if len(buff)/2 < self._headerlength:
            raise ValueError(f"Corrupted data {buff}")
        return Header(
            version=unpack('>B', buff[0]),
            msglength=unpack('>I', b'\x00' + buff[1:4]),
            cmdflags=unpack('>B', buff[4]),
            cmdcode=unpack('>I', b'\x00' + buff[5:8]),
            appId=unpack('>I', buff[8:12]),
            hopByHopId=unpack('>I', buff[12:16]),
            endToEndId=unpack('>I', buff[16:20])
        )
