from message import Message
from diameterheader import Header
from baseavp import AVP
from datatypes import OctetString
import random


class Session(Message):
    def __init__(self,
                 cmdflags,
                 cmdcode,
                 appId,
                 avps=list(),
                 hopByHopId=random.getrandbits(32),
                 endToEndId=random.getrandbits(32)):
        super().__init__(cmdflags, cmdcode, appId, avps, hopByHopId, endToEndId)
        self._sessionId = None
        self._avps.append(AVP(
            code=263,
            flags=0b0,
            data=OctetString(self._session)
        ))

    @property
    def sessionId(self):
        return self._sessionId

    @sessionId.setter
    def sessionId(self, val):
        self._sessionId = val
