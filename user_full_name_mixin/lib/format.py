from math import ceil
from typing import Union, Tuple

_NAME_FMT = "{first} {last}"


def format_name(first: Union[str, bool, None], last: Union[str, bool, None]) -> str:
    if not last:
        return first or ""
    if not first:
        return last
    return _NAME_FMT.format(first=first, last=last)


def decompose_name(name: str) -> Tuple[str, str]:
    """
    Decompose name in a simple way.
    This will obviously fail for "John Doe Jr" and the like, just accept this.
    @return (first_name, last_name,)
    """
    names = name.split(" ")
    num_names = len(names)
    if num_names < 1:
        return name, ""
    if num_names < 4:
        return " ".join(names[0:-1]), names[-1]
    num_names = ceil(num_names / 2)
    return " ".join(names[:num_names]), " ".join(names[num_names:])
