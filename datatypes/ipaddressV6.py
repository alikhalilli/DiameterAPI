from .datatype import Type
import socket


class IpAddressV6(Type):
    def __init__(self, value):
        self._value = value

    @staticmethod
    def decodeFromBuffer(buff):
        return IpAddressV6(socket.inet_ntop(socket.AF_INET6, buff))

    def encode(self):
        return socket.inet_pton(socket.AF_INET6, self._value)

    def decode(self):
        pass

    def getpadding(self):
        return 0

    def __len__(self):
        return 16

    def len(self):
        return self.__len__()
