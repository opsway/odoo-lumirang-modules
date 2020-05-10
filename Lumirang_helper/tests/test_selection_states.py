import unittest

from ..fields.selection import SelectionStates, State


class TestSelectionStates(unittest.TestCase):
    def test_values(self):
        alt_name = "Alternative name"

        class States(SelectionStates):
            TEST = State()
            _NON_EXISTENT = State()
            SECOND = State()
            OVERRIDDEN = State(string=alt_name)

        self.assertEqual("test", States.TEST)
        self.assertEqual("second", States.SECOND)
        self.assertListEqual([
            (States.TEST, "Test",),
            (States.SECOND, "Second",),
            (States.OVERRIDDEN, alt_name),
        ], States.states())
