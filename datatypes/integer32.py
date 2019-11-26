from struct import pack, unpack
from binascii import hexlify, unhexlify
from datatypes.datatype import Type

"""
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                           AVP Code                            |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |V M P r r r r r|                  AVP Length                   |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |                        Vendor-ID (opt)                        |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
  |    Data ...
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

  AVP Code => 32 bits = 4 bytes [0xffffffff]
  AVP Flags => 8 bits = 1 bytes [0xff]
  AVP Length => 24 bits = 3 bytes [0xffffff]
  AVP VendorID => 32 bits = 4 bytes [0xffffffff]

4 octets = 32 bytes
AVP_header_length = 12 bytes [4+1+3+4]
"""


class Integer32(Type):
    def __init__(self, value):
        super().__init__(value)

    def encode(self):
        # Integer32 => 4 bytes
        return pack('>I', self._value)

    def decode(self):
        # Integer32 => 4 bytes
        return unpack('>I', unhexlify(self.value))

    def len(self):
        return 4

    def getpadding(self):
        return 0

    @staticmethod
    def decodeFromBytes(buf):
        # return unpack('>I', buf)
        return int.from_bytes(buf, byteorder='big')


print(Integer32(32444).encode())
print(Integer32.decodeFromBytes(b'\x00\x00~\xbc'))
print(len(b'\x00\x00~\xbc'))
""" @staticmethod
    def getAVPLen(vFlag=False):
        # The AVP Length fieldc MUST be set to 12 (16 if the 'V' bit is enabled)
        # len(AVPCode) + len(AVPFlags) + len(AVPLength) + len(AVPVendorID) + len(Int32)
        # 4 + 1 + 3 + [4] + 4 = 12 + [4]
        return 12 if vFlag else 16"""
