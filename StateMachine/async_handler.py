import asyncio
import time
import socket
from functools import lru_cache

"""
base_events
coroutines
events
futures
locks
protocols
runners
queues
streams
subprocess
tasks
transports
"""

asyncio.sleep()


class PeerStateListener:
    def __init__(self):
        pass

    def stateChanged(self, oldstate, newstate):
        pass


class SessionStateListener:
    def __init__(self):
        pass

    def stateChanged(self, oldstate, newstate):
        pass


class Peer:
    def __init__(self, reader, writer, originrealm, appId, firmwareId):
        self._reader = reader
        self._writer = writer
        self._originrealm = originrealm
        self._appId = appId
        self._firmwareId = firmwareId
        self._listeners = []
        self.watchdog = WatchDogTask(interval=5)

    def connect(self):
        pass

    def disconnect(self):
        pass

    def addStateListener(self, listener):
        pass

    def removeStateListener(self, listener):
        pass

    def resetTimer(self):
        self.timer = 5

    async def getTimer(self):
        await self.timer


class PeerTable:
    def __init__(self, peers=[]):
        self._peers = peers

    def insert(self, peer):
        self._peers.append(peer)

    def remove(self, peer):
        self._peers.remove(peer)


class Session:
    def __init__(self, sessid, state):
        self._sessionid = sessid
        self._state = state
        self._future = asyncio.Future()

    def terminate(self):
        if self._state == "IDLE":
            pass

    def __await__(self):
        return self._future


class SessionTable:
    def __init__(self, sess=[]):
        self._sessions = sess

    def insert(self, sess):
        self._sessions.append(sess)

    def remove(self, sess):
        self._sessions.remove(sess)


peerTable = PeerTable()


async def getStreams(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    return reader, writer


async def updatePeerTable(peer, appId=None, vendorId=None):
    pass


def prepareCER():
    return "CERMessage"


def prepareDWR():
    return "DWRMessage"


class WatchDogTask:
    def __init__(self, interval):
        self.interval = interval
        self.task = asyncio.ensure_future(self._job)

    async def _job(self):
        await asyncio.sleep(self.interval)

    def reset(self):
        self.cancel()
        asyncio.ensure_future(self._job())

    def cancel(self):
        self.task.cancel()


async def periodicDWR(timer, peer):
    while True:
        result = await peer.writer.write(prepareDWR())
        loop = asyncio.get_event_loop()
        loop.call_at(time.time() + (await peer.getTimer()))
        await peer.watchdog()


async def addNewPeer(host, port):
    reader, writer = await getStreams(host, port)
    message = prepareCER()
    await writer.write()
    result = message.decodeFromBuffer(await reader.read())
    p = Peer(reader, writer, originrealm,
             result['appID'], result['firmwareId'])
    await updatePeerTable(p)
    asyncio.ensure_future(periodicDWR(timer, p))

asyncio.ensure_future(addNewPeer("127.0.0.1", 8888))


loop = asyncio.get_event_loop()
t1 = loop.create_task(tcp_echo_client(host='127.0.0.1', port=8888))
asyncio.gather()


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        global peerTable
        peername = transport.get_extra_info('peername')
        print(f"Connection from {peername}")
        self.transport = transport
        peerTable.insert(Peer(self.transport.reader,
                              self.transport.writer, "", ""))

    def data_received(self, data):
        message = data.decode()
        print(f"Data received: {message!r}")
        print(f"Send: {message!r}")
        self.transport.write(data)
        # self.transport.close()

    def get_transport(self):
        return self.transport


async def main():
    peerTable = PeerTable()
    print("main begin..")
    loop = asyncio.get_running_loop()
    print("aaaa")
    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '127.0.0.1', 9999
    )
    print("okk..2")
    print(f"Sockets: {server.sockets}")
    async with server:
        await server.serve_forever()

asyncio.run(main())
