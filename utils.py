import message
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
import groupedAVP
import time
import baseavp

flags = dict(
    Request=1 << 7,
    Proxiable=1 << 6,
    Error=1 << 5,
    Retransmitted=1 << 4,
    VendorSpecific=1 << 7,
    Mandatory=1 << 6,
    Protected=1 << 5)


def findType(avpcode=None, avpname=None, vendorid=None):
    pass


def makeCER():
    cer_message = message.Message(
        cmdflags=flags['Request'], cmdcode=257, appId=0)
    print(cer_message)
    originHost = baseavp.AVP(code=264, flags=0x40,
                             data=diamidentity.DiameterIdentity('10.5.8.11'))
    originRealm = baseavp.AVP(code=296, flags=64,
                              data=diamidentity.DiameterIdentity('azercell.com'))
    host_IP_Address = baseavp.AVP(code=257, flags=0x40,
                                  data=address.Address('10.5.8.11'))
    vendorID = baseavp.AVP(code=266, flags=0x40,
                           data=unsigned32.Unsigned32(193))
    productName = baseavp.AVP(code=269, flags=0b0,
                              data=octetstring.OctetString('Delishka'))
    authAppId = baseavp.AVP(code=258, flags=0x40,
                            data=unsigned32.Unsigned32(4))
    avps = [originHost, originRealm, host_IP_Address,
            vendorID, productName, authAppId]
    for avp in avps:
        cer_message.addNewAVP(avp)
    print(cer_message.encode())
    # return m.encode()


def makeCEA():
    cea_message = message.Message(cmdflags=0b0, cmdcode=257, appId=0)
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
    m = Message(cmdflags=0b0, cmdcode=280, appId=0)
    originHost = AVP(
        code=264, flags=0x40, data=DiameterIdentity('10.5.8.11'))
    originRealm = AVP(
        code=296, flags=0x40, data=DiameterIdentity('azercell.com'))
    avps = [originHost, originRealm]
    for avp in avps:
        print(id(avp))
        m.addNewAVP(avp)
    return m.encode()


def makeDWA():
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
    c = message.Message(cmdflags=1, cmdcode=272, appId=0)
    print(id(c))
    # k = message.Message(cmdflags=1, cmdcode=2, appId=1)
    ccr_message = message.Message(cmdflags=1, cmdcode=272, appId=0)
    print(ccr_message)
    sessionID = baseavp.AVP(code=263,
                            flags=0x40,
                            data=utf8string.UTF8String('delishka;hlapi;1611836847258625'))
    serviceContextID = baseavp.AVP(code=461,
                                   flags=0x40,
                                   data=utf8string.UTF8String('SCAP_V.2.0@ericsson.com'))
    authAppId = baseavp.AVP(code=258,
                            flags=0x40,
                            data=unsigned32.Unsigned32(4))
    originHost = baseavp.AVP(code=264,
                             flags=0x40,
                             data=diamidentity.DiameterIdentity('10.5.8.11'))
    originRealm = baseavp.AVP(code=296,
                              flags=0x40,
                              data=diamidentity.DiameterIdentity('azercell.com'))
    ccRequestNumber = baseavp.AVP(code=415,
                                  flags=0x40,
                                  data=unsigned32.Unsigned32(0))
    serviceIdentifier = baseavp.AVP(code=439,
                                    flags=0x40,
                                    data=unsigned32.Unsigned32(3))
    destinationRealm = baseavp.AVP(code=283,
                                   flags=0x40,
                                   data=diamidentity.DiameterIdentity('azercell2.com'))
    eventTimestamp = baseavp.AVP(code=55,
                                 flags=0x40,
                                 data=dtime.Time(time.time()))
    subscriptionID = baseavp.AVP(code=443, flags=0xc0, vendorID=193, data=groupedAVP.GroupedAVP([
        baseavp.AVP(code=444, flags=0xc0, vendorID=193,
                    data=utf8string.UTF8String('994504040098')),
        baseavp.AVP(code=450, flags=0xc0, vendorID=193,
                    data=enumerated.Enumerated(0))
    ]))
    otherPartyId = baseavp.AVP(code=1075, flags=0xc0, vendorID=193, data=groupedAVP.GroupedAVP([
        baseavp.AVP(code=1077, flags=0xc0, vendorID=193,
                    data=utf8string.UTF8String('98915')),
        baseavp.AVP(code=1078, flags=0xc0, vendorID=193,
                    data=enumerated.Enumerated(0))
    ]))
    msTimeZone = baseavp.AVP(code=23, flags=0xc0, data=octetstring.OctetString(
        '  '))
    ccRequestType = baseavp.AVP(
        code=416, flags=0x40, data=enumerated.Enumerated(1))
    ccRequestedServiceUnit = baseavp.AVP(code=437, flags=0x40, data=groupedAVP.GroupedAVP(
        [
            baseavp.AVP(code=417, flags=0x40, data=unsigned32.Unsigned32(1))
        ]
    ))

    avps = [sessionID, serviceContextID, authAppId, originHost, originRealm,
            ccRequestNumber, serviceIdentifier, destinationRealm, eventTimestamp,
            subscriptionID, otherPartyId, msTimeZone, ccRequestType, ccRequestedServiceUnit]
    for avp in avps:
        print(id(avp))
        ccr_message.addNewAVP(avp)
    print(ccr_message.encode())
    # return m.encode()


def makeCCA():
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
