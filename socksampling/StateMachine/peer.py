

class Peer:
    def __init__(self, sock):
        self._sock = sock

    @property
    def appId(self):
        return self._appId

    @appId.setter
    def appId(self, val):
        self._appId = val
