import struct
import datatypes.datatype as datatype

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


class Integer32(datatype.Type):
    def __init__(self, value):
        super().__init__(value)

    def encode(self):
        # Integer32 => 4 bytes
        return struct.pack('>I', self._value)

    def decode(self):
        # Integer32 => 4 bytes
        return struct.unpack('>I', self.value)

    def len(self):
        return self.__len__()

    def __len__(self):
        return 4

    def getpadding(self):
        return 0

    @staticmethod
    def decodeFromBuffer(buff):
        # return unpack('>I', buf)
        return Integer32(int.from_bytes(buff, byteorder='big'))
