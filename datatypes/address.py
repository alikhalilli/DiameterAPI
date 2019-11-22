from .octetstring import OctetString
from .datatype import Type
from struct import pack, unpack

addressFamily = {
    'Reserved': {'val': bytearray([0x00, 0x00]), 'len': 0},
    'IPv4': {'val': bytearray([0x00, 0x01]), 'len': 4},
    'IPv6': {'val': bytearray([0x00, 0x02]), 'len': 16}
}

"""
   Address
      The Address format is derived from the OctetString Basic AVP
      Format.  It is a discriminated union representing, for example, a
      32-bit (IPv4) [RFC0791] or 128-bit (IPv6) [RFC4291] address, most
      significant octet first.  The first two octets of the Address AVP
      represent the AddressType, which contains an Address Family,
      defined in [IANAADFAM].  The AddressType is used to discriminate
      the content and format of the remaining octets.
"""


def getNatureOfAdress(val):
    return 'ipv4'


class Adress(OctetString):

    def __init__(self, value):
        super().__init__(value)
        self._addrType = getNatureOfAdress(value)

    def encode(self):
        encoded = bytearray()
        encoded[0:] = addressFamily[self._addrType]['val']
        encoded[2:6] = None

    def decode(self):
        pass

    def __len__(self):
        return addressFamily[self._addrType]['len'] + 2

    def len(self):
        return self.__len__()
