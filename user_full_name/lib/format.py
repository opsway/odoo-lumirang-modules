from typing import Union

_NAME_FMT = "{first} {last}"


def format_name(first: Union[str, bool, None], last: Union[str, bool, None]) -> str:
    if not last:
        return first or ""
    if not first:
        return last or ""
    return _NAME_FMT.format(first=first, last=last)
