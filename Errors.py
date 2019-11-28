class IntegerValueError(ValueError):
    pass


class OctetStringValueError(ValueError):
    pass


class TimeValueError(ValueError):
    pass


class FloatValueError(ValueError):
    pass


class GroupedAVPValueError(ValueError):
    pass


class UnsignedValueError(ValueError):
    pass


class CommandNotFoundException(Exception):
    def __init__(self, msg):
        self.msg = msg
