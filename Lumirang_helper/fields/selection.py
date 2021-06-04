import re

from ..functions.auto_attr import AutoAttr,SPLIT_REGEX


class StateValue(str):
    string = None


class State(AutoAttr):
    def __init__(self, string=None):
        super().__init__()
        self.string = string

    def _create_value(self):
        if self.string is None:
            self.string = " ".join(y.capitalize() for y in SPLIT_REGEX.split(self.name))
        value = StateValue(self.name)
        value.string = self.string
        return value

    def __set_name__(self, owner, name):
        self.name = name.lower()


class SelectionStates:
    _VALID_STATE_REGEX = re.compile(r"^[A-Z][A-Z_]+$")

    @classmethod
    def states(cls):
        states = (getattr(cls, x) for x in cls.__dict__ if cls._VALID_STATE_REGEX.match(x))
        return [(x, x.string) for x in states]
