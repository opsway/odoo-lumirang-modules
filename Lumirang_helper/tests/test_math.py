import unittest
import math
from ..functions.math_helper import round_half_up


class TestMath(unittest.TestCase):

    def test_round_half_up(self):
        # pylint: disable=no-self-use
        for x, decimal, result in [
            (1.124, 2, 1.12),
            (1.125, 2, 1.13),
            (1.126, 2, 1.13),
            (0, 2, 0),
            (2, 2, 2),
            (12, 2, 12),
            (2, 0, 2),
            (2.5, 0, 3),
            (12.5, -1, 10),
        ]:
            self.assertAlmostEqual(round_half_up(x, decimal), result, 3,
                                   msg='Failed for input {}, output {} with decimal places {}'.format(x, result,
                                                                                                      decimal))

    def test_round_half_up_negative(self):
        # pylint: disable=no-self-use
        self.assertRaises(ValueError, lambda: math.isclose(round_half_up(-3, 2), 0, rel_tol=1e-04))
