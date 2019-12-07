import re

_SPLIT_REGEX = re.compile(r"[\s_]+")


def make_states(states):
    return [(x, " ".join(y.capitalize() for y in _SPLIT_REGEX.split(x))) for x in states]
