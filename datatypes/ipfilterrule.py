import octetstring


"""
The IPFilterRule format is derived from the OctetString AVP Base
      Format.  It uses the ASCII charset.  Packets may be filtered based
      on the following information that is associated with it:

         Direction                          (in or out)
         Source and destination IP address  (possibly masked)
         Protocol
         Source and destination port        (lists or ranges)
         TCP flags
         IP fragment flag
         IP options
         ICMP types

      Rules for the appropriate direction are evaluated in order, with
      the first matched rule terminating the evaluation.  Each packet is
      evaluated once.  If no rule matches, the packet is dropped if the
      last rule evaluated was a permit, and passed if the last rule was
      a deny.
"""


class IPFilterRule(octetstring.OctetString):
    pass
