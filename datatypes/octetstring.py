import struct
from .datatype import Type
import datatypes.calcpad as calcpad
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
        return struct.pack(f'>{len(self._value)}s', self._value.encode('utf-8'))

    def decode(self):
        # Size is dynamic
        return struct.unpack(f'>{len(self._value)//2}s', self._value)

    def len(self):
        return self.__len__()

    def __len__(self):
        return len(self._value)

    def getpadding(self):
        return calcpad.new_calc_padding(self.len()) - self.len()

    @staticmethod
    def decodeFromBuffer(buff):
        return OctetString(struct.unpack(f'>{len(buff)}s', buff)[0])
