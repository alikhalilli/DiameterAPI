import struct
from binascii import hexlify, unhexlify


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


class Float64:
    @staticmethod
    def decode(val):
        # Float64 => 8 bytes
        # d - double
        return struct.unpack('>d', unhexlify(val))

    @staticmethod
    def encode(val):
        # Float32 => 8 bytes
        # d - double
        return hexlify(struct.pack('>d', val.encode('utf-8'))).decode('utf-8')

    @staticmethod
    def getAVPLen(vFlag=False):
        # len(AVPCode) + len(AVPFlags) + len(AVPLength) + len(AVPVendorID) + len(Float64)
        # 4 + 1 + 3 + [4] + 4 = 12 + [8]
        return 16 if vFlag else 20

    @staticmethod
    def getTypeLen():
        return 8

    @staticmethod
    def getPaddingC():
        return 0