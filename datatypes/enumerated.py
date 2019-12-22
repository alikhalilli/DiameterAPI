from .integer32 import Integer32

"""
 Enumerated
      Enumerated is derived from the Integer32 AVP Base Format.  The
      definition contains a list of valid values and their
      interpretation and is described in the Diameter application
      introducing the AVP.
"""


class Enumerated(Integer32):
    pass
