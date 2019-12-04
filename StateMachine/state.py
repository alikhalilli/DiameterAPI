import abc


class State(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self, name):
        pass

    @abc.abstractmethod
    def enter(self):
        pass

    @abc.abstractmethod
    def exit(self):
        pass


class Closed(State):
    def __init__(self, name="Closed"):
        self._name = name
