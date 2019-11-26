from datatypes.enumerated import Enumerated
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
    "DiameterURI": None,
    "Enumerated": Enumerated,
    "Float32": Float32,
    "Float64": Float64,
    "Grouped": Group,
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


def findType(avpcode=None, avpname=None, vendorid=None):
    pass
