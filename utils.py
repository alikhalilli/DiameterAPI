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
from grouped import GroupedAVP
from datatypes.integer32 import Integer32
from datatypes.integer64 import Integer64
from datatypes.float32 import Float32
from datatypes.float64 import Float64
from datatypes.octetstring import OctetString
from datatypes.diamidentity import DiameterIdentity
from datatypes.address import Address
from datatypes.datatype import Type
from message import Message
import time

flags = dict(
    Request=1 << 7,
    Proxiable=1 << 6,
    Error=1 << 5,
    Retransmitted=1 << 4,
    VendorSpecific=1 << 7,
    Mandatory=1 << 6,
    Protected=1 << 5)

types = {
    "Address": Address,
    "DiameterIdentity": DiameterIdentity,
    "DiameterURI": DiameterURI,
    "Enumerated": Enumerated,
    "Float32": Float32,
    "Float64": Float64,
    "Grouped": GroupedAVP,
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


def findType(avpcode=None, avpname=None, vendorid=None):
    pass


def makeCER():
    from avp import AVP, avpflags
    m = Message(cmdflags=flags['Request'], cmdcode=257, appId=0)
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity('10.5.8.11'))
    originRealm = AVP(
        code=296, flags=64, data=DiameterIdentity('azercell.com'))
    host_IP_Address = AVP(code=257, flags=0x40, data=Address('10.5.8.11'))
    vendorID = AVP(code=266, flags=0x40, data=Unsigned32(193))
    productName = AVP(code=269, flags=0b0, data=OctetString('Delishka'))
    authAppId = AVP(code=258, flags=0x40, data=Unsigned32(4))
    avps = [originHost, originRealm, host_IP_Address,
            vendorID, productName, authAppId]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()


def makeCEA():
    from avp import AVP, avpflags
    m = Message(cmdflags=0b0, cmdcode=257, appId=0)
    resultCode = AVP(code=268, flags=0x40, data=Unsigned32(2001))
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity('10.5.8.11'))
    originRealm = AVP(code=296, flags=0x40,
                      data=DiameterIdentity('azercell.com'))
    host_IP_Address = AVP(code=257, flags=0x40, data=Address('10.5.8.11'))
    vendorID = AVP(code=266, flags=0x40, data=Unsigned32(193))
    productName = AVP(code=269, flags=0b0, data=OctetString('Delishka'))
    authAppId = AVP(code=258, flags=0x40, data=Unsigned32(4))
    avps = [resultCode, originHost, originRealm, host_IP_Address,
            vendorID, productName, authAppId]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()


def makeDWR():
    from avp import AVP, avpflags
    m = Message(cmdflags=0b0, cmdcode=280, appId=0)
    originHost = AVP(
        code=264, flags=0x40, data=DiameterIdentity('10.5.8.11'))
    originRealm = AVP(
        code=296, flags=0x40, data=DiameterIdentity('azercell.com'))
    avps = [originHost, originRealm]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()


def makeDWA():
    from avp import AVP, avpflags
    m = Message(cmdflags=0b0, cmdcode=280, appId=0)
    resultCode = AVP(code=268, flags=0x40, data=Unsigned32(2001))
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity('10.5.8.11'))
    originRealm = AVP(code=296, flags=0x40,
                      data=DiameterIdentity('azercell.com'))
    avps = [resultCode, originHost, originRealm]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()


def makeCCR():
    from avp import AVP, avpflags
    m = Message(cmdflags=0b0, cmdcode=272, appId=0)
    sessionID = AVP(code=263, flags=0x40, data=UTF8String(
        'delishka;hlapi;1611836847258625'))
    serviceContextID = AVP(code=461, flags=0x40,
                           data=UTF8String('SCAP_V.2.0@ericsson.com'))
    authAppId = AVP(code=258, flags=0x40, data=Unsigned32(4))
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity('10.5.8.11'))
    originRealm = AVP(code=296, flags=0x40,
                      data=DiameterIdentity('azercell.com'))
    ccRequestNumber = AVP(code=415, flags=0x40, data=Unsigned32(0))
    serviceIdentifier = AVP(code=439, flags=0x40, data=Unsigned32(3))
    destinationRealm = AVP(code=283, flags=0x40,
                           data=DiameterIdentity('azercell2.com'))
    eventTimestamp = AVP(code=55, flags=0x40, data=Time(time.time()))
    subscriptionID = AVP(code=443, flags=0x40, data=GroupedAVP([
        AVP(code=444, flags=0x40, data=UTF8String('994504040098')),
        AVP(code=450, flags=0x40, data=Enumerated(0))
    ]))
    otherPartyId = AVP(code=1075, flags=0x40, data=GroupedAVP([
        AVP(code=1077, flags=0x40, data=UTF8String('98915')),
        AVP(code=1078, flags=0x40, data=Enumerated(0))
    ]))
    msTimeZone = AVP(code=23, flags=0xc0, data=OctetString(
        '00000017c000000e000028af00000000'))
    ccRequestType = AVP(code=416, flags=0x40, data=Enumerated(1))
    ccRequestedServiceUnit = AVP(code=437, flags=0x40, data=GroupedAVP(
        [
            AVP(code=417, flags=0x40, data=Unsigned32(1))
        ]
    ))

    avps = [sessionID, serviceContextID, authAppId, originHost, originRealm,
            ccRequestNumber, serviceIdentifier, destinationRealm, eventTimestamp,
            subscriptionID, otherPartyId, msTimeZone, ccRequestType, ccRequestedServiceUnit]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()


def makeCCA():
    from avp import AVP, avpflags
    m = Message(cmdflags=0b0, cmdcode=272, appId=0)
    sessionID = AVP(code=263, flags=0x40, data=UTF8String(
        'delishka;hlapi;1611836847258625'))
    resultCode = AVP(code=268, flags=0x40, data=Unsigned32(2001))
    authAppId = AVP(code=258, flags=0x40, data=Unsigned32(4))
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity('10.5.8.11'))
    originRealm = AVP(code=296, flags=0x40,
                      data=DiameterIdentity('azercell.com'))
    ccRequestNumber = AVP(code=415, flags=0x40, data=Unsigned32(0))
    ccRequestType = AVP(code=416, flags=0x40, data=Enumerated(1))
    ccGrantedServiceUnit = AVP(code=431, flags=0x40, data=GroupedAVP(
        [
            AVP(code=417, flags=0x40, data=Unsigned32(1))
        ]
    ))
    validityTime = AVP(code=448, flags=0x40, data=Unsigned32(120))
    avps = [sessionID, resultCode, authAppId, originHost, originRealm,
            ccRequestNumber, ccRequestType, ccGrantedServiceUnit, validityTime]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()
