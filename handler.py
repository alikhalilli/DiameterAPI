import asyncio
from abc import ABC, abstractmethod
from message import Message
from Errors import CommandNotFoundException


class Handler(ABC):
    @abstractmethod
    def next_handler(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    _next_handler = None

    def next_handler(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, request):
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
        Header = Message.decodeHeader(request[:20])
        print(Header)
        cmdCode = Header.cmdcode
        cmdType = Header.cmdflags
        handler = None
        if cmdCode == 257 & cmdType:
            handler = self.cerhndlr
        elif cmdCode == 257 & (not cmdType):
            handler = self.ceahndlr
        elif cmdCode == 272 & cmdType:
            handler = self.ccrhndlr
        elif cmdCode == 272 & (not cmdType):
            handler = self.ccahndlr
        elif cmdCode == 280 & cmdType:
            handler = self.dwrhndlr
        elif cmdCode == 280 & (not cmdType):
            handler = self.dwahndlr
        elif cmdCode == 282 & cmdType:
            handler = self.dprhndlr
        elif cmdCode == 283 & (not cmdType):
            handler = self.dpahndlr
        else:
            raise CommandNotFoundException(msg="Command Not Found")
        self.next_handler(handler)
        if self._next_handler:
            self._next_handler.handle(request[20:])


class CERHandler(AbstractHandler):
    def handle(self, request):
        avps = [avp for avp in Message.decodeBody(request)]
        for avp in avps:
            print(avp)


class CEAHandler(AbstractHandler):
    def handle(self, request):
        pass


class CCRHandler(AbstractHandler):
    def handle(self, request):
        pass


class CCAHandler(AbstractHandler):
    def handle(self, request):
        pass


class DWRHandler(AbstractHandler):
    def handle(self, request):
        pass


class DWAHandler(AbstractHandler):
    def handle(self, request):
        pass


class DPRHandler(AbstractHandler):
    def handle(self, request):
        pass


class DPAHandler(AbstractHandler):
    def handle(self, request):
        pass


def client_code(handler, request):
    handler.handle(request)
