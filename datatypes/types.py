import datatypes.address as address
import datatypes.diamidentity as diamidentity
import datatypes.diameteruri as diameteruri
import datatypes.enumerated as enumerated
import datatypes.float32 as float32
import datatypes.float64 as float64
import datatypes.ipfilterrule as ipfilterrule
import datatypes.integer32 as integer32
import datatypes.integer64 as integer64
import datatypes.utf8string as utf8string
import datatypes.unsigned32 as unsigned32
import datatypes.unsigned64 as unsigned64
import datatypes.octetstring as octetstring
import datatypes.dtime as dtime
import datatypes.grouped as grouped

types = {
    "Address": address.Address,
    "DiameterIdentity": diamidentity.DiameterIdentity,
    "DiameterURI": diameteruri.DiameterURI,
    "Enumerated": enumerated.Enumerated,
    "Float32": float32.Float32,
    "Float64": float64.Float64,
    "Grouped": grouped.Grouped,
    "IPFilterRule": ipfilterrule.IPFilterRule,
    "IPAddress": address.Address,
    "Integer32": integer32.Integer32,
    "Integer64": integer64.Integer64,
    "OctetString": octetstring.OctetString,
    "QoSFilterRule": None,
    "Time": dtime.Time,
    "UTF8String": utf8string.UTF8String,
    "Unsigned32": unsigned32.Unsigned32,
    "Unsigned64": unsigned64.Unsigned64,
    "AppId": unsigned32.Unsigned32,
    "VendorId": unsigned32.Unsigned32
}
