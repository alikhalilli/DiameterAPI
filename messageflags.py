from enum import Enum


class MessageFlags(Enum):
    Request = 1 << 7,
    Proxiable = 1 << 6,
    Error = 1 << 5,
    Retransmitted = 1 << 4,
    VendorSpecific = 1 << 7,
    Mandatory = 1 << 6,
    Protected = 1 << 5
