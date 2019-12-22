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


def makeCCR():
    from groupedAVP import GroupedAVP
    m = Message(cmdflags=flags['Request'], cmdcode=272, appId=4)
    sessionID = AVP(code=263, flags=0x40, data=UTF8String(
        'csdk;hlapi;1611836847258625'))
    serviceContextID = AVP(code=461, flags=0x40,
                           data=UTF8String('SCAP_V.2.0@ericsson.com'))
    authAppId = AVP(code=258, flags=0x40, data=Unsigned32(4))
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(
        'DESKTOP-KTP2918.azercell.com'))
    originRealm = AVP(code=296, flags=0x40,
                      data=DiameterIdentity('azercell.com'))
    ccRequestNumber = AVP(code=415, flags=0x40, data=Unsigned32(0))
    serviceIdentifier = AVP(code=439, flags=0x40, data=Unsigned32(3))
    destinationRealm = AVP(code=283, flags=0x40,
                           data=DiameterIdentity('azercell2.com'))
    eventTimestamp = AVP(code=55, flags=0x40, data=Time(time.time()))
    subscriptionID = AVP(code=443, flags=0x40, data=GroupedAVP([
        AVP(code=450, flags=0x40, data=Enumerated(0)),
        AVP(code=444, flags=0x40, data=UTF8String('994504040098'))
    ]))
    otherPartyId = AVP(code=1075, flags=0xc0, vendorID=193, data=GroupedAVP([
        AVP(code=1077, flags=0xc0, vendorID=193, data=UTF8String('98915')),
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
    avps = [sessionID,
            serviceContextID,
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
    return m.encode()

##############################################


class PeerTable:
    def __init__(self):
        self._peers = []
        self._observers = []

    def addPeer(self, peer):
        self._peers.append(peer)

    def removePeer(self, peer):
        self._peers.remove(peer)

    def addChangeListener(self, observer):
        self._observers.append(observer)

    def notifyObservers(self):
        for observer in self._observers:
            observer.update()


class PeerStates(Enum):
    IDLE = 0x00,
    WAIT_ACK = 0x01


class SessionStates(Enum):
    IDLE = 0x00,
    WAITING = 0x01


class WatchDogTask:
    def __init__(self, interval, peer):
        self._interval = interval
        self._peer = peer
        self._currentTask = None

    def resetDWR(self):
        self._currentTask.cancel()
        self._currentTask = asyncio.ensure_future(self.sendDWR())

    def startDWR(self):
        self._currentTask = asyncio.ensure_future(self.sendDWR())

    async def sendDWR(self):
        while True:
            await asyncio.sleep(self._interval)
            self._peer.transport.write(makeDWR(
                self._peer.appId,
                self._peer.origHost,
                self._peer.origRealm
            ))


class Peer:
    def __init__(self, appId, firmwareId, vendorId, transport, watchdogInterval):
        self._appId = appId
        self._firmwareId = firmwareId
        self._vendorId = vendorId
        self._transport = transport
        self._watchdogTask = WatchDogTask(watchdogInterval, self)
        self._state = None

    @property
    def transport(self):
        return self._transport

    @transport.setter
    def transport(self, val):
        self._transport = val

    def write(self, data):
        self._transport.write(data)

    def read(self):
        return self._transport.read()


peerTable = PeerTable()
peer = Peer(appId=192,
            firmwareId=193,
            vendorId=194,
            transport=None,
            watchdogInterval=5)
sessionFutureMap = dict()


class PeerProtocol(asyncio.Protocol):
    def __init__(self, fut=None, peer=None):
        self._fut = fut
        self._peer = None
        self._handler = HeaderHandler()
        self._watchdog = None

    def connection_made(self, transport):
        self._peer.transport = transport
        self._peer.state = PeerStates.WAIT_ACK
        # message encoding/decoding-i ayri processor core-una submit edirem
        transport.write(await asyncio.create_subprocess_exec(makeCER()))

    def data_received(self, data):
        self._handler.handle(self._peer, data)

    def handleCCA(self, b):
        sessionAVP = "12343t35"
        sessionFutureMap[sessionAVP].future.set_result(b)

    def connection_lost(self, exc):
        self._fut.set_result(exc)


async def addPeer(host, port):
    loop = asyncio.get_event_loop()
    protofactory = partial(PeerProtocol)
    connection_coro = loop.create_connection(
        protocol_factory=protofactory,
        host='127.0.0.1',
        port=8888)
    await asyncio.ensure_future(connection_coro)


async def doCCR(testcase):
    dttime -= 60
    message = makeCCR(dttime, session=True)
    result = await message.send(peerTable["peer1"])
    # send methodun-da await edirem future ucun
    grantedUnit = result["message"]
    while dtime % 60 > 0:
        pass
