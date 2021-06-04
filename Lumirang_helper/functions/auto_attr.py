import re
from typing import Callable

ParseFnType = Callable[[str], str]

SPLIT_REGEX = re.compile(r"[\s_]+")


def identity_name(name: str) -> str:
    return name


def readable_name(name: str) -> str:
    return " ".join(y for y in SPLIT_REGEX.split(name.lower())).capitalize()


class AutoAttr:
    def __init__(self, convert_name_fn: ParseFnType = identity_name):
        self.name = None
        self.convert_name = convert_name_fn
        self.value = None

    def _create_value(self):
        return self.convert_name(self.name)

    def __get__(self, instance, owner):
        if self.value is None:
            self.value = self._create_value()
        return self.value

    def __set_name__(self, owner, name):
        self.name = name


class AutoString(AutoAttr):
    def __init__(self, convert_name_fn: ParseFnType = readable_name):
        super().__init__(convert_name_fn)
