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

decoders = {
    "Address": address.Address.decodeFromBuffer,
    "DiameterIdentity": diamidentity.DiameterIdentity.decodeFromBuffer,
    "DiameterURI": diameteruri.DiameterURI.decodeFromBuffer,
    "Enumerated": enumerated.Enumerated.decodeFromBuffer,
    "Float32": float32.Float32.decodeFromBuffer,
    "Float64": float64.Float64.decodeFromBuffer,
    "Grouped": grouped.Grouped.decodeFromBuffer,
    "IPFilterRule": ipfilterrule.IPFilterRule.decodeFromBuffer,
    "IPAddress": address.Address.decodeFromBuffer,
    "Integer32": integer32.Integer32.decodeFromBuffer,
    "Integer64": integer64.Integer64.decodeFromBuffer,
    "OctetString": octetstring.OctetString.decodeFromBuffer,
    "QoSFilterRule": None,
    "Time": dtime.Time.decodeFromBuffer,
    "UTF8String": utf8string.UTF8String.decodeFromBuffer,
    "Unsigned32": unsigned32.Unsigned32.decodeFromBuffer,
    "Unsigned64": unsigned64.Unsigned64.decodeFromBuffer,
    "AppId": unsigned32.Unsigned32.decodeFromBuffer,
    "VendorId": unsigned32.Unsigned32.decodeFromBuffer
}
