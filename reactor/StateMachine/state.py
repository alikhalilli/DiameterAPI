import abc
import enum


class Event(enum.Enum):


class PeerStateMachine:
    def __init__(self, state):
        self._state = state


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

    @abc.abstractmethod
    def next_state(self):
        pass


class Closed(State):
    def __init__(self, name="Closed"):
        self._name = name
