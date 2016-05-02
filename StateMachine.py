import CardEngine.Engine as Cards
import Heart
import pygame


# InheritanceError is used to ensure certain class methods are inherited.
class InheritanceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class State:
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.next_state = None
        return

    def enter(self):
        raise InheritanceError("Enter method in state not defined.")

    def exit(self):
        raise InheritanceError("Exit method in state not defined.")

    def handle_keypress(self, event):
        raise InheritanceError("Keypress method in state not defined.")

    def handle_card_click(self, card_ui):
        raise InheritanceError("Card Click method in state not defined.")

    def update(self):
        raise InheritanceError("Update method in state not defined.")


class SetupState(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)

    def enter(self):
        self.game.deck = Cards.CardEngine.create_deck(Heart.suits, Heart.values)
        self.game.shuffled_deck = Cards.CardEngine.shuffle(self.game.deck)
        self.game.create_card_ui()
        self.game.setup_hands()
        self.game.setup_ui()
        self.game.hearts_broken = False

        self.next_state = "Passing"

    def exit(self):
        self.next_state = None

    def handle_keypress(self, event):
        return

    def handle_card_click(self, card_ui):
        return

    def update(self):
        return self.next_state


class PassingState(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.passing_order = "Left"
        # Passing states are 'Left', 'Right', 'Straight', 'None', in that order.

    def enter(self):
        if self.passing_order is "None":
            self.passing_order = "Left"
            self.next_state = "Playing"
        return

    def exit(self):
        self.next_state = None

    def handle_keypress(self, event):
        # Possible to have a card click before transition to the next state.
        if self.next_state is not None:
            return

        if event.type is pygame.KEYUP:
            if len(self.game.player_one.passing) is 3:
                self.passing_round()
                self.next_state = "Playing"

    def handle_card_click(self, card_ui):
        # Possible to have a card click before transition to the next state.
        if self.next_state is not None:
            return

        card = card_ui.card

        if card in self.game.player_one.hand:
            if card not in self.game.player_one.passing:
                if len(self.game.player_one.passing) < 3:
                    card_ui.move(0, -25, 0)
                    self.game.player_one.passing.append(card)
            else:
                self.game.player_one.passing.remove(card)
                card_ui.move(0, 25, 0)

    def update(self):
        return self.next_state

    def passing_round(self):

        # Syntactic sugar
        player_one = self.game.player_one
        player_two = self.game.player_two
        player_three = self.game.player_three
        player_four = self.game.player_four

        # Since player one (Human player) has already chosen their cards, have ai choose cards.
        player_two.ai.pass_cards(player_two)
        player_three.ai.pass_cards(player_three)
        player_four.ai.pass_cards(player_four)

        # Syntactic sugar for cards to pass
        player_one_pass = player_one.passing
        player_two_pass = player_two.passing
        player_three_pass = player_three.passing
        player_four_pass = player_four.passing

        if self.passing_order is "Left":

            Cards.CardEngine.transfer_cards(player_one_pass, player_one.hand, player_two.hand)
            Cards.CardEngine.transfer_cards(player_two_pass, player_two.hand, player_three.hand)
            Cards.CardEngine.transfer_cards(player_three_pass, player_three.hand, player_four.hand)
            Cards.CardEngine.transfer_cards(player_four_pass, player_four.hand, player_one.hand)

            # Human to computer one
            # Computer one to computer two
            # Computer two to computer three
            # Computer three to Human
            self.passing_order = "Right"

        elif self.passing_order is "Right":

            Cards.CardEngine.transfer_cards(player_one_pass, player_one.hand, player_four.hand)
            Cards.CardEngine.transfer_cards(player_two_pass, player_two.hand, player_one.hand)
            Cards.CardEngine.transfer_cards(player_three_pass, player_three.hand, player_two.hand)
            Cards.CardEngine.transfer_cards(player_four_pass, player_four.hand, player_three.hand)

            # Human to computer three
            # Computer one to Human
            # Computer two to computer one
            # Computer three to computer two
            self.passing_order = "Straight"

        elif self.passing_order is "Straight":

            Cards.CardEngine.transfer_cards(player_one_pass, player_one.hand, player_three.hand)
            Cards.CardEngine.transfer_cards(player_two_pass, player_two.hand, player_four.hand)
            Cards.CardEngine.transfer_cards(player_three_pass, player_three.hand, player_one.hand)
            Cards.CardEngine.transfer_cards(player_four_pass, player_four.hand, player_four.hand)

            # Human to computer two
            # Computer one to computer three
            # Computer two to Human
            # Computer three to computer one
            self.passing_order = "None"

        elif self.passing_order is "None":
            self.passing_order = "Left"

        player_one.sort_hand()
        player_two.sort_hand()
        player_three.sort_hand()
        player_four.sort_hand()

        self.game.setup_ui()
        return


class PlayingState(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.currentPlayer = None
        self.currentSuit = "Club"
        self.trickPile = []
        self.heartsBroken = False
        self.currentCard = None

        self.player_one_x = 25
        self.player_one_y = 25

        self.player_two_x = 125
        self.player_two_y = 125

        self.player_three_x = 225
        self.player_three_y = 225

        self.player_four_x = 325
        self.player_four_y = 325

    def enter(self):

        self.currentSuit = "Club"
        self.trickPile = []
        self.heartsBroken = False

        for i in range(0, 13):
            if self.game.player_one.hand[i].suit is 1 and self.game.player_one.hand[i].value is 2:
                self.currentPlayer = self.game.player_one

            elif self.game.player_two.hand[i].suit is 1 and self.game.player_two.hand[i].value is 2:
                self.currentPlayer = self.game.player_two

            elif self.game.player_three.hand[i].suit is 1 and self.game.player_three.hand[i].value is 2:
                self.currentPlayer = self.game.player_three

            elif self.game.player_four.hand[i].suit is 1 and self.game.player_four.hand[i].value is 2:
                self.currentPlayer = self.game.player_four
        # TO DO:
        # Set current player as player with 2 of clubs
        # Setup hearts not broken
        # Setup trick pile
        # Setup current suit as clubs

        return

    def exit(self):
        self.next_state = None

    def handle_keypress(self, event):
        if self.currentPlayer is self.game.player_one:
            if self.currentCard is not None:
                self.trickPile.append(self.currentCard)
                self.currentCard = None
                self.currentPlayer = self.game.player_two

        # Check if current turn
        #   Check if card is selected
        #       Place card in trick pile
        #       Let next player play card
        return

    def handle_card_click(self, card_ui):
        if self.currentPlayer is self.game.player_one:
            if card_ui.card in self.game.player_one.hand:
                if card_ui is self.currentCard:
                    card_ui.move(0, 25, 0)
                    self.currentCard = None
                else:
                    if self.currentCard is not None:
                        self.currentCard.move(0, 25, 0)
                    card_ui.move(0, -25, 0)
                    self.currentCard = card_ui
        # Check if card is in player's hand
        #   Check if card is valid to play
        #       Update selected card
        return

    def update(self):
        if len(self.trickPile) is 4:
            return

        if self.currentPlayer is not self.game.player_one:
            card = self.currentPlayer.ai.play_card(self.currentSuit)
            self.trickPile.append(card)

            for card_ui in self.game.card_ui_elements:
                if card is card_ui.card:
                    if self.currentPlayer is self.game.player_two:
                        card_ui.set_location(25, 25)

                    elif self.currentPlayer is self.game.player_three:
                        card_ui.set_location(50, 50)

                    elif self.currentPlayer is self.game.player_four:
                        card_ui.set_location(75, 75)

            if self.currentPlayer is self.game.player_two:
                self.currentPlayer = self.game.player_three

            elif self.currentPlayer is self.game.player_three:
                self.currentPlayer = self.game.player_four

            elif self.currentPlayer is self.game.player_four:
                self.currentPlayer = self.game.player_one

        # If computer player can play a card, let computer play card
        # If all players have played a card, evaluate to see who won trick pile
        #   Determine if hearts were played.
        #       If so, update hearts_broken to True
        #   Place center trick pile into players trick pile
        #
        return self.next_state


class ScoringState(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)

    def enter(self):
        # Evaluate points each player receives as follows:
        #   Heart: 1 point
        #   Queen of Spades: 13 points
        #   Shooting the moon: One player gets all hearts and Queen of Spades
        #       All other players receive 26 points
        # Determine if anyone has 100 points or more
        #   Determine winner: Lowest Points
        return

    def exit(self):
        self.next_state = None

    def handle_keypress(self, event):
        return

    def handle_card_click(self, card_ui):
        return

    def update(self):
        return self.next_state


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
        print event.key
        self.current_state.handle_keypress(event)
        return

    def handle_card_click(self, card_ui):
        self.current_state.handle_card_click(card_ui)
        return

    def update(self):
        print self.current_state.name
        key = self.current_state.update()
        next_state = self.state_list.get(key, None)
        if next_state is not None:
            self.current_state.exit()
            self.current_state = next_state
            self.current_state.enter()
        return
