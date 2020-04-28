import unittest
import math
from ..functions.math_helper import round_half_up


class TestDate(unittest.TestCase):

    def test_round_half_up_low(self):
        # pylint: disable=no-self-use
        assert math.isclose(round_half_up(1.124, 2), 1.12, rel_tol=1e-04)

    def test_round_half_up_mid(self):
        # pylint: disable=no-self-use
        assert math.isclose(round_half_up(1.125, 2), 1.13, rel_tol=1e-04)

    def test_round_half_up_mid_high(self):
        # pylint: disable=no-self-use
        assert math.isclose(round_half_up(1.126, 2), 1.13, rel_tol=1e-04)