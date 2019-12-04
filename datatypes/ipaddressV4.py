import socket
import datatypes.datatype as datatype


class IpAddressV4(datatype.Type):
    def __init__(self, value):
        self._value = value

    @staticmethod
    def decodeFromBuffer(buff):
        return IpAddressV4(socket.inet_ntop(socket.AF_INET, buff))

    def encode(self):
        return socket.inet_pton(socket.AF_INET, self._value)

    def getpadding(self):
        return 0

    def __len__(self):
        return 4

    def len(self):
        return self.__len__()
