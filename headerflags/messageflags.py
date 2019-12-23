from enum import IntEnum


class MessageFlags(IntEnum):
    REQUEST = 1 << 7,
    PROXIABLE = 1 << 6,
    ERROR = 1 << 5,
    RETRANSMITTED = 1 << 4
