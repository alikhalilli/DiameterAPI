from datatypes.integer32 import Integer32
from datatypes.integer64 import Integer64
from datatypes.float32 import Float32
from datatypes.float64 import Float64
from datatypes.octetstring import OctetString
from datatypes.diamidentity import DiameterIdentity
from datatypes.address import Address
from datatypes.datatype import Type

types = {
    "Address": None,
    "DiameterIdentity": DiameterIdentity,
    "DiameterURI": None,
    "Enumerated": None,
    "Float32": Float32,
    "Float64": Float64,
    "Grouped": None,
    "IPFilterRule": None,
    "IPv4": None,
    "Integer32": Integer32,
    "Integer64": Integer64,
    "OctetString": OctetString,
    "QoSFilterRule": None,
    "Time": None,
    "UTF8String": None,
    "Unsigned32": None,
    "Unsigned64": None,
}
