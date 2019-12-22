import asyncio


class Peer:
    def __init__(self, transport):
        self._transport = transport

    @property
    def transport(self):
        return self._transport

    @transport.setter
    def transport(self, val):
        self._transport = val

    def write(self, data):
        self._transport.write(data)

    def read(self):
        return self._transport.read()


peerTable = None


async def sendPeriodicMessage(p):
    while True:
        p.write("salamsalam".encode())
        await asyncio.sleep(0)


class PeerProtocol(asyncio.Protocol):
    def __init__(self):
        self._peer = None

    def connection_made(self, transport):
        self._peer = Peer(transport)
        self._peer.write("salamsalam".encode())
        asyncio.ensure_future(sendPeriodicMessage(self._peer))

    def data_received(self, data):
        print("--")
        print(data)

    def connection_lost(self, exc):
        self._peer = None


async def addPeer():
    loop = asyncio.get_event_loop()
    connection_coro = loop.create_connection(
        protocol_factory=lambda: PeerProtocol(),
        host='127.0.0.1',
        port=8888)
    connection_coro2 = loop.create_connection(
        protocol_factory=lambda: PeerProtocol(),
        host='127.0.0.1',
        port=8877)
    await asyncio.ensure_future(connection_coro)
    await asyncio.ensure_future(connection_coro2)


loop = asyncio.get_event_loop()
loop.run_until_complete(addPeer())
loop.run_forever()

"""async def printNumbers(i):
    print(f"----{i}-----")
    await asyncio.sleep(5)


async def runner():
    for _ in range(100):
        await printNumbers(1)
    #tasks = [asyncio.ensure_future(printNumbers(i)) for i in range(100)]
    # await asyncio.gather(*tasks)


async def runner2():
    for _ in range(100):
        await printNumbers(2)


async def main():
    await asyncio.gather(runner(), runner2())

asyncio.run(main())
"""
