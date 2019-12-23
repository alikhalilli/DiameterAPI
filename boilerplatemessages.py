from headerflags.avpflags import AVPFlags
from headerflags.messageflags import MessageFlags
from message import Message
from sessionFactory import Session
from baseavp import AVP
import time

from datatypes.address import Address
from datatypes.unsigned32 import Unsigned32
from datatypes.octetstring import OctetString
from datatypes.utf8string import UTF8String
from datatypes.dtime import Time
from datatypes.unsigned32 import Unsigned32
from datatypes.unsigned64 import Unsigned64
from datatypes.enumerated import Enumerated
from datatypes.diamidentity import DiameterIdentity

######### Messages #############


def makeDWR(o_host='10.5.8.11', o_realm='azercell.com'):
    m = Message(cmdflags=MessageFlags.REQUEST.value, cmdcode=280, appId=0)
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(o_host))
    originRealm = AVP(code=296, flags=0x40, data=DiameterIdentity(o_realm))
    avps = [originHost, originRealm]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()


def makeDWA(resultCode=2001, o_host='10.5.8.11', o_realm='azercell.com'):
    m = Message(cmdflags=0x00, cmdcode=280, appId=0)
    resultCode = AVP(code=268, flags=AVPFlags.MANDATORY,
                     data=Unsigned32(resultCode))
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(o_host))
    originRealm = AVP(code=296, flags=0x40, data=DiameterIdentity(o_realm))
    avps = [resultCode, originHost, originRealm]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()


def makeCER(o_host='10.5.8.11', o_realm='azercell.com', prod_name='AiDiameter'):
    message = Message(cmdflags=MessageFlags.REQUEST.value,
                      cmdcode=257, appId=0)
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(o_host))
    originRealm = AVP(code=296, flags=64,
                      data=DiameterIdentity(o_realm))
    host_IP_Address = AVP(code=257, flags=0x40, data=Address(o_host))
    vendorID = AVP(code=266, flags=0x40, data=Unsigned32(193))
    productName = AVP(code=269, flags=0x00, data=OctetString(prod_name))
    authAppId = AVP(code=258, flags=0x40, data=Unsigned32(4))
    avps = [originHost, originRealm, host_IP_Address,
            vendorID, productName, authAppId]
    for avp in avps:
        message.addNewAVP(avp)
    return message


def makeCEA(o_host='10.5.8.11', o_realm='azercell.com', prod_name='AiDiameter'):
    message = Message(cmdflags=0x00,
                      cmdcode=257, appId=0)
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(o_host))
    originRealm = AVP(code=296, flags=64,
                      data=DiameterIdentity(o_realm))
    host_IP_Address = AVP(code=257, flags=0x40, data=Address(o_host))
    vendorID = AVP(code=266, flags=0x40, data=Unsigned32(193))
    productName = AVP(code=269, flags=0x00, data=OctetString(prod_name))
    authAppId = AVP(code=258, flags=0x40, data=Unsigned32(4))
    avps = [originHost, originRealm, host_IP_Address,
            vendorID, productName, authAppId]
    for avp in avps:
        message.addNewAVP(avp)
    return message


def makeCCR(sessionId="csdk;hlapi;1611836847258625",
            ccontext="SCAP_V.2.0@ericsson.com",
            origHost='DESKTOP-KTP2918.azercell.com',
            origRealm='azercell.com',
            destRealm='azercell2.com',
            servedmsisdn='504040098',
            bnumber='879462'):
    from groupedAVP import GroupedAVP
    m = Session(cmdflags=MessageFlags.REQUEST.value,
                cmdcode=272, appId=4, sessionId=sessionId)
    #sessionID = AVP(code=263, flags=0x40, data=UTF8String(sessionId))
    serviceContextID = AVP(code=461, flags=0x40, data=UTF8String(ccontext))
    authAppId = AVP(code=258, flags=0x40, data=Unsigned32(4))
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(origHost))
    originRealm = AVP(code=296, flags=0x40, data=DiameterIdentity(origRealm))
    ccRequestNumber = AVP(code=415, flags=0x40, data=Unsigned32(0))
    serviceIdentifier = AVP(code=439, flags=0x40, data=Unsigned32(3))
    destinationRealm = AVP(code=283, flags=0x40,
                           data=DiameterIdentity(destRealm))
    eventTimestamp = AVP(code=55, flags=0x40, data=Time(time.time()))
    subscriptionID = AVP(code=443, flags=0x40, data=GroupedAVP([
        AVP(code=450, flags=0x40, data=Enumerated(0)),
        AVP(code=444, flags=0x40, data=UTF8String(servedmsisdn))
    ]))
    otherPartyId = AVP(code=1075, flags=0xc0, vendorID=193, data=GroupedAVP([
        AVP(code=1077, flags=0xc0, vendorID=193, data=UTF8String(bnumber)),
        AVP(code=1078, flags=0xc0, vendorID=193, data=Enumerated(0))
    ]))
    msTimeZone = AVP(code=23, flags=0xc0, vendorID=10415,
                     data=OctetString('  '))
    ccRequestType = AVP(code=416, flags=0x40, data=Enumerated(1))
    ccRequestedServiceUnit = AVP(code=437, flags=0x40, data=GroupedAVP(
        [
            AVP(code=417, flags=0x40, data=Unsigned64(4))
        ]
    ))
    requestedAction = AVP(code=436, flags=0x40, data=Enumerated(0))
    avps = [serviceContextID,
            authAppId,
            originHost,
            originRealm,
            ccRequestNumber,
            serviceIdentifier,
            destinationRealm,
            eventTimestamp,
            subscriptionID,
            otherPartyId,
            msTimeZone,
            ccRequestType,
            requestedAction,
            ccRequestedServiceUnit]
    for avp in avps:
        m.addNewAVP(avp)
    # sessTable.insertSession(sessionId, m._state)
    return m


def makeDPR(o_host='10.5.8.11', o_realm='azercell.com'):
    m = Message(cmdflags=MessageFlags.REQUEST.value, cmdcode=280, appId=0)
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(o_host))
    originRealm = AVP(code=296, flags=0x40, data=DiameterIdentity(o_realm))
    avps = [originHost, originRealm]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()


def makeDPA(o_host='10.5.8.11', o_realm='azercell.com'):
    m = Message(cmdflags=MessageFlags.REQUEST.value, cmdcode=280, appId=0)
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(o_host))
    originRealm = AVP(code=296, flags=0x40, data=DiameterIdentity(o_realm))
    avps = [originHost, originRealm]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()
##############################################
