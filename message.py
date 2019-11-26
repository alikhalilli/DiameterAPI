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
        return Header()

    def decodeBody(self, buff):
        while buff:
            a = AVP.decodeFromBuffer(buff)
            buff = buff[len(a):]

    def decodeFromBytes(self, buff):
        h = self.decodeHeader(buff[:self.header._headerlength])
        body = buff[self.header._headerlength:]
