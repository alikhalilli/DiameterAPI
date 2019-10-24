import struct
from binascii import hexlify, unhexlify
from calcpad import get_paddingc
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


class OctetString:
    @staticmethod
    def decode(val):
        # Size is dynamic
        return struct.unpack(f'>{len(val)//2}s', unhexlify(val))[0]

    @staticmethod
    def encode(val):
        # Size is dynamic
        return hexlify(struct.pack(f'>{len(val)}s', val.encode('utf-8'))).decode('utf-8')

    @staticmethod
    def getAVPLen(val, vFlag=False):
        # The AVP Length fieldc MUST be set to 12 (16 if the 'V' bit is enabled)
        # len(AVPCode) + len(AVPFlags) + len(AVPLength) + len(AVPVendorID) + len(Int32)
        # 4 + 1 + 3 + [4] + 8 = 16 + [4]
        data = hexlify(struct.pack(
            f'>{len(val)}s', val.encode('utf-8'))).decode('utf-8')
        return 12 + len(data)/2 if vFlag else 8 + len(data)/2

    @staticmethod
    def getPaddingC(val):
        n = len(val)
        return get_paddingc(n) - n
