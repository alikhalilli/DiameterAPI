import asyncio
import abc
import message
from sessionFactory import Session
from Errors import CommandNotFoundException
import utils
from async_handler import PeerStates

sessionfuturemap = dict()


class Handler(abc.ABC):
    @abc.abstractmethod
    def next_handler(self, handler):
        pass

    @abc.abstractmethod
    def handle(self, peer, request):
        pass


class AbstractHandler(Handler):
    _next_handler = None

    def next_handler(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, peer, request):
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

    def handle(self, peer, request):
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
            self._next_handler.handle(peer, header, request[20:])


class CERHandler(AbstractHandler):
    def handle(self, peer, header, request):
        if peer.state == PeerStates.WAIT_I_CEA:
            avps = [avp for avp in message.Message.decodeBody(request)]
            for avp in avps:
                print(avp)
            peer.state = PeerStates.I_OPEN
            peer.startWatchDog()


class CEAHandler(AbstractHandler):
    def handle(self, peer, header, request):
        pass


class CCRHandler(AbstractHandler):
    def handle(self, peer, request):
        pass


class CCAHandler(AbstractHandler):
    def handle(self, peer, header, request):
        avps = [avp for avp in Session.decodeBody(request)]
        for avp in avps:
            if avp.code == "263":  # session avp
                try:
                    peer.sessionfuturemap[avp.data.value].set_result(
                        (header, avps))
                    return
                except KeyError:
                    print("Session not found")


class DWRHandler(AbstractHandler):
    def handle(self, request, conn):
        conn.sendall(utils.makeDWA())


class DWAHandler(AbstractHandler):
    def handle(self, peer, header, request):
        avps = [avp for avp in message.Message.decodeBody(request)]
        peer.state = PeerStates.IDLE
        peer.resetWatchDog()


class DPRHandler(AbstractHandler):
    def handle(self, request):
        pass


class DPAHandler(AbstractHandler):
    def handle(self, request):
        pass


def client_code(handler, request):
    handler.handle(request)
