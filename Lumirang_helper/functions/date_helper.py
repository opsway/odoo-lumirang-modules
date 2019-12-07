from datetime import date
import operator

YEAR_MONTHS = 12
_OP = {'>': operator.gt, '>=': operator.ge, '<': operator.lt, '<=': operator.le, '=': operator.eq, '!=': operator.ne}
_BEGINNING_OF_TIME = date(year=1, month=1, day=1)


def diff_month(d1, d2):
    """Calculate number of months between two dates"""
    return (d1.year - d2.year) * YEAR_MONTHS + d1.month - d2.month


def compare_dates_non_strict(date1, oper, date2):
    """Make a comparison between two date even if they are not of a datetime format"""
    if oper not in _OP.keys():
        raise ValueError("Unacceptable operator {}".format(oper))
    fn = _OP[oper]
    return fn(date1 or _BEGINNING_OF_TIME, date2 or _BEGINNING_OF_TIME)
