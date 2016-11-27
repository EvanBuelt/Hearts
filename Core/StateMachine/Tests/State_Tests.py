import unittest
from Core import CardLogging
from Core.StateMachine import State


CardLogging.log_file.enabled = False


class MockGame(object):
    def __init__(self):
        return


class StateTests(unittest.TestCase):
    def test_init(self):
        mock_game = MockGame()
        base_state = State.State(mock_game, "Base State")
        self.assertEqual(base_state.game, mock_game)
        self.assertEqual(base_state.name, "Base State")
        self.assertEqual(base_state.next_state, None)

    def test_enter(self):
        mock_game = MockGame()
        base_state = State.State(mock_game, "Base State")
        self.assertRaises(State.InheritanceError, base_state.enter)

    def test_exit(self):
        mock_game = MockGame()
        base_state = State.State(mock_game, "Base State")
        self.assertRaises(State.InheritanceError, base_state.exit)

    def test_update(self):
        mock_game = MockGame()
        base_state = State.State(mock_game, "Base State")
        self.assertRaises(State.InheritanceError, base_state.update)

    def test_keypress(self):
        mock_game = MockGame()
        base_state = State.State(mock_game, "Base State")
        self.assertRaises(State.InheritanceError, base_state.handle_keypress, "a")

    def test_card_click(self):
        mock_game = MockGame()
        base_state = State.State(mock_game, "Base State")
        self.assertRaises(State.InheritanceError, base_state.handle_card_click, "B")