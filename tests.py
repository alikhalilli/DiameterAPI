from datatypes.integer32 import Integer32
from datatypes.octetstring import OctetString
from datatypes.diamidentity import DiameterIdentity
from datatypes.group import Group
from message import Message
from datatypes.group import Group
from grouped import GroupedAVP
from scap import SCAPDef
from datatypes.address import Address
from datatypes.unsigned32 import Unsigned32
import socket
from abc import ABC, abstractmethod
import utils
import handler

flags = dict(
    Request=1 << 7,
    Proxiable=1 << 6,
    Error=1 << 5,
    Retransmitted=1 << 4,
    VendorSpecific=1 << 7,
    Mandatory=1 << 6,
    Protected=1 << 5)


if __name__ == "__main__":
    from avp import AVP, avpflags

    cer = utils.makeCER()

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '10.1.0.12'
    port = 3868
    client_sock.connect((host, port))
    count = 0

    hdr_handler = handler.HeaderHandler()

    while True:
        data = input("input:")
        client_sock.sendall(cer)
        from_server = client_sock.recv(1024)
        if from_server != b'':
            hdr_handler.handle(from_server)
        else:
            client_sock.close()

"""
    m = Message(
        cmdflags=flags['Request'],
        cmdcode=272,
        appId=4
    )
    m.addNewAVP(AVP(code=231,
                    flags=avpflags['vendor'] | avpflags['mandatory'],
                    vendorID=22,
                    data=Integer32(12)))
    m.addNewAVP(AVP(233,
                    flags=avpflags['vendor'],
                    vendorID=77,
                    data=OctetString("Salam")))
    m.addNewAVP(AVP(
        code=263,
        flags=avpflags['mandatory'],
        vendorID=None,
        data=OctetString("grump.example.com:33041;23432;893;0AF3B81")
    ))
    m.addNewAVP(
        AVP(
            code=263,
            flags=avpflags['mandatory'],
            vendorID=None,
            data=GroupedAVP(
                [
                    AVP(code=231,
                        flags=avpflags['vendor'] | avpflags['mandatory'],
                        vendorID=22,
                        data=Integer32(12)),
                    AVP(233,
                        flags=avpflags['vendor'],
                        vendorID=77,
                        data=OctetString("Salam")),
                    AVP(
                        code=263,
                        flags=avpflags['mandatory'],
                        vendorID=None,
                        data=OctetString(
                            "grump.example.com:33041;23432;893;0AF3B81")
                    )
                ]
            ))
    )"""
# print(m.decodeFromBytes(b'\x01\x00\x00\xcc\x80\x00\x01\x10\x00\x00\x00\x04\xae\x1c\x8a\xd7\x83W\x81\xad\x00\x00\x00\xe7\xc0\x00\x00\x10\x00\x00\x00\x16\x00\x00\x00\x0c\x00\x00\x00\xe9\x80\x00\x00\x11\x00\x00\x00MSalam\x00\x00\x00\x00\x00\x01\x07@\x00\x001grump.example.com:33041;23432;893;0AF3B81\x00\x00\x00\x00\x00\x01\x07@\x00\x00`\x00\x00\x00\xe7\xc0\x00\x00\x10\x00\x00\x00\x16\x00\x00\x00\x0c\x00\x00\x00\xe9\x80\x00\x00\x11\x00\x00\x00MSalam\x00\x00\x00\x00\x00\x01\x07@\x00\x001grump.example.com:33041;23432;893;0AF3B81\x00\x00\x00'))
"""    buff = b'\x01\x00\x01\x10'
    while buff:
        print(buff)
        buff = buff[1:]
    print(m.encode())"""
"""    a = AVP(231,
            flags=avpflags['vendor'] | avpflags['mandatory'],
            vendor=22,
            data=Integer32(12))
    b = AVP(232,
            flags=avpflags['mandatory'],
            vendor=333,
            data=Integer32(333))
    c = Integer32.decodeFromBytes(b'\x00\x00\x00\x0c')
    d = AVP(233,
            flags=avpflags['vendor'],
            vendor=77,
            data=OctetString("Salam"))
    di = AVP(234,
             flags=avpflags['vendor'],
             vendor=78,
             data=DiameterIdentity("aaa://host.example.com:6666;transport=tcp;protocol=diameter"))
    print(f"data: {a}")
    print(f"decoded: {c}")
    print(d)
    print(di)
    # print(b)"""
