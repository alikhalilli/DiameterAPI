from struct import pack, unpack
from binascii import hexlify, unhexlify
import random

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
        self._headerlength = 20
        self._msglength = self._headerlength
        self._cmdflags = cmdflags
        self._cmdcode = cmdcode
        self._appId = appId
        self._hopByhopId = random.getrandbits(32)
        self._endToEndId = random.getrandbits(32)

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, val):
        self._version = val

    @staticmethod
    def getLength():
        return self._msglength

    def encode(self):
        encoded = bytearray()
        encoded[0:] = pack('>B', self._version)
        encoded[1:] = int(self._msglength).to_bytes(3, byteorder='big')
        encoded[4:] = pack('>B',  self._cmdflags)
        encoded[5:] = int(self._cmdcode).to_bytes(3, byteorder='big')
        encoded[8:] = pack('>I', self._appId)
        encoded[12:] = pack('>I', self._hopByhopId)
        encoded[16:] = pack('>I', self._endToEndId)
        return encoded

    def decode(self, buff):
        if len(buff) < self._headerlength:
            raise ValueError(f"Corrupted data {buff}")
        return Header(
            version=unpack('>B', buff[0])[0],
            msglength=int.from_bytes(buff[1:4], byteorder='big'),
            cmdflags=unpack('>B', buff[4])[0],
            cmdcode=int.from_bytes(buff[5:8], byteorder='big'),
            appId=unpack('>I', buff[8:12])[0],
            hopByHopId=unpack('>I', buff[12:16])[0],
            endToEndId=unpack('>I', buff[16:20])[0]
        )
