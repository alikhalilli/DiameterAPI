from enum import Enum, auto
from watchdogtask import WatchDogTask


class PeerStates(Enum):
    IDLE = auto(),
    WAIT_CONN_ACK = auto(),
    WAIT_I_CEA = auto(),
    WAIT_RETURNS = auto(),
    R_OPEN = auto(),
    I_OPEN = auto(),
    CLOSING = auto(),
    ELECT = auto()


class Peer:
    def __init__(self, appId, firmwareId, vendorId, transport, watchdogInterval):
        self._appId = appId
        self._firmwareId = firmwareId
        self._vendorId = vendorId
        self._transport = transport
        self._sessionFutureMap = dict()
        self._watchdogTask = WatchDogTask(watchdogInterval, self)
        self._state = None
        self._stateObservers = []

    def addStateChangeListener(self, observer):
        self._stateObservers.append(observer)

    def notifyStateChange(self):
        for observer in self._stateObservers:
            observer.stateChanged(self)

    @property
    def sessionFutureMap(self):
        return self._sessionFutureMap

    @sessionFutureMap.setter
    def sessionFutureMap(self, val):
        self._sessionFutureMap = val

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        self._state = val
        self.notifyStateChange()

    @property
    def transport(self):
        return self._transport

    @transport.setter
    def transport(self, val):
        self._transport = val

    def startWatchDog(self):
        self._watchdogTask.startDWR()

    def resetWatchDog(self):
        self._watchdogTask.resetDWR()

    def write(self, data):
        self._transport.write(data)

    def read(self):
        return self._transport.read()