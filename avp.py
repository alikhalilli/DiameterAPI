from struct import pack, pack_into, unpack
from binascii import hexlify, unhexlify
from datatypes.datatype import Type

from datatypes.integer32 import Integer32
from datatypes.integer64 import Integer64
from datatypes.float32 import Float32
from datatypes.float64 import Float64
from datatypes.octetstring import OctetString
from datatypes.diamidentity import DiameterIdentity
from datatypes.address import Address
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


avpflags = dict(
    vendor=1 << 7,  # 0b00000001 -> 0b10000000
    mandatory=1 << 6,
    protected=1 << 5)
#avpflags['vendor'] | avpflags['mandatory']


class AVP:
    def __init__(self, code=None, flags=None, vendorID=None, data=None):
        self._code = code
        self._flags = flags
        self._vendorID = vendorID
        self._data = data
        self._length = self._hlen + len(data)
        self._padding = data.getpadding()
        self._encoded = None

    def encode(self):
        encoded = bytearray()
        encoded[0:] = pack('>I', self._code)  # 0, 1, 2, 3
        encoded[4] = pack('>B', self._flags)  # 4
        encoded[5:] = int(self.length).to_bytes(3, byteorder='big')
        # pack('>I', self.length)[1:] if self.length <= 0xffffff else b'Error'  # 1:4 bytes = 3bytes ; 5, 6, 7
        if self._vendorID | (self.flags & avpflags['vendor']):
            encoded[8:] = pack('>I', self._vendorID)  # 8, 9, 10, 11
        encoded[self._hlen:] = self._data.encode()
        encoded[-1:] += pack(f">{self.padding}B",
                             *(0 for i in range(self._padding)))
        self._encoded = encoded
        return self._encoded

    def decodeToSelf(self, buff):
        if len(buff) < 8:
            raise ValueError("Not enough data to decode")
        self._code = unpack('>I', buff[:4])  # 0 1 2 3
        self._flags = unpack('>B', buff[4])  # 4
        # unpack('>I', b'\x00' + bytedata[5:8])
        self._length = int.from_bytes(buff[5:8], byteorder='big')  # 5 6 7
        if self._flags & avpflags['vendor']:
            self._vendor = unpack('>I', buff[8:12])  # 8 9 10 11
        self._data = (AVP.getType(self._code, self._vendor)).decode(buff[12:])
        return self

    @staticmethod
    def decodeFromBuffer(buff):
        a = AVP()
        a.code = unpack('>I', buff[:4])
        a.flags = unpack('>B', buff[4])
        # unpack('>I', b'\x00' + bytedata[5:8])
        a.length = int.from_bytes(buff[5:8], byteorder='big')
        a.vendorID = unpack('>I', buff[8:12])
        a.data = (AVP.getType(a.code, a.vendorID)).decode(buff[12:])
        return a

    @staticmethod
    def getType(avpcode, vendorID):
        return types["Integer"]

    @staticmethod
    def encodeFromAVP(avp):
        encoded = bytearray(avp.length)
        encoded[0:] = pack('>I', avp.code)  # 0, 1, 2, 3
        encoded[4:] = pack('>B', avp.flags)  # 4
        # 1:4 bytes = 3bytes ; 5, 6, 7
        encoded[5:] = int(avp.length).to_bytes(3, byteorder='big')
        #pack('>I', avp.length)[1:] if avp.length <= 0xffffff else b'Error'
        encoded[8:] = pack('>I', avp.vendorID)  # 8, 9, 10, 11
        encoded[12:] = avp.data.encode()
        encoded[-1:] += pack(f">{avp.data.getpadding()}B",
                             *(0 for i in range(avp.data.getpadding())))
        return encoded

    @staticmethod
    def newAVP(code, flags, vendorID=None, data=None):
        return AVP(code, flags, vendorID, data)

    def len(self):
        return self.__len__()

    def __len__(self):
        return self._length + self._data.getpadding()

    def _hlen(self):
        if self._vendor | (self._flags & avpflags['vendor']):
            return 12
        return 8

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
    def vendorID(self):
        return self._vendorID

    @vendorID.setter
    def vendorID(self, val):
        self._vendorID = val

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
