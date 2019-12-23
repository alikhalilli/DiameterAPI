import asyncio
from handler import HeaderHandler
from functools import partial
from sessionFactory import Session, SessionTable
from peertable import PeerTable
from peer import Peer, PeerStates
import boilerplatemessages


sessTable = SessionTable()
peerTable = PeerTable()
sessionFutureMap = dict()


class PeerProtocol(asyncio.Protocol):
    def __init__(self, peer=None):
        self._peer = peer
        self._peer.state = PeerStates.WAIT_CONN_ACK
        self._handler = HeaderHandler()
        self._watchdog = None

    def connection_made(self, transport):
        if self._peer.state == PeerStates.WAIT_CONN_ACK:
            self._peer.transport = transport
            self._peer.state = PeerStates.WAIT_I_CEA
            # message encoding/decoding-i ayri processor core-una submit edirem
            # asyncio.ensure_future(transport.write(makeCER()))
            transport.write(boilerplatemessages.makeCER(appId=4))

    def data_received(self, data):
        self._handler.handle(self._peer, data)

    def connection_lost(self, exc):
        self._peer.state = PeerStates.CLOSING
        peerTable.removePeer(self._peer)


async def addPeer(host, port):
    loop = asyncio.get_event_loop()
    protofactory = partial(PeerProtocol, Peer(appId=192,
                                              firmwareId=193,
                                              vendorId=194,
                                              transport=None,
                                              watchdogInterval=5))
    connection_coro = loop.create_connection(
        protocol_factory=protofactory,
        host=host,
        port=port)
    asyncio.ensure_future(connection_coro)  # await elemesende olar


async def simpleCCR(peer):
    session = boilerplatemessages.makeCCR()
    result = await session.send(peer)
    print(result)


peerTable = PeerTable()


async def main():
    asyncio.ensure_future(addPeer(host='10.1.0.12', port=3868))
    # asyncio.ensure_future(addPeer(host='127.0.0.1', port=8899))
    # asyncio.ensure_future(simpleCCR(peerTable.getPeer("peer01")))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()


"""
async def doCCR(testcase):
    dttime -= 60
    message = makeCCR(dttime, session=True)
    result = await message.send(sessionFutureMap, peerTable["peer1"])
    # send methodun-da await edirem future ucun
    for avp in result.result():
        if avp.code == "431":
            grantedUnit = avp.data.value
    while dtime % 60 > 0:
        pass
"""
