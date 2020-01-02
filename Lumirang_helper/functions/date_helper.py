from datetime import date
import operator
from typing import Union

YEAR_MONTHS = 12
_OP = {
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
    '=': operator.eq,
    '!=': operator.ne
}
BEGINNING_OF_TIME = date(year=1, month=1, day=1)


def diff_month(d1: date, d2: date) -> int:
    """
    Calculate number of months between two dates.
    """
    return (d1.year - d2.year) * YEAR_MONTHS + d1.month - d2.month


def compare_dates_non_strict(date1: Union[date, bool, None], op: str, date2: Union[date, bool, None]) -> int:
    """
    Make a comparison between two dates. Accepts false in place of any date, casts it to the minimal date possible.
    :param date1: first date object, None or False.
    :param op: on of the following: >, >=, <, <=, =, !=.
    :param date2: second date object, None or False.
    :return: integer comparison result.
    """
    if op not in _OP.keys():
        raise ValueError("Unacceptable operator {}".format(op))
    fn = _OP[op]
    return fn(date1 or BEGINNING_OF_TIME, date2 or BEGINNING_OF_TIME)
