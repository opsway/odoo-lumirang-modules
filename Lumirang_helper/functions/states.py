import re
from typing import List, Iterable

_SPLIT_REGEX = re.compile(r"[\s_]+")


def make_states(states: Iterable[str]) -> List[tuple]:
    """
    Creates list of states valid for fields.Selection.
    :param states: iterable of state ids, words separated with spaces or underscores, e.g. ["name_1", "name_2"].
    :return: list of tuples [("name_1", "Name 1"), ("name_2", "Name 2"), ...]
    """
    return [(x, " ".join(y.capitalize() for y in _SPLIT_REGEX.split(x))) for x in states]


class SelectionStates:
    _VALID_STATE_REGEX = re.compile(r"^[A-Z][A-Z_]+$")

    @classmethod
    def states(cls):
        fields = getattr(cls, '__ALL__', None)
        if not fields:
            fields = (x for x in dir(cls) if cls._VALID_STATE_REGEX.match(x))
        return make_states(fields)
