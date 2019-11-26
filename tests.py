from avp import AVP, avpflags
from datatypes.integer32 import Integer32
from datatypes.octetstring import OctetString
from datatypes.diamidentity import DiameterIdentity
from message import Message


flags = dict(
    Request=1 << 7,
    Proxiable=1 << 6,
    Error=1 << 5,
    Retransmitted=1 << 4,
    VendorSpecific=1 << 7,
    Mandatory=1 << 6,
    Protected=1 << 5)

if __name__ == "__main__":

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
    print(m.encode())
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
