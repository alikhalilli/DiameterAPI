from enum import IntEnum

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


class AVPFlags(IntEnum):
    VENDORSPECIFIC = 1 << 7,  # 0b00000001 -> 0b10000000
    MANDATORY = 1 << 6,
    PROTECTED = 1 << 5
