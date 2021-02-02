import unittest
from datetime import date, datetime

import pytz

from ..functions.date_helper import compare_dates_non_strict, adjust_12am


class TestDate(unittest.TestCase):
    def test_valid_date_comparison(self):
        self.assertTrue(compare_dates_non_strict(date(year=1, month=1, day=1), '<', date(year=1, month=1, day=2)))

    def test_invalid_date_comparison(self):
        self.assertTrue(compare_dates_non_strict(False, '<', date(year=1, month=1, day=2)))

    def test_adjust_12am(self):
        d = datetime(year=2020, month=5, day=4, minute=5, hour=1)
        self.assertEqual(d, adjust_12am(d))

        d = datetime(year=2020, month=5, day=4)
        new_d = adjust_12am(d)
        self.assertNotEqual(d, new_d)
        self.assertEqual(3, new_d.day)
        self.assertEqual(5, new_d.month)
        self.assertEqual(2020, new_d.year)

        d = datetime(year=2020, month=5, day=4, minute=5, second=6)
        new_d = adjust_12am(d, ("hour",))
        self.assertNotEqual(d, new_d)
        self.assertEqual(3, new_d.day)
        self.assertEqual(5, new_d.month)
        self.assertEqual(2020, new_d.year)

        d = datetime(year=2020, month=5, day=4, tzinfo=pytz.timezone("Europe/Madrid"))
        new_d = adjust_12am(d)
        self.assertGreater(d, new_d)
        self.assertEqual(3, new_d.day)
        self.assertEqual(5, new_d.month)
        self.assertEqual(2020, new_d.year)
