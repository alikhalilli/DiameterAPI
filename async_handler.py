import asyncio
from handler import HeaderHandler
from functools import partial
from datatypes.diamidentity import DiameterIdentity
from baseavp import AVP
from message import Message
from enum import Enum, auto
import handler
from datatypes.address import Address
from datatypes.unsigned32 import Unsigned32
from datatypes.octetstring import OctetString
from datatypes.utf8string import UTF8String
from datatypes.dtime import Time
from datatypes.unsigned32 import Unsigned32
from datatypes.unsigned64 import Unsigned64
from datatypes.enumerated import Enumerated
from sessionFactory import Session, SessionTable
import time

flags = dict(
    Request=1 << 7,
    Proxiable=1 << 6,
    Error=1 << 5,
    Retransmitted=1 << 4,
    VendorSpecific=1 << 7,
    Mandatory=1 << 6,
    Protected=1 << 5)

######### Messages #############


def makeDWR(appId, o_host='10.5.8.11', o_realm='azercell.com'):
    m = Message(cmdflags=0b0, cmdcode=280, appId=0)
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(o_host))
    originRealm = AVP(code=296, flags=0x40, data=DiameterIdentity(o_realm))
    avps = [originHost, originRealm]
    for avp in avps:
        m.addNewAVP(avp)
    return m.encode()


def makeCER(appId, o_host='10.5.8.11', o_realm='azercell.com'):
    message = Message(cmdflags=0b0, cmdcode=257, appId=0)
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(o_host))
    originRealm = AVP(code=296, flags=64,
                      data=DiameterIdentity(o_realm))
    host_IP_Address = AVP(code=257, flags=0x40, data=Address(o_host))
    vendorID = AVP(code=266, flags=0x40, data=Unsigned32(193))
    productName = AVP(code=269, flags=0b0, data=OctetString('AiDiameter'))
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
    m = Session(cmdflags=flags['Request'],
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

##############################################


class RequestTypes(Enum):
    INITIAL_REQUEST = auto()
    UPDATE_REQUEST = auto()
    TERMINATION_REQUEST = auto()
    EVENT_REQUEST = auto()


sessTable = SessionTable()
peerTable = PeerTable()
sessionFutureMap = dict()


class PeerProtocol(asyncio.Protocol):
    def __init__(self, peer=None):
        self._peer = peer
        self._peer.state = PeerStates.WAIT_CONN_ACK
        self._handler = HeaderHandler()
        self._watchdog = None

    def connection_made(self, transport):
        if self._peer.state == PeerStates.WAIT_CONN_ACK:
            self._peer.transport = transport
            self._peer.state = PeerStates.WAIT_I_CEA
            # message encoding/decoding-i ayri processor core-una submit edirem
            # asyncio.ensure_future(transport.write(makeCER()))
            transport.write(makeCER(appId=4))

    def data_received(self, data):
        self._handler.handle(self._peer, data)

    def connection_lost(self, exc):
        self._peer.state = PeerStates.CLOSING
        peerTable.removePeer(self._peer)


async def addPeer(host, port):
    loop = asyncio.get_event_loop()
    protofactory = partial(PeerProtocol, Peer(appId=192,
                                              firmwareId=193,
                                              vendorId=194,
                                              transport=None,
                                              watchdogInterval=5))
    connection_coro = loop.create_connection(
        protocol_factory=protofactory,
        host=host,
        port=port)
    asyncio.ensure_future(connection_coro)  # await elemesende olar


async def simpleCCR(peer):
    session = makeCCR()
    result = await session.send(peer)
    print(result)


peerTable = PeerTable()


async def main():
    asyncio.ensure_future(addPeer(host='127.0.0.1', port=8888))
    asyncio.ensure_future(addPeer(host='127.0.0.1', port=8899))
    asyncio.ensure_future(simpleCCR(peerTable.getPeer("peer01")))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()


"""
async def doCCR(testcase):
    dttime -= 60
    message = makeCCR(dttime, session=True)
    result = await message.send(sessionFutureMap, peerTable["peer1"])
    # send methodun-da await edirem future ucun
    for avp in result.result():
        if avp.code == "431":
            grantedUnit = avp.data.value
    while dtime % 60 > 0:
        pass
"""
