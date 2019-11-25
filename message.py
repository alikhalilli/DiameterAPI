from diameterheader import Header


class Message:
    def __init__(self,
                 version,
                 msglength,
                 cmdflags,
                 cmdcode,
                 appId,
                 hopByHopId,
                 endToEndId):
        self.header = Header(version, msglength, cmdflags,
                             cmdcode, appId, hopByHopId, endToEndId)
        self.avps = []

    def addNewAVP(self, avp):
        self.avps.append(avp)

    def encode(self):
        encoded = bytearray()
        encoded += self.header.encode()
        for avp in self.avps:
            encoded += avp.encode()
        return encoded

    def decode(self):
        pass
