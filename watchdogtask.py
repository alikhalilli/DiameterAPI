import asyncio
import boilerplatemessages


class WatchDogTask:
    def __init__(self, interval, peer):
        self._interval = interval
        self._peer = peer
        self._currentTask = None

    def resetDWR(self):
        self.cancelDWR()
        # self.startDWR()

    def cancelDWR(self):
        if self._currentTask:
            self._currentTask.cancel()

    def startDWR(self):
        self._currentTask = asyncio.ensure_future(self.sendDWR())

    async def sendDWR(self):
        while True:
            await asyncio.sleep(self._interval)
            self._peer.transport.write(
                boilerplatemessages.makeDWR(self._peer.origHost,
                                            self._peer.origRealm
                                            ))
