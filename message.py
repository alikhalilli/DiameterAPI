import diameterheader
import random
import asyncio


"""
Package Header Flags:
+-+-+-+-+-+-+-+-+
|R|P|E|T|r|r|r|r|
+-+-+-+-+-+-+-+-+

10000000 1<<7 0x80
01000000 1<<6 0x40
00100000 1<<5 0x20
00010000 1<<4 0x10

AVP Header Flags:
+-+-+-+-+-+-+-+-+
|V|M|P|r|r|r|r|r|
+-+-+-+-+-+-+-+-+

10000000 1<<7 0x80
01000000 1<<6 0x40
00100000 1<<5 0x20
"""


class Message:
    def __init__(self,
                 cmdflags,
                 cmdcode,
                 appId,
                 avps=list(),
                 hopByHopId=random.getrandbits(32),
                 endToEndId=random.getrandbits(32)):
        self._header = diameterheader.Header(cmdflags=cmdflags,
                                             cmdcode=cmdcode,
                                             appId=appId,
                                             hopByHopId=hopByHopId,
                                             endToEndId=endToEndId)
        self._avps = avps if avps else list()
        self._session = None

    def addNewAVP(self, avp):
        self._avps.append(avp)
        self._header._msglength += len(avp)

    def encode(self):
        encoded = bytearray()
        encoded += self._header.encode()
        for avp in self._avps:
            encoded += avp.encode()
        return encoded

    async def send(self, peer):
        await peer.write(self.encode())
        future = asyncio.get_event_loop().create_future()
        return await future

    @staticmethod
    def decodeHeader(buff):
        return diameterheader.Header.decode(buff)

    @staticmethod
    def decodeBody(buff):
        import baseavp
        while buff:
            a = baseavp.AVP.decodeFromBuffer(buff)
            buff = buff[len(a):]
            yield a

    @staticmethod
    def decodeFromBytes(buff):
        header = Message.decodeHeader(buff[:20])
        decodedAVPs = [a for a in Message.decodeBody(buff[20:])]
        return Message(cmdflags=header.cmdflags,
                       cmdcode=header.cmdcode,
                       appId=header.appId,
                       hopByHopId=header.hopByHopId,
                       endToEndId=header.endToEndId,
                       avps=decodedAVPs)

    @property
    def avps(self):
        if self._avps is None:
            return []
        return list(self._avps)

    @property
    def header(self):
        return self._header

    def length(self):
        return self._header.length

    def __repr__(self):
        return f"""
        Header: {self._header}
        AVPs: {[avp for avp in self._avps]}
        """
