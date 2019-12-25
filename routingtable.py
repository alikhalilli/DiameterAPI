from enum import IntEnum, auto


class LocalAction(IntEnum):
    LOCAL = auto(),
    RELAY = auto(),
    PROXY = auto(),
    REDIRECT = auto()


class RoutingTable:
    def __init__(self, realmname, appID, serverID, localaction, discoverytype, expirationTime=None):
        self._realmname = realmname
        self._appID = appID
        self._serverID = serverID
        self._localaction = localaction
        self._discoveryType = discoverytype
        self._expirationTime = expirationTime
        self._subscribers = []

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def notifySubscribers(self):
        for subscriber in self._subscribers:
            subscriber.notify()
