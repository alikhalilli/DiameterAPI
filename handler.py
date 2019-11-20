import asyncio
from abc import ABC, abstractmethod


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
