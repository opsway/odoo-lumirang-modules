import unittest

from ..functions.auto_attr import AutoAttr, AutoString


class TestAutoAttr(unittest.TestCase):
    def test_attr(self):
        class Test:
            V1 = AutoAttr()

        self.assertEqual("V1", Test.V1)

    def test_string(self):
        class Test:
            TEST_ATTR = AutoString()

        self.assertEqual("Test attr", Test.TEST_ATTR)
