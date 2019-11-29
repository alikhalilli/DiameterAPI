import abc


class AbstractType(abc.ABC):

    @abc.abstractmethod
    def encode(self):
        raise NotImplementedError

    @abc.abstractmethod
    def len(self):
        raise NotImplementedError

    @abc.abstractmethod
    def getpadding(self):
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def decodeFromBuffer(self, buff):
        raise NotImplementedError


class Type(AbstractType):
    def __init__(self, value):
        self._value = value
        self._encoded = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    def getpadding(self):
        return 0

    def __repr__(self):
        return f"""
        Value: {self._value}
        Length: {self.len()}
        Padding: {self.getpadding()}
        Encoded: {self._encoded}"""
