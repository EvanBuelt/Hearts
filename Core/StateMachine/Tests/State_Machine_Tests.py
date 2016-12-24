import unittest
from Core import CardLogging
from Core.StateMachine import State
from Core.StateMachine import StateMachine

CardLogging.log_file.enabled = False


class MockGame(object):
    def __init__(self):
        return


class MockState(State.State):
    def __init__(self, game, name):
        State.State.__init__(self, game, name)
        self.action = "Init"
        self.next_state = None

    def enter(self):
        self.action = "Enter"

    def exit(self):
        self.action = "Exit"

    def handle_keypress(self, event):
        self.action = "Handle Keypress"

    def handle_card_click(self, card_ui):
        self.action = "Handle Card Click"

    def update(self):
        self.action = "Update"


class StateMachineTests(unittest.TestCase):
    def test_setup(self):
        state_machine = StateMachine.StateMachine()

        # Verify current state is None, and state list is empty
        self.assertIsNone(state_machine.current_state)
        self.assertDictEqual(state_machine.state_list, {})

    def test_add_state(self):
        state_machine = StateMachine.StateMachine()

        # Mocking out game
        mock_game = MockGame()

        # Create Mock States
        state_one = MockState(mock_game, "State One")
        state_two = MockState(mock_game, "State Two")

        # Add states to state machine
        state_machine.add_state(state_one, "Initial")
        state_machine.add_state(state_two, "Secondary")

        # Verify current state is still none, but state list contains both states
        self.assertIsNone(state_machine.current_state)
        self.assertDictEqual(state_machine.state_list, {"Initial": state_one, "Secondary": state_two})

    def test_add_same_state(self):
        state_machine = StateMachine.StateMachine()

        # Mocking out game
        mock_game = MockGame()

        # Create Mock States
        state_one = MockState(mock_game, "State One")
        state_two = MockState(mock_game, "State Two")

        # Add state one and verify state list
        state_machine.add_state(state_one, "Initial")
        self.assertDictEqual(state_machine.state_list, {"Initial": state_one})

        # Attempt to add state one again
        state_machine.add_state(state_one, "Initial")
        self.assertDictEqual(state_machine.state_list, {"Initial": state_one})

        # Add second state
        state_machine.add_state(state_two, "Secondary")
        self.assertDictEqual(state_machine.state_list, {"Initial": state_one, "Secondary": state_two})

        # Attempt to add state one again
        state_machine.add_state(state_one, "Initial")
        self.assertDictEqual(state_machine.state_list, {"Initial": state_one, "Secondary": state_two})

    def test_remove_state(self):
        state_machine = StateMachine.StateMachine()

        # Mocking out game
        mock_game = MockGame()

        # Create Mock States
        state_one = MockState(mock_game, "State One")
        state_two = MockState(mock_game, "State Two")

        # Add both states to state machine
        state_machine.add_state(state_one, "Initial")
        state_machine.add_state(state_two, "Secondary")

        # Verify internals updated correctly
        self.assertIsNone(state_machine.current_state)
        self.assertDictEqual(state_machine.state_list, {"Initial": state_one, "Secondary": state_two})

        # Remove initial state and verify it was removed
        state_machine.remove_state("Initial")
        self.assertDictEqual(state_machine.state_list, {"Secondary": state_two})

    def test_remove_same_state(self):
        state_machine = StateMachine.StateMachine()

        # Mocking out game
        mock_game = MockGame()

        # Create Mock States
        state_one = MockState(mock_game, "State One")
        state_two = MockState(mock_game, "State Two")

        # Add both states to state machine
        state_machine.add_state(state_one, "Initial")
        state_machine.add_state(state_two, "Secondary")

        # Verify internals updated correctly
        self.assertIsNone(state_machine.current_state)
        self.assertDictEqual(state_machine.state_list, {"Initial": state_one, "Secondary": state_two})

        # Remove initial state and verify it was removed
        state_machine.remove_state("Initial")
        self.assertDictEqual(state_machine.state_list, {"Secondary": state_two})

        # Remove initial state and verify it was removed
        state_machine.remove_state("Initial")
        self.assertDictEqual(state_machine.state_list, {"Secondary": state_two})

    def test_add_and_remove_state(self):
        state_machine = StateMachine.StateMachine()

        # Mocking out game
        mock_game = MockGame()

        # Create Mock States
        state_one = MockState(mock_game, "State One")
        state_two = MockState(mock_game, "State Two")
        state_three = MockState(mock_game, "State Three")

        # Add states one and two to state machine
        state_machine.add_state(state_one, "Initial")
        state_machine.add_state(state_two, "Secondary")

        # Verify internals of state machine
        self.assertIsNone(state_machine.current_state)
        self.assertDictEqual(state_machine.state_list, {"Initial": state_one, "Secondary": state_two})

        # Remove state one and verify internals
        state_machine.remove_state("Initial")
        self.assertDictEqual(state_machine.state_list, {"Secondary": state_two})

        # Add state one and verify internals
        state_machine.add_state(state_one, "Initial")
        self.assertDictEqual(state_machine.state_list, {"Initial": state_one, "Secondary": state_two})

        # Add state three and verify internals
        state_machine.add_state(state_three, "Tertiary")
        self.assertDictEqual(state_machine.state_list, {"Initial": state_one, "Secondary": state_two,
                                                        "Tertiary": state_three})

    def test_set_initial_state(self):
        state_machine = StateMachine.StateMachine()

        # Mocking out game
        mock_game = MockGame()

        # Create Mock States
        state_one = MockState(mock_game, "State One")
        state_two = MockState(mock_game, "State Two")

        # Add states to state machine
        state_machine.add_state(state_one, "Initial")
        state_machine.add_state(state_two, "Secondary")

        # Set initial state to State One and verify
        state_machine.set_initial_state("Initial")
        self.assertEqual(state_machine.current_state, state_one)
        self.assertEqual(state_one.action, "Enter")
        self.assertEqual(state_two.action, "Init")

        # Set initial state to State Two and verify
        state_machine.set_initial_state("Secondary")
        self.assertEqual(state_machine.current_state, state_two)
        self.assertEqual(state_one.action, "Exit")
        self.assertEqual(state_two.action, "Enter")

    def test_handle_keypress(self):
        state_machine = StateMachine.StateMachine()

        # Mocking out game
        mock_game = MockGame()

        # Create Mock States
        state_one = MockState(mock_game, "State One")
        state_two = MockState(mock_game, "State Two")

        # Add states to state machine
        state_machine.add_state(state_one, "Initial")
        state_machine.add_state(state_two, "Secondary")

        # Set initial state to State One
        state_machine.set_initial_state("Initial")

        # Send keypress event to State Machine and verify
        state_machine.handle_keypress((2, 3,))
        self.assertEqual(state_one.action, "Handle Keypress")
        self.assertEqual(state_two.action, "Init")

    def test_handle_card_click(self):
        state_machine = StateMachine.StateMachine()

        # Mocking out game
        mock_game = MockGame()

        # Create Mock States
        state_one = MockState(mock_game, "State One")
        state_two = MockState(mock_game, "State Two")

        # Add states to state machine
        state_machine.add_state(state_one, "Initial")
        state_machine.add_state(state_two, "Secondary")

        # Set initial state to State One
        state_machine.set_initial_state("Initial")

        # Send keypress event to State Machine and verify
        state_machine.handle_card_click((2, 3))
        self.assertEqual(state_one.action, "Handle Card Click")
        self.assertEqual(state_two.action, "Init")

    def test_update(self):
        state_machine = StateMachine.StateMachine()

        # Mocking out game
        mock_game = MockGame()

        # Create Mock States
        state_one = MockState(mock_game, "State One")
        state_two = MockState(mock_game, "State Two")

        # Add states to state machine
        state_machine.add_state(state_one, "Initial")
        state_machine.add_state(state_two, "Secondary")

        # Send keypress event to State Machine and verify
        state_machine.update()
        self.assertEqual(state_one.action, "Init")
        self.assertEqual(state_two.action, "Init")

        # Set initial state to State One
        state_machine.set_initial_state("Initial")

        # Send keypress event to State Machine and verify
        state_machine.update()
        self.assertEqual(state_one.action, "Update")
        self.assertEqual(state_two.action, "Init")



