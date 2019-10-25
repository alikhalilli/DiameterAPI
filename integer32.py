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
AVP_header_length = 12 bytes [4+1+3+4]
"""


class Integer32:
    def __init__(self, val):
        self._value = val

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    def decode(self):
        # Integer32 => 4 bytes
        return struct.unpack('>I', unhexlify(self._value))

    def encode(self):
        # Integer32 => 4 bytes
        return struct.pack('>I', self._value)

    @staticmethod
    def getLength(self=None):
        return 4

    @staticmethod
    def getPaddingC(self=None):
        return 0

    def __repr__(self):
        return f"""Int32_Value: {self.value}
        Int32_Length: {self.getLength()}
        Int32_Padding: {self.getPaddingC()}
        Int32_Encoded: {self.encode()}"""


""" @staticmethod

    def getAVPLen(vFlag=False):
        # The AVP Length fieldc MUST be set to 12 (16 if the 'V' bit is enabled)
        # len(AVPCode) + len(AVPFlags) + len(AVPLength) + len(AVPVendorID) + len(Int32)
        # 4 + 1 + 3 + [4] + 4 = 12 + [4]
        return 12 if vFlag else 16"""
