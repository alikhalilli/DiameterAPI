from .datatype import Type
from struct import pack, unpack
from binascii import hexlify, unhexlify
"""
  Time
      The Time format is derived from the OctetString AVP Base Format.
      The string MUST contain four octets, in the same format as the
      first four bytes are in the NTP timestamp format.  The NTP
      Timestamp format is defined in chapter 3 of [SNTP].

      This represents the number of seconds since 0h on 1 January 1900
      with respect to the Coordinated Universal Time (UTC).

      On 6h 28m 16s UTC, 7 February 2036 the time value will overflow.
      SNTP [SNTP] describes a procedure to extend the time to 2104.
      This procedure MUST be supported by all DIAMETER nodes.

"""


class Time(Type):

    def __init__(self, value):
        self._value = value
        self._timedelta = 2208988800

    def encode(self):
        # int(self._value + self._timedelta).to_bytes(4, order='big)
        encoded = pack('>I', self._value + self._timedelta)
        return encoded

    def len(self):
        return self.__len__()

    def decode(self):
        pass

    def decodeFromBytes(self, buff):
        decoded = unpack('>I', unhexlify(buff))[0]
        return decoded - self._timedelta

    def getpadding(self):
        return 0

    def __len__(self):
        return 4
