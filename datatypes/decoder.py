#from .address import Address
from .address import Address
from .diamidentity import DiameterIdentity
from .diameteruri import DiameterURI
from .enumerated import Enumerated
from .float32 import Float32
from .float64 import Float64
from .grouped import Grouped
from .ipfilterrule import IPFilterRule
from .address import Address
from .integer32 import Integer32
from .integer64 import Integer64
from .octetstring import OctetString
from .dtime import Time
from .utf8string import UTF8String
from .unsigned32 import Unsigned32
from .unsigned64 import Unsigned64

decoders = {
    "Address": Address.decodeFromBuffer,
    "DiameterIdentity": DiameterIdentity.decodeFromBuffer,
    "DiameterURI": DiameterURI.decodeFromBuffer,
    "Enumerated": Enumerated.decodeFromBuffer,
    "Float32": Float32.decodeFromBuffer,
    "Float64": Float64.decodeFromBuffer,
    "Grouped": Grouped.decodeFromBuffer,
    "IPFilterRule": IPFilterRule.decodeFromBuffer,
    "IPAddress": Address.decodeFromBuffer,
    "Integer32": Integer32.decodeFromBuffer,
    "Integer64": Integer64.decodeFromBuffer,
    "OctetString": OctetString.decodeFromBuffer,
    "QoSFilterRule": None,
    "Time": Time.decodeFromBuffer,
    "UTF8String": UTF8String.decodeFromBuffer,
    "Unsigned32": Unsigned32.decodeFromBuffer,
    "Unsigned64": Unsigned64.decodeFromBuffer,
    "AppId": Unsigned32.decodeFromBuffer,
    "VendorId": Unsigned32.decodeFromBuffer
}
