import struct
from binascii import hexlify, unhexlify
from datatype import Type


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
AVP_header_length = 8 or 12 bytes [4+1+3+(4)]
"""


class Float64(Type):

    def __init__(self, val, vFlag=False):
        self._val = val
        self._vFlag = vFlag

    def decode(self):
        # Float64 => 8 bytes
        # d - double
        return struct.unpack('>d', unhexlify(self._val))

    def encode(self):
        # Float32 => 8 bytes
        # d - double
        return hexlify(struct.pack('>d', self._val.encode('utf-8'))).decode('utf-8')

    def getAVPLen(self):
        # len(AVPCode) + len(AVPFlags) + len(AVPLength) + len(AVPVendorID) + len(Float64)
        # 4 + 1 + 3 + [4] + 4 = 12 + [8]
        return 16 if self._vFlag else 20

    @staticmethod
    def getTypeLen():
        return 8

    def getPaddingC(self):
        return 0
