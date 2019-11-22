from .octetstring import OctetString
from .datatype import Type

addressFamily = {
    'Reserved': {'val': [0x00, 0x00], 'len': 0},
    'IPv4': {'val': [0x00, 0x01], 'len': 4},
    'IPv6': {'val': [0x00, 0x02], 'len': 16}
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

    def encode(self):
        encoded = bytearray()


print(bytearray([0x00, 0x01]))
