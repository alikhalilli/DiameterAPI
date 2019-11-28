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
    def handle(self, request):
        cerhndlr = CERHandler()
        ccrhndlr = CCRHandler()
        dwrhndlr = DWRHandler()
        Header = Message.decodeHeader(request[:20])
        cmdCode = Header.cmdcode
        cmdType = Header.cmdflags
        if cmdCode == 253:
            self.next_handler(cerhndlr)
        elif cmdCode == 254:
            self.next_handler(ccrhndlr)
        elif cmdCode == 255:
            self.next_handler(dwrhndlr)
        else:
            raise CommandNotFoundException(msg="Command Not Found")

        if self._next_handler:
            self._next_handler.handle(request)


def CCAHandler():
    pass


class CERHandler(AbstractHandler):
    def handle(self, request):
        pass


class CCRHandler(AbstractHandler):
    def handle(self, request):
        pass


class DWRHandler(AbstractHandler):
    def handle(self, request):
        pass


def client_code(handler, request):
    handler.handle(request)
