import unittest
from datetime import date
from ..functions.date_helper import compare_dates_non_strict


class TestDate(unittest.TestCase):

    def test_valid_date_comparison(self):
        assert compare_dates_non_strict(date(year=1, month=1, day=1), '<', date(year=1, month=1, day=2))

    def test_invalid_date_comparison(self):
        assert compare_dates_non_strict(False, '<', date(year=1, month=1, day=2))
