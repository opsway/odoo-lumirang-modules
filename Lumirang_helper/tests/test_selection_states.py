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

        self.assertListEqual([
            ('test', "Test",),
            ('second', "Second",),
            ('overridden', alt_name),
        ], States.states())
