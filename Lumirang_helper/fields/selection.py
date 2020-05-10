import re

from ..functions.states import SPLIT_REGEX


class StateValue(str):
    string = None


class State:
    def __init__(self, string=None):
        self._string = string
        self._name = None
        self._value = None

    def __get__(self, instance, owner):
        if self._value is None:
            if self._string is None:
                string = " ".join(y.capitalize() for y in SPLIT_REGEX.split(self._name))
            else:
                string = self._string
            self._value = StateValue(self._name)
            self._value.string = string
        return self._value

    def __set_name__(self, owner, name):
        self._name = name.lower()


class SelectionStates:
    _VALID_STATE_REGEX = re.compile(r"^[A-Z][A-Z_]+$")

    @classmethod
    def states(cls):
        states = (getattr(cls, x) for x in cls.__dict__ if cls._VALID_STATE_REGEX.match(x))
        return [(x, x.string) for x in states]
