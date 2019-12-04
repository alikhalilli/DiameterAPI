import diameterheader
import random


class Message:
    def __init__(self,
                 cmdflags,
                 cmdcode,
                 appId,
                 avps=list(),
                 hopByHopId=random.getrandbits(32),
                 endToEndId=random.getrandbits(32)):
        print(f"new message is being created..")
        self._header = diameterheader.Header(cmdflags=cmdflags,
                                             cmdcode=cmdcode,
                                             appId=appId,
                                             hopByHopId=hopByHopId,
                                             endToEndId=endToEndId)
        self._avps = avps if avps else list()
        # print(id(self._avps))
        #self._encoded = None

    def addNewAVP(self, avp):
        self._avps.append(avp)
        self._header._msglength += len(avp)

    def encode(self):
        encoded = bytearray()
        encoded += self._header.encode()
        print(f"len of avps: {len(self._avps)}")
        for avp in self._avps:
            #print(f"encoding avp: {avp.code}")
            encoded += avp.encode()
        #self._encoded = encoded
        return encoded

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
        return self._avps

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
