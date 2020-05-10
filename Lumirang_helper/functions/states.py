import re
from typing import List, Iterable

SPLIT_REGEX = re.compile(r"[\s_]+")


def make_states(states: Iterable[str]) -> List[tuple]:
    """
    Creates list of states valid for fields.Selection.
    :param states: iterable of state ids, words separated with spaces or underscores, e.g. ["name_1", "name_2"].
    :return: list of tuples [("name_1", "Name 1"), ("name_2", "Name 2"), ...]
    """
    return [(x, " ".join(y.capitalize() for y in SPLIT_REGEX.split(x))) for x in states]
