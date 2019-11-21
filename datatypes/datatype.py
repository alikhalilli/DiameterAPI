from abc import ABC, abstractmethod


class Type(ABC):
    @abstractmethod
    def typelen(self):
        raise NotImplementedError

    @abstractmethod
    def len(self):
        raise NotImplementedError

    @abstractmethod
    def encode(self):
        raise NotImplementedError

    @abstractmethod
    def decode(self):
        raise NotImplementedError

    @abstractmethod
    def getpadding(self):
        raise NotImplementedError
