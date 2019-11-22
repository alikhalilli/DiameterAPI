from struct import pack, unpack
from binascii import hexlify, unhexlify
from .datatype import Type
from .calcpad import get_paddingc
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


class OctetString(Type):

    def __init__(self, value):
        super().__init__(value)

    def encode(self):
        # Size is dynamic
        return pack(f'>{len(self._value)}s', self._value.encode('utf-8'))

    def decode(self):
        # Size is dynamic
        return unpack(f'>{len(self._value)//2}s', unhexlify(self._value))

    def len(self):
        return self.__len__()

    def __len__(self):
        return len(self._value)

    def getpadding(self):
        return get_paddingc(self.len()) - self.len()

    @staticmethod
    def decodeFromBytes(buf):
        return unpack(f'>{len(buf)}s', buf)


"""    @staticmethod
    def getAVPLen(val, vFlag=False):
        # The AVP Length fieldc MUST be set to 12 (16 if the 'V' bit is enabled)
        # len(AVPCode) + len(AVPFlags) + len(AVPLength) + len(AVPVendorID) + len(Int32)
        # 4 + 1 + 3 + [4] + 8 = 16 + [4]
        data = hexlify(struct.pack(
            f'>{len(val)}s', val.encode('utf-8'))).decode('utf-8')
        return 12 + len(data)/2 if vFlag else 8 + len(data)/2"""

"""    @staticmethod
    def getPaddingC(val):
        n = len(val)
        return get_paddingc(n) - n"""
