import asyncio
from handler import HeaderHandler
from functools import partial
from datatypes.diamidentity import DiameterIdentity
from baseavp import AVP
from message import Message

######### Messages #############


def makeDWR(appId, o_host='10.5.8.11', o_realm='azercell.com'):
    m = Message(cmdflags=0b0, cmdcode=280, appId=0)
    originHost = AVP(code=264, flags=0x40, data=DiameterIdentity(o_host))
    originRealm = AVP(code=296, flags=0x40, data=DiameterIdentity(o_realm))
    avps = [originHost, originRealm]
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


class PeerStates(enum):
    def __init__(self):
        pass


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
        global peerTable
        self._peer.transport = transport
        await self.makeCCR()

    def data_received(self, data):
        self._handler.handle(self._peer, data)

    async def makeCCR(self):
        self._peer.transport.write("CCRMessage")

    def CCRHandler(self):
        # message.decode().getSession()
        sessionFutureMap["session"].set_result("message")

    def getSessionMapping(self):
        pass

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
