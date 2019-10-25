class Message:
    def __init__(self):
        self.header = ''
        self.avps = []

    def addNewAVP(self, avp):
        self.avps.append(avp)
    
    