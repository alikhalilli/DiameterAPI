from .datatype import Type

"""
 The Diameter protocol allows AVP values of type 'Grouped.'  This
   implies that the Data field is actually a sequence of AVPs.  It is
   possible to include an AVP with a Grouped type within a Grouped type,
   that is, to nest them.  AVPs within an AVP of type Grouped have the
   same padding requirements as non-Grouped AVPs, as defined in Section
   4.
Calhoun, et al.             Standards Track                    [Page 49]
RFC 3588                Diameter Based Protocol           September 2003
   The AVP Code numbering space of all AVPs included in a Grouped AVP is
   the same as for non-grouped AVPs.  Further, if any of the AVPs
   encapsulated within a Grouped AVP has the 'M' (mandatory) bit set,
   the Grouped AVP itself MUST also include the 'M' bit set.
   Every Grouped AVP defined MUST include a corresponding grammar, using
   ABNF [ABNF] (with modifications), as defined below.
      grouped-avp-def  = name "::=" avp
      name-fmt         = ALPHA *(ALPHA / DIGIT / "-")
      name             = name-fmt
                         ; The name has to be the name of an AVP,
                         ; defined in the base or extended Diameter
                         ; specifications.
      avp              = header  [ *fixed] [ *required] [ *optional]
                         [ *fixed]
      header           = "<" "AVP-Header:" avpcode [vendor] ">"
      avpcode          = 1*DIGIT
                         ; The AVP Code assigned to the Grouped AVP
      vendor           = 1*DIGIT
                         ; The Vendor-ID assigned to the Grouped AVP.
                         ; If absent, the default value of zero is
                         ; used.
"""


class Grouped(Type):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def __len__(self):
        return len(self._value)

    def len(self):
        return self.__len__()

    def encode(self):
        return self._value

    def getpadding(self):
        return 0

    @staticmethod
    def decodeFromBuffer(buff):
        return Grouped(buff)
