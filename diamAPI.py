import struct
import codecs
import socket
import sys
import logging
import time
import string
from static import avpDict, commandDict, vendorDict
from .types.calcpad import get_paddingc

"""
Package Header Flags:
+-+-+-+-+-+-+-+-+
|R|P|E|T|r|r|r|r|
+-+-+-+-+-+-+-+-+

10000000 1<<7 0x80
01000000 1<<6 0x40
00100000 1<<5 0x20
00010000 1<<4 0x10

AVP Header Flags:
+-+-+-+-+-+-+-+-+
|V|M|P|r|r|r|r|r|
+-+-+-+-+-+-+-+-+

10000000 1<<7 0x80
01000000 1<<6 0x40
00100000 1<<5 0x20
"""

flags = dict(
    Request=1 << 7,
    Proxiable=1 << 6,
    Error=1 << 5,
    Retransmitted=1 << 4,
    VendorSpecific=1 << 7,
    Mandatory=1 << 6,
    Protected=1 << 5)

statics = dict(
    diam_header_length=20,
    avp_header_length=12
)

"""
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |    Version    |                 Message Length                |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 | Command Flags |                  Command Code                 |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                         Application-ID                        |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                      Hop-by-Hop Identifier                    |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
 |                      End-to-End Identifier                    |
 +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

4 Octets = 4 * 8 bits = 32 bytes

Version => 8 bits
MessageLength => 24 bits = 3 bytes
CommandFlags => 8 bits
CommandCode => 24 bits = 3 bytes
Application-ID => 32 bits = 4 bytes
Hop-By-Hop Identifier => 32 bits = 4 bytes
End-to-End Identifier => 32 bits = 4 bytes
"""

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


class DiameterHeader:
    def __init__(self, *args, **kwargs):
        self.version = 1
        self.msglength = 0
        self.commandflags = 0
        self.commandcode = 0
        self.applicationID = 0
        self.hopbyhopID = 0
        self.endtoendID = 0


class AVP:
    def __init__(self, name, val, flags=None):
        self._AVPcode = AVPRepo.getCodeByName(name)
        self._AVPname = name
        self._flags = flags
        self._AVPlength = 0
        #self.vendorID = Vendor.getCodeById(AVPRepo.getVendorIdByName(name))
        self._data = ''
        self._val = val
        self._type = AVPRepo.getTypeByName(name)

    @property
    def AVPcode(self):
        return self._AVPcode

    @property
    def AVPname(self):
        return self._AVPname

    @property
    def flags(self):
        return self._flags

    @property
    def datatype(self):
        return self._type

    @property
    def val(self):
        return self._val

    @flags.setter
    def flags(self, val):
        self._flags = val

    def encode(self):
        if isinstance(self.val, list):
            avpsequence = ''
            for aval in self.val:
                avpsequence += (aval + get_paddingc(len(aval)/2) * '00')

        self._data = AVPRepo.getAllDetailsByName(self.AVPname)
        encoded, m = globals()[self.datatype].encode(self.val)
        self._AVPlength = m + len(encoded)/2
        return encoded, m

    def __repr__(self):
        return f"""AVPname: {self.AVPname}
        AVPCode: {self.AVPcode}
        AVPval: {self.val}
        AVPType: {self.datatype}"""


class AVPRepo:
    """
    'code': '60',
    'mandatory': 'must',
    'mayencrypt': 'yes',
    'protected': 'may',
    'vendorbit': 'mustnot',
    'vendorid': '',
    'typename': 'OctetString'
    """
    @staticmethod
    def getAllDetailsByName(name):
        return avpDict[name]

    @staticmethod
    def getCodeByName(name):
        try:
            return avpDict[name]['code']
        except KeyError:
            print('AVP Not Found')

    @staticmethod
    def getNameByCode(code):
        for k, v in avpDict.items():
            if v['code'] == code:
                return k

    @staticmethod
    def getMandatoryByName(name):
        return avpDict[name]['mandatory']

    @staticmethod
    def getMayEncryptByName(name):
        return avpDict[name]['mayencrypt']

    @staticmethod
    def getProtectedByName(name):
        return avpDict[name]['protected']

    @staticmethod
    def getVendorBitByName(name):
        return avpDict[name]['vendorbit']

    @staticmethod
    def getVendorIdByName(name):
        return '0' if avpDict[name]['vendorid'] == "" else avpDict[name]['vendorid']

    @staticmethod
    def getTypeByName(name):
        try:
            return avpDict[name]['typename']
        except KeyError:
            print("AVP Not Found")

    @staticmethod
    def isEnum(name):
        return AVPRepo.getTypeByName == 'Enumerated'


print(AVPRepo.getCodeByName('Management-Policy-Id'))





"""
0x00000001
0x
"""

print(AVP("Origin-Hos", b"pcrf.myrealm.example"))
print(AVP("Origin-Host", b"pcrf.myrealm.example").encode())
