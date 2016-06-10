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
        if self.current_state is not None:
            self.current_state.exit()

        self.current_state = self.state_list.get(key)
        self.current_state.enter()
        return

    def handle_keypress(self, event):
        # print event.key
        self.current_state.handle_keypress(event)
        return

    def handle_card_click(self, card_ui):
        self.current_state.handle_card_click(card_ui)
        return

    def update(self):
        # print self.current_state.name
        key = self.current_state.update()
        next_state = self.state_list.get(key, None)
        if next_state is not None:
            self.current_state.exit()
            self.current_state = next_state
            self.current_state.enter()
        return
