# InheritanceError is used to ensure certain class methods are inherited.
class InheritanceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class State:
    def __init__(self, name, game):
        self.name = name
        self.game = game
        return

    def enter(self):
        self.name = self.name
        raise InheritanceError("Enter method in state not defined.")

    def exit(self):
        self.name = self.name
        raise InheritanceError("Exit method in state not defined.")

    def handle_keypress(self, event):
        self.name = event
        raise InheritanceError("Keypress method in state not defined.")

    def handle_card_click(self, card_ui):
        self.name = card_ui
        raise InheritanceError("Card Click method in state not defined.")

    def update(self):
        self.name = self.name
        raise InheritanceError("Update method in state not defined.")


class SetupState(State):
    def __init__(self, name, game):
        State.__init__(self, name, game)


class PassingState(State):
    def __init__(self, name, game):
        State.__init__(self, name, game)


class PlayingState(State):
    def __init__(self, name, game):
        State.__init__(self, name, game)


class ScoringState(State):
    def __init__(self, name, game):
        State.__init__(self, name, game)


class StateMachine:
    def __init__(self):
        self.current_state = None
        self.state_list = {}
        return

    def add_state(self, state, key):
        if key not in self.state_list:
            self.state_list[key] = state
        return

    def remove_state(self, key):
        if key in self.state_list:
            self.state_list.pop(key, None)
        return

    def set_initial_state(self, key):
        self.current_state = self.state_list.get(key)
        return

    def handle_keypress(self, event):
        self.current_state.handle_keypress(event)
        return

    def handle_card_click(self, card_ui):
        self.current_state.handle_card_click(card_ui)
        return

    def update(self):
        key = self.current_state.update()
        next_state = self.state_list.get(key, None)
        if next_state is not None:
            self.current_state.exit()
            self.current_state = next_state
            self.current_state.enter()
        return
