from struct import pack, unpack
from binascii import hexlify, unhexlify


class Header:
    def __init__(self,
                 version,
                 msglength,
                 cmdflags,
                 cmdcode,
                 appId,
                 hopByHopId,
                 endToEndId):
        self._version = version
        self._msglength = msglength
        self._headerlength = 20
        self._cmdflags = cmdflags
        self._cmdcode = cmdcode
        self._appId = appId
        self._hopByhopId = hopByHopId
        self._endToEndId = endToEndId

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, val):
        self._version = val

    def decode(self, buff):
        if len(buff)/2 < self._headerlength:
            raise ValueError(f"Corrupted data {buff}")
        return Header(
            version=unpack('>B', buff[0]),
            msglength=unpack('>I', b'\x00' + buff[1:4]),
            cmdflags=unpack('>B', buff[4]),
            cmdcode=unpack('>I', b'\x00' + buff[5:8]),
            appId=unpack('>I', buff[8:12]),
            hopByHopId=unpack('>I', buff[12:16]),
            endToEndId=unpack('>I', buff[16:20])
        )
