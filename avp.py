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
  +-+-+-+-+-+-+-+-+

  AVP Code => 32 bits = 4 bytes [0xffffffff]
  AVP Flags => 8 bits = 1 bytes [0xff]
  AVP Length => 24 bits = 3 bytes [0xffffff]
  AVP VendorID => 32 bits = 4 bytes [0xffffffff]

4 octets = 32 bytes
AVP_header_length = 12 bytes [4+1+3+4]
"""

avpflags = dict(
    Vendor=1 << 7,
    Mandatory=1 << 6,
    Protected=1 << 5)


class AVP:
    def __init__(self, code=None, flags=None, vendor=None, data=None):
        self._code = code
        self._flags = flags
        self._length = self.headerLength + data.len()
        self._vendor = vendor
        self._data = data

    @property
    def headerLength(self):
        if self.vendor and (self.flags & avpflags['Vendor']):
            return 12
        return 8

    @staticmethod
    def newAVP(code, flags, vendor, data):
        return AVP(code, flags, vendor, data)

    @staticmethod
    def decode(data, application):
        a = AVP()
        a.vendor = 'vendor'
        return AVP

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, val):
        self._code = val

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, val):
        self._flags = val

    @property
    def vendor(self):
        return self._vendor

    @vendor.setter
    def vendor(self, val):
        self._vendor = val

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, val):
        self._data = val

    @property
    def length(self):
        return self._length

    def __repr__(self):
        return f"""Code: {self.code}
        Flags: {self.flags}
        Length: {self.length}
        VendorID: {self.vendor}
        Data: {self.data}"""
