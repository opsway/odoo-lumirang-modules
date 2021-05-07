from typing import Union, Tuple

_NAME_FMT = "{first} {last}"


def format_name(first: Union[str, bool, None], last: Union[str, bool, None]) -> str:
    if not last:
        return first or ""
    if not first:
        return last or ""
    return _NAME_FMT.format(first=first, last=last)


def decompose_name(name: str) -> Tuple[str, str]:
    """
    @return (first_name, last_name,)
    """
    names = name.split(" ")
    return " ".join(names[0:-1]), names[-1] if len(names) > 1 else ""
