import utils
from Errors import CommandNotFoundException
import message
import abc
import asyncio
from functools import partial


class GyProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        print(transport)


class Session:
    def __await__(self):
        yield self


class Peer:
    def __init__(self, transport):
        self._transport = transport

    @property
    def transport(self):
        return self._transport


class PeerTable:
    def __init__(self, peers=[]):
        self._peers = peers


SessionFutureMap = dict()


class Handler(abc.ABC):
    @abc.abstractmethod
    def next_handler(self, handler):
        pass

    @abc.abstractmethod
    def handle(self, header, request):
        pass


class AbstractHandler(Handler):
    _next_handler = None

    def next_handler(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, header, request):
        if self._next_handler:
            self._next_handler.handle(request)
        return None


class HeaderHandler(AbstractHandler):
    def __init__(self):
        self.cerhndlr = CERHandler()
        self.ceahndlr = CEAHandler()
        self.ccrhndlr = CCRHandler()
        self.ccahndlr = CCAHandler()
        self.dwrhndlr = DWRHandler()
        self.dwahndlr = DWAHandler()
        self.dprhndlr = DPRHandler()
        self.dpahndlr = DPAHandler()

    def handle(self, request):
        header = message.Message.decodeHeader(request[:20])
        cmdCode = header.cmdcode
        cmdType = header.cmdflags
        handler = None
        if (cmdCode == 257) & (cmdType != 0b0):
            handler = self.cerhndlr
        elif (cmdCode == 257) & (cmdType == 0b0):
            handler = self.ceahndlr
        elif (cmdCode == 272) & (cmdType != 0b0):
            handler = self.ccrhndlr
        elif (cmdCode == 272) & (cmdType == 0b0):
            handler = self.ccahndlr
        elif (cmdCode == 280) & (cmdType != 0b0):
            handler = self.dwrhndlr
        elif (cmdCode == 280) & (cmdType == 0b0):
            handler = self.dwahndlr
        elif (cmdCode == 282) & (cmdType != 0b0):
            handler = self.dprhndlr
        elif (cmdCode == 283) & (cmdType == 0b0):
            handler = self.dpahndlr
        else:
            raise CommandNotFoundException(msg="Command Not Found")
        self.next_handler(handler)
        if self._next_handler:
            self._next_handler.handle(header, request[20:])


class CERHandler(AbstractHandler):
    def handle(self, header, request):
        avps = [avp for avp in message.Message.decodeBody(request)]
        for avp in avps:
            print(avp)


class CEAHandler(AbstractHandler):
    def handle(self, request):
        pass


class CCRHandler(AbstractHandler):
    def handle(self, request):
        pass


class CCAHandler(AbstractHandler):
    def handle(self, header, request):
        avps = [avp for avp in message.Message.decodeBody(request)]
        for avp in avps:
            print(avp)
            if avp.code == "283":  # session avp
                try:
                    SessionFutureMap[avp.data].set_result((header, avps))
                    return
                except KeyError:
                    print("Session not found")


class DWRHandler(AbstractHandler):
    def handle(self, request, conn):
        conn.sendall(utils.makeDWA())


class DWAHandler(AbstractHandler):
    def handle(self, request):
        pass


class DPRHandler(AbstractHandler):
    def handle(self, request):
        pass


class DPAHandler(AbstractHandler):
    def handle(self, request):
        pass


class PeerProtocol(asyncio.Protocol):

    def __init__(self, fut, peer=None):
        self._fut = fut
        self._peer = None
        self._handler = HeaderHandler()

    def connection_made(self, transport):
        self.transport = transport
        global peerTable
        peerTable["1"] = transport
        transport.write("smth".encode())

    def data_received(self, data):
        self._handler.handle(data)

    def CCRHandler(self):
        # message.decode().getSession()
        SessionFutureMap["session"].set_result("message")

    def getSessionMapping(self):
        pass

    def handleCCA(self, b):
        global SessionFutureMap
        sessionAVP = "12343t35"
        SessionFutureMap[sessionAVP].future.set_result(b)

    def connection_lost(self, exc):
        self._fut.set_result(exc)


async def addPeer(fut):
    loop = asyncio.get_event_loop()
    protofactory = partial(PeerProtocol, fut)
    connection_coro = loop.create_connection(
        protocol_factory=protofactory,
        host='127.0.0.1',
        port=8888)
    await asyncio.ensure_future(connection_coro)


async def peerResult():
    global peerTable
    print(peerTable)


async def periodicPeerCheck():
    while True:
        await asyncio.sleep(5)
        print(await peerResult())


class WatchDogTask:
    def __init__(self, loop):
        self._loop = loop

    def cancel(self):
        self._loop.cancel()


async def periodicDWR(self):
    while True:
        await asyncio.sleep(5)


async def doCCR(testcase):
    dttime -= 60
    message = makeCCR(dttime, session=True)
    result = await message.send(peerTable["peer1"])
    # send methodun-da await edirem future ucun
    grantedUnit = result["message"]
    while dtime % 60 > 0:
        pass


peerTable = dict()


async def main():
    future = asyncio.get_event_loop().create_future()
    await asyncio.ensure_future(addPeer(future))
    await asyncio.ensure_future(periodicPeerCheck())
    await future


loop = asyncio.get_event_loop()
loop.run_until_complete(main())


"""

async def main():
    loop = asyncio.get_event_loop()
    server = await loop.create_server(protocol_factory=lambda: GyProtocol(), host='127.0.0.1', port=8888)
    async with server:
        await server.serve_forever()

asyncio.run(main())
"""
