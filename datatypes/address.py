from .octetstring import OctetString
from .datatype import Type
from struct import pack, unpack
import ipaddress
from functools import reduce
import socket

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
    return 'IPv4'


class AdressValueError(ValueError):
    pass


def ipv4toInt(octets):
    result = 0
    for i, octet in zip(range(len(octets)-1, -1, -1), octets):
        result += pow(256, i) * int(octet)
    return result


def intToIpV4_2():
    octets = [192, 168, 0, 1]
    result = 0
    for octet in octets:
        result = 256


def intToIpv4(octets):
    return reduce(lambda x, y: x << 8 | y, octets)


def ipv4Address(addr):
    if isinstance(addr, str):
        octets = addr.split('.')
        if len(octets) != 4:
            raise AdressValueError("Invalid Ipv4")
        print(int.from_bytes(map(parse_octet, octets), 'big'))


def parse_octet(octetstr):
    return(int(octetstr, 10))


class Address(OctetString):

    def __init__(self, value):
        super().__init__(value)
        self._addrType = getNatureOfAdress(value)

    def encode(self):
        encoded = bytearray()
        encoded[0:] = addressFamily[self._addrType]['val']
        if self._addrType == 'IPv4':
            encoded[2:6] = socket.inet_pton(socket.AF_INET, self._value)
        elif self._addrType == 'IPv6':
            encoded[2:18] = socket.inet_pton(socket.AF_INET6, self._value)

        return encoded

    @staticmethod
    def decodeFromBuffer(self, buff):
        self._addrType = buff[:2]
        if self._addrType == addressFamily['IPv4']['val']:
            return Address(socket.inet_ntop(socket.AF_INET, buff[2:]))
        elif self._addrType == addressFamily['IPv6']['val']:
            return Address(socket.inet_ntop(socket.AF_INET6, buff[2:]))

    def __len__(self):
        return addressFamily[self._addrType]['len'] + 2

    def len(self):
        return self.__len__()
