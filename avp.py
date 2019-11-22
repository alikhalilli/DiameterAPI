from struct import pack, pack_into, unpack
from binascii import hexlify, unhexlify
from datatypes.integer32 import Integer32
from datatypes.integer64 import Integer64
from datatypes.float32 import Float32
from datatypes.float64 import Float64
from datatypes.octetstring import OctetString
from datatypes.diamidentity import DiameterIdentity
from collections import namedtuple
from datatypes.datatype import Type

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
  |    Data ...                                                   |
  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

  AVP Code => 32 bits = 4 bytes [0xffffffff]
  AVP Flags => 8 bits = 1 bytes [0xff]
  AVP Length => 24 bits = 3 bytes [0xffffff]
  AVP VendorID => 32 bits = 4 bytes [0xffffffff]

4 octets = 32 bytes
AVP_header_length = 12 bytes [4+1+3+4]
"""


types = {
    "Address": None,
    "DiameterIdentity": DiameterIdentity,
    "DiameterURI": None,
    "Enumerated": None,
    "Float32": Float32,
    "Float64": Float64,
    "Grouped": None,
    "IPFilterRule": None,
    "IPv4": None,
    "Integer32": Integer32,
    "Integer64": Integer64,
    "OctetString": OctetString,
    "QoSFilterRule": None,
    "Time": None,
    "UTF8String": None,
    "Unsigned32": None,
    "Unsigned64": None,
}

avpflags = dict(
    Vendor=1 << 7,  # 0b00000001
    Mandatory=1 << 6,
    Protected=1 << 5)


class AVP:
    def __init__(self, code=None, flags=None, vendor=None, data=None):
        self._code = code
        self._flags = flags
        self._vendor = vendor
        self._length = self.headerLength + data.len()
        self._data = data
        self._encoded = None
        self._padding = data.getpadding()

    @property
    def headerLength(self):
        if self._vendor:
            if (self._flags & avpflags['Vendor']):
                return 12
        return 8

    @staticmethod
    def newAVP(code, flags, vendor, data):
        return AVP(code, flags, vendor, data)

    def encode(self):
        encoded = bytearray()
        encoded[0:] = pack('>I', self.code)  # 0, 1, 2, 3
        encoded[4:] = pack('>B', self.flags)  # 4
        encoded[5:] = int(self.length).to_bytes(3, byteorder='big')
        # pack('>I', self.length)[1:] if self.length <= 0xffffff else b'Error'  # 1:4 bytes = 3bytes ; 5, 6, 7
        encoded[8:] = pack('>I', self.vendor)  # 8, 9, 10, 11
        encoded[12:] = self._data.encode()
        encoded[-1:] += pack(f">{self.padding}B",
                             *(0 for i in range(self.padding)))
        self._encoded = encoded
        return self._encoded

    @staticmethod
    def decodeFromBuffer(bytedata):
        a = AVP()
        a.code = unpack('>I', bytedata[0:4])
        a.flags = unpack('>B', bytedata[4])
        # unpack('>I', b'\x00' + bytedata[5:8])
        a.length = int.from_bytes(bytedata[5:8], byteorder='big')
        a.vendor = unpack('>I', bytedata[8:12])
        a.data = (AVP.getType(a.code, a.vendor)).decode(bytedata[12:])
        return AVP

    @staticmethod
    def getType(avpcode, avpvendor):
        return types["Integer"]

    @staticmethod
    def encodeFromObj(avp, application):
        encoded = bytearray(avp.length)
        encoded[0:] = pack('>I', avp.code)  # 0, 1, 2, 3
        encoded[4:] = pack('>B', avp.flags)  # 4
        # 1:4 bytes = 3bytes ; 5, 6, 7
        encoded[5:] = pack('>I', avp.length)[
            1:] if avp.length <= 0xffffff else b'Error'
        encoded[8:] = pack('>I', avp.vendor)  # 8, 9, 10, 11
        encoded[12:] = avp.data.encode()
        encoded[-1:] += pack(f">{avp.data.getPaddingC()}B",
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
        return f"""
        --------------------------------------
        AVP:
        Code: {self.code}
        Flags: {self.flags}
        Length: {self.length}
        VendorID: {self.vendor}
        Data: {self.data},
        Whole AVP Encoded: {self.encode()}
        --------------------------------------"""


if __name__ == "__main__":

    a = AVP(231,
            flags=avpflags['Vendor'] | avpflags['Mandatory'],
            vendor=22,
            data=Integer32(12))
    b = AVP(232,
            flags=avpflags['Mandatory'],
            vendor=333,
            data=Integer32(333))
    c = Integer32.decodeFromBytes(b'\x00\x00\x00\x0c')
    d = AVP(233,
            flags=avpflags['Vendor'],
            vendor=77,
            data=OctetString("Salam"))
    di = AVP(234,
             flags=avpflags['Vendor'],
             vendor=78,
             data=DiameterIdentity("aaa://host.example.com:6666;transport=tcp;protocol=diameter"))
    print(f"data: {a}")
    print(f"decoded: {c}")
    print(d)
    print(di)
    # print(b)
