import diameterheader
import random


class Message:
    def __init__(self,
                 cmdflags,
                 cmdcode,
                 appId,
                 hopByHopId=random.getrandbits(32),
                 endToEndId=random.getrandbits(32),
                 avps=[]):
        self.header = diameterheader.Header(cmdflags=cmdflags,
                                            cmdcode=cmdcode,
                                            appId=appId,
                                            hopByHopId=hopByHopId,
                                            endToEndId=endToEndId)
        self.avps = avps
        #self._encoded = None

    def addNewAVP(self, avp):
        self.avps.append(avp)
        self.header._msglength += len(avp)

    def encode(self):
        encoded = bytearray()
        encoded += self.header.encode()
        for avp in self.avps:
            print(f"encoding avp: {avp.code}")
            encoded += avp.encode()
        #self._encoded = encoded
        return encoded

    @staticmethod
    def decodeHeader(buff):
        return diameterheader.Header.decode(buff)

    @staticmethod
    def decodeBody(buff):
        from avp import AVP
        while buff:
            a = AVP.decodeFromBuffer(buff)
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

    def length(self):
        return self.header.length

    def __repr__(self):
        return f"""
        Header: {self.header}
        AVPs: {[avp for avp in self.avps]}
        """
