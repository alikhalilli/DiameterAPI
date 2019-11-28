from datatypes.enumerated import Enumerated
from datatypes.time import Time
from datatypes.utf8string import UTF8String
from datatypes.ipfilterrule import IPFilterRule
from datatypes.ipaddressV4 import IpAddressV4
from datatypes.ipaddressV6 import IpAddressV6
from datatypes.unsigned32 import Unsigned32
from datatypes.unsigned64 import Unsigned64
from datatypes.diameteruri import DiameterURI
from datatypes.group import Group
from datatypes.integer32 import Integer32
from datatypes.integer64 import Integer64
from datatypes.float32 import Float32
from datatypes.float64 import Float64
from datatypes.octetstring import OctetString
from datatypes.diamidentity import DiameterIdentity
from datatypes.address import Address
from datatypes.datatype import Type

types = {
    "Address": Address,
    "DiameterIdentity": DiameterIdentity,
    "DiameterURI": DiameterURI,
    "Enumerated": Enumerated,
    "Float32": Float32,
    "Float64": Float64,
    "Grouped": Group,
    "IPFilterRule": IPFilterRule,
    "IPAddress": IpAddressV4,
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


def findType(avpcode=None, avpname=None, vendorid=None):
    pass
