from diameterheader import Header
from avp import AVP


class Message:
    def __init__(self,
                 cmdflags,
                 cmdcode,
                 appId):
        self.header = Header(cmdflags=cmdflags,
                             cmdcode=cmdcode,
                             appId=appId)
        self.avps = []

    def addNewAVP(self, avp):
        self.avps.append(avp)
        self.header._msglength += len(avp)

    def encode(self):
        encoded = bytearray()
        encoded += self.header.encode()
        for avp in self.avps:
            encoded += avp.encode()
        return encoded

    def decodeHeader(self, buff):
        return Header.decode(buff)

    def decodeBody(self, buff):
        while buff:
            a = AVP.decodeFromBuffer(buff)
            buff = buff[len(a):]
            yield a

    def decodeFromBytes(self, buff):
        header = self.decodeHeader(buff[:self.header.headerlength()])
        decodedAVPs = [a for a in self.decodeBody(
            buff[self.header.headerlength():])]
        return (header, decodedAVPs)

    def __repr__(self):
        return f"""
        Header: {self.header}
        AVPs: {[avp for avp in self.avps]}
        """
