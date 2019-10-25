import struct
from binascii import hexlify, unhexlify
from integer32 import Integer32

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
        self._vendor = vendor
        self._length = self.headerLength + data.getLength()
        print(self._length)
        self._data = data
        self._padding = data.getPaddingC()

    @property
    def headerLength(self):
        if self.vendor:
            if (self.flags & avpflags['Vendor']):
                return 12
        return 8

    @staticmethod
    def newAVP(code, flags, vendor, data):
        return AVP(code, flags, vendor, data)

    def encode(self):
        encoded = bytearray()
        encoded[0:] = struct.pack('>I', self.code)  # 0, 1, 2, 3
        encoded[4:] = struct.pack('>B', self.flags)  # 4
        encoded[5:] = struct.pack('>I', self.length)[
            1:] if self.length <= 0xffffff else b'Error'  # 1:4 bytes = 3bytes ; 5, 6, 7
        encoded[8:] = struct.pack('>I', self.vendor)  # 8, 9, 10, 11
        encoded[12:] = self._data.encode()
        encoded[-1:] += struct.pack(f">{self.padding}B",
                                    *(0 for i in range(self.padding)))
        self._encoded = encoded
        return self._encoded

    @staticmethod
    def decodeAVP(bytedata, application):
        a = AVP()
        a.code = struct.unpack('>I', bytedata[0:4])
        a.flags = struct.unpack('>B', bytedata[4])
        a.length = struct.unpack('>I', b'\x00' + bytedata[5:8])
        a.vendor = struct.unpack('>I', bytedata[8:12])
        a.data = bytedata[12:]
        return AVP

    @staticmethod
    def encodeAVP(avp, application):
        encoded = bytearray(avp.length)
        encoded[0:] = struct.pack_into('>I', encoded, avp.code)  # 0, 1, 2, 3
        encoded[4:] = struct.pack('>B', avp.flags)  # 4
        encoded[5:] = struct.pack('>I', avp.length)[
            1:] if avp.length <= 0xffffff else b'Error'  # 1:4 bytes = 3bytes ; 5, 6, 7
        encoded[8:] = struct.pack('>I', avp.vendor)  # 8, 9, 10, 11
        encoded[12:] = avp.data.encode()
        encoded[-1:] += struct.pack(f">{avp.data.getPaddingC()}B",
                                    *(0 for i in range(avp.data.getPaddingC())))
        return encoded

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

    @property
    def padding(self):
        return self._padding

    @property
    def encoded(self):
        return self._encoded

    def __repr__(self):
        return f"""Code: {self.code}
        Flags: {self.flags}
        Length: {self.length}
        VendorID: {self.vendor}
        Data: {self.data},
        Whole AVP Encoded: {self.encode()}"""


if __name__ == "__main__":
    a = AVP(231, avpflags['Vendor'], vendor=22, data=Integer32(12))
    b = AVP(232, flags=0x000000, vendor=333, data=Integer32(333))
    print(a)
    print(b)
