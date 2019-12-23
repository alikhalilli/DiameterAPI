import struct
import datatypes.decoder as decoder
from datatypes import decoder
from AVPRepo import AVPTools
from datatypes import Grouped
from headerflags import AVPFlags

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
        self._length = self._hlen() + len(data)
        self._padding = data.getpadding()
        self._encoded = None

    def encode(self):
        encoded = bytearray()
        encoded[0:] = struct.pack('>I', self._code)  # 0, 1, 2, 3
        encoded[4:] = struct.pack('>B', self._flags)  # 4
        encoded[5:] = int(self.length).to_bytes(3, byteorder='big')
        # pack('>I', self.length)[1:] if self.length <= 0xffffff else b'Error'  # 1:4 bytes = 3bytes ; 5, 6, 7
        if (self._vendorID is not None):
            encoded[8:] = struct.pack('>I', self._vendorID)  # 8, 9, 10, 11
        encoded[self._hlen():] = self._data.encode()
        encoded[-1:] += struct.pack(f">{self.padding}B",
                                    *(0 for i in range(self._padding)))
        self._encoded = encoded
        return self._encoded

    def decodeToSelf(self, buff):
        if len(buff) < 8:
            raise ValueError("Not enough data to decode")
        self._code = struct.unpack('>I', buff[:4])  # 0 1 2 3
        self._flags = struct.unpack('>B', buff[4])  # 4
        # unpack('>I', b'\x00' + bytedata[5:8])
        self._length = int.from_bytes(buff[5:8], byteorder='big')  # 5 6 7
        if self._flags & AVPFlags.VENDORSPECIFIC.value:
            self._vendorID = struct.unpack('>I', buff[8:12])  # 8 9 10 11
        self._data = (AVP.getType(self._code, self._vendorID)
                      ).decodeFromBuffer(buff[12:])
        return self

    @staticmethod
    def decodeFromBuffer(buff):
        a_code = struct.unpack('>I', buff[0:4])[0]
        a_flags = struct.unpack('>B', buff[4:5])[0]
        a_length = int.from_bytes(buff[5:8], byteorder='big')
        a_vendorID = None
        a_hdrlen = 8
        if a_flags & AVPFlags.VENDORSPECIFIC.value:
            a_vendorID = struct.unpack('>I', buff[8:12])[0]
            a_hdrlen += 4
        a_data = AVP.decodeBuff(a_code)(buff[a_hdrlen:a_length])
        if isinstance(a_data, Grouped):
            from groupedAVP import GroupedAVP
            a_data = GroupedAVP.decodeFromBuffer(a_data)
        return AVP(
            code=a_code,
            flags=a_flags,
            vendorID=a_vendorID,
            data=a_data
        )

    @staticmethod
    def decodeBuff(avpcode, vendorID=None):
        return decoder.decoders[AVP.getType(avpcode, vendorID)]

    @staticmethod
    def getType(avpcode, vendorID=None):
        return AVPTools.getTypeByCode(avpcode)

    @staticmethod
    def encodeFromAVP(avp):
        encoded = bytearray(avp.length)
        encoded[0:] = struct.pack('>I', avp.code)  # 0, 1, 2, 3
        encoded[4:] = struct.pack('>B', avp.flags)  # 4
        # 1:4 bytes = 3bytes ; 5, 6, 7
        encoded[5:] = int(avp.length).to_bytes(3, byteorder='big')
        #pack('>I', avp.length)[1:] if avp.length <= 0xffffff else b'Error'
        encoded[8:] = struct.pack('>I', avp.vendorID)  # 8, 9, 10, 11
        encoded[12:] = avp.data.encode()
        encoded[-1:] += struct.pack(f">{avp.data.getpadding()}B",
                                    *(0 for i in range(avp.data.getpadding())))
        return encoded

    @staticmethod
    def newAVP(code, flags, vendorID=None, data=None):
        return AVP(code, flags, vendorID, data)

    def len(self):
        return self.__len__()

    def __len__(self):
        return self._length + self._padding

    def _hlen(self):
        if self._vendorID:
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
        Code: {self._code}
        Flags: {self._flags}
        LengthOnMsg: {self._length}
        WholeLength: {self.__len__()}
        VendorID: {self._vendorID}
        Data: {self._data},
        Whole AVP Encoded: {self._encoded}
        --------------------------------------"""
