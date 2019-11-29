import struct


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
"""


class AVPHeader:
    def __init__(self, code, flags, vendor):
        self._code = code
        self._flags = flags
        self._vendor = vendor
        self._length = None
        self._encoded = None

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, val):
        self._length = val

    def encode(self):
        encoded = bytearray()
        encoded[0]

    def decode(self):
        pass

    def __repr__(self):
        return f"AVPHeader: Code: {self._code}, Flags: {self._flags}, Vendor: {self._vendor}"
