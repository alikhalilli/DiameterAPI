from .address import Address
from .datatype import Type
from .decoder import decoders
from .diameteruri import DiameterURI
from .diamidentity import DiameterIdentity
from .dtime import Time
from .enumerated import Enumerated
from .float32 import Float32
from .float64 import Float64
from .grouped import Grouped
from .integer32 import Integer32
from .integer64 import Integer64
from .ipaddressV4 import IpAddressV4
from .ipaddressV6 import IpAddressV6
from .ipfilterrule import IPFilterRule
from .octetstring import OctetString
from .unsigned32 import Unsigned32
from .unsigned64 import Unsigned64
from .utf8string import UTF8String


types = {
    "Address": Address,
    "DiameterIdentity": DiameterIdentity,
    "DiameterURI": DiameterURI,
    "Enumerated": Enumerated,
    "Float32": Float32,
    "Float64": Float64,
    "Grouped": Grouped,
    "IPFilterRule": IPFilterRule,
    "IPAddress": Address,
    "Integer32": Integer32,
    "Integer64": Integer64,
    "OctetString": OctetString,
    "QoSFilterRule": None,
    "Time": Time,
    "UTF8String": UTF8String,
    "Unsigned32": Unsigned32,
    "Unsigned64": Unsigned64,
    "AppId": Unsigned32,
    "VendorId": Unsigned32
}
