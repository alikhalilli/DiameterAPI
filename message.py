from diameterheader import Header
from avp import AVP


class Message:
    def __init__(self,
                 cmdflags,
                 cmdcode,
                 appId,
                 avps=[]):
        self.header = Header(cmdflags=cmdflags,
                             cmdcode=cmdcode,
                             appId=appId)
        self.avps = avps

    def addNewAVP(self, avp):
        self.avps.append(avp)
        self.header._msglength += len(avp)

    def encode(self):
        encoded = bytearray()
        encoded += self.header.encode()
        for avp in self.avps:
            print(f"encoding avp: {avp.code}")
            encoded += avp.encode()
        return encoded

    @staticmethod
    def decodeHeader(buff):
        return Header.decode(buff)

    @staticmethod
    def decodeBody(buff):
        while buff:
            a = AVP.decodeFromBuffer(buff)
            buff = buff[len(a):]
            yield a

    @staticmethod
    def decodeFromBytes(self, buff):
        header = Message.decodeHeader(buff[:self.header.headerlength()])
        decodedAVPs = [a for a in Message.decodeBody(buff[20:])]
        return Message(header.cmdflags, header.cmdcode, header.appId, decodedAVPs)

    def length(self):
        return self.header.length

    def __repr__(self):
        return f"""
        Header: {self.header}
        AVPs: {[avp for avp in self.avps]}
        """
