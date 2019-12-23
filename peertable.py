class PeerTable:
    def __init__(self):
        self._peers = []
        self._observers = []

    def getPeer(self, peer):
        for p in self._peers:
            if p.name == peer:
                return p

    def addPeer(self, peer):
        self._peers.append(peer)

    def removePeer(self, peer):
        self._peers.remove(peer)
        self.notifyObservers()

    def addChangeListener(self, observer):
        self._observers.append(observer)

    def notifyObservers(self):
        for observer in self._observers:
            observer.update()
