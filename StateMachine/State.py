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
        self.game.player_one.sort_hand()
        self.game.player_two.sort_hand()
        self.game.player_three.sort_hand()
        self.game.player_four.sort_hand()
        self.game.setup_ui()
        self.game.hearts_broken = False

        self.next_state = "Passing"

    def exit(self):
        self.game.player_one.set_hand_owner()
        self.game.player_two.set_hand_owner()
        self.game.player_three.set_hand_owner()
        self.game.player_four.set_hand_owner()
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
        self.game.player_one.set_hand_owner()
        self.game.player_two.set_hand_owner()
        self.game.player_three.set_hand_owner()
        self.game.player_four.set_hand_owner()
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
        player_two.pass_cards()
        player_three.pass_cards()
        player_four.pass_cards()

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

    # Data for playing the round
    currentPlayer = None
    currentSuit = None
    trickPile = []
    heartsBroken = False
    currentCard = None

    # Data for where each player places card for trick pile
    player_one_x = 0
    player_one_y = 0
    player_two_x = 0
    player_two_y = 0
    player_three_x = 0
    player_three_y = 0
    player_four_x = 0
    player_four_y = 0

    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.currentPlayer = None
        self.currentSuit = "Club"
        self.trickPile = []
        self.heartsBroken = False
        self.currentCard = None

        self.set_trick_pile_locations()

    def enter(self):

        self.currentSuit = Heart.suits_str["Clubs"]
        self.trickPile = []
        self.heartsBroken = False

        for i in range(0, 13):
            if self.game.player_one.hand[i].suit is Heart.suits_str["Clubs"] \
                    and self.game.player_one.hand[i].value is Heart.values_str["2"]:
                self.currentPlayer = self.game.player_one

            elif self.game.player_two.hand[i].suit is Heart.suits_str["Clubs"] \
                    and self.game.player_two.hand[i].value is Heart.values_str["2"]:
                self.currentPlayer = self.game.player_two

            elif self.game.player_three.hand[i].suit is Heart.suits_str["Clubs"] \
                    and self.game.player_three.hand[i].value is Heart.values_str["2"]:
                self.currentPlayer = self.game.player_three

            elif self.game.player_four.hand[i].suit is Heart.suits_str["Clubs"] \
                    and self.game.player_four.hand[i].value is Heart.values_str["2"]:
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
            self.currentCard = self.currentPlayer.handle_keypress(event)
            if self.currentCard is not None:
                self.move_card_to_trick_pile(self.currentCard.card)
                self.set_next_player()

                self.game.player_one.hand.remove(self.currentCard.card)
                self.currentCard = None
        return

    def handle_card_click(self, card_ui):
        if self.currentPlayer is self.game.player_one:
            self.currentPlayer.handle_card_click(card_ui, self.currentSuit)
        return

    def update(self):
        if len(self.trickPile) is 4:
            highest_card = self.find_highest_card()

            trick_player = highest_card.card.owner

            while len(self.trickPile) > 0:
                card = self.trickPile[0]
                Cards.CardEngine.transfer_card(card, self.trickPile, trick_player.tricks)

            self.currentSuit = None

        elif self.is_done():
            self.next_state = "Scoring"

        elif self.currentPlayer is not self.game.player_one:
            card = self.currentPlayer.play_card(self.currentSuit)

            if self.currentSuit is None:
                self.currentSuit = card.suit

            self.move_card_to_trick_pile(card)
            self.set_next_player()

        return self.next_state

    def set_trick_pile_locations(self):

        # Size of card: 75w 105h
        # Size of screen: 800w 800h

        self.player_one_x = 362
        self.player_one_y = 400

        self.player_two_x = 400
        self.player_two_y = 362

        self.player_three_x = 438
        self.player_three_y = 400

        self.player_four_x = 400
        self.player_four_y = 438
        return

    def move_card_to_trick_pile(self, card):
        for card_ui in self.game.card_ui_elements:
            if card is card_ui.card:
                self.trickPile.append(card_ui)
                if self.currentPlayer is self.game.player_one:
                    card_ui.set_location(self.player_one_x, self.player_one_y)
                    card_ui.front_view = True

                if self.currentPlayer is self.game.player_two:
                    card_ui.set_location(self.player_two_x, self.player_two_y)
                    card_ui.front_view = True

                elif self.currentPlayer is self.game.player_three:
                    card_ui.set_location(self.player_three_x, self.player_three_y)
                    card_ui.front_view = True

                elif self.currentPlayer is self.game.player_four:
                    card_ui.set_location(self.player_four_x, self.player_four_y)
                    card_ui.front_view = True
        return

    def set_next_player(self):
        if self.currentPlayer is self.game.player_one:
            self.currentPlayer = self.game.player_four

        elif self.currentPlayer is self.game.player_two:
            self.currentPlayer = self.game.player_one

        elif self.currentPlayer is self.game.player_three:
            self.currentPlayer = self.game.player_two

        elif self.currentPlayer is self.game.player_four:
            self.currentPlayer = self.game.player_three

    def find_highest_card(self):
        highest_card = None
        highest_value = -1

        for card_ui in self.trickPile:
            card_ui.set_location(1200, 1200)
            card_ui.visible = False
            if card_ui.card.suit is self.currentSuit:
                if (card_ui.card.value % 14) > highest_value:
                    highest_card = card_ui

        return highest_card

    def is_done(self):
        num_cards = 0
        num_cards += len(self.game.player_one.hand)
        num_cards += len(self.game.player_two.hand)
        num_cards += len(self.game.player_three.hand)
        num_cards += len(self.game.player_four.hand)

        if num_cards is 0:
            return True

        else:
            return False

    def player_select_card(self, card_ui):
        card_ui.move(0, -25, 0)
        self.currentCard = card_ui
        return

    def player_deselect_card(self, card_ui):
        if self.currentCard is card_ui:
            if card_ui is not None:
                card_ui.move(0, 25, 0)
            self.currentCard = None
        return


class ScoringState(State):

    player_one_points = 0
    player_two_points = 0
    player_three_points = 0
    player_four_points = 0

    def __init__(self, game, name):
        State.__init__(self, game, name)

    def enter(self):
        # Evaluate points each player receives as follows:
        #   Heart: 1 point
        #   Queen of Spades: 13 points
        #   Shooting the moon: One player gets all hearts and Queen of Spades
        #       All other players receive 26 points
        # Determine if anyone has 100 points or more
        #   Determine winner: Lowest

        player_one_temp_points = self.get_points(self.game.player_one)
        player_two_temp_points = self.get_points(self.game.player_two)
        player_three_temp_points = self.get_points(self.game.player_three)
        player_four_temp_points = self.get_points(self.game.player_four)

        if player_one_temp_points is 26:
            player_one_temp_points = 0
            player_two_temp_points = 26
            player_three_temp_points = 26
            player_four_temp_points = 26

        elif player_two_temp_points is 26:
            player_one_temp_points = 26
            player_two_temp_points = 0
            player_three_temp_points = 26
            player_four_temp_points = 26

        elif player_three_temp_points is 26:
            player_one_temp_points = 26
            player_two_temp_points = 26
            player_three_temp_points = 0
            player_four_temp_points = 26

        elif player_four_temp_points is 26:
            player_one_temp_points = 26
            player_two_temp_points = 26
            player_three_temp_points = 26
            player_four_temp_points = 0

        self.player_one_points += player_one_temp_points
        self.player_two_points += player_two_temp_points
        self.player_three_points += player_three_temp_points
        self.player_four_points += player_four_temp_points

        print self.player_one_points
        print self.player_two_points
        print self.player_three_points
        print self.player_four_points

        return

    def exit(self):
        self.next_state = None

    def handle_keypress(self, event):
        return

    def handle_card_click(self, card_ui):
        return

    def update(self):
        return self.next_state

    def get_points(self, player):
        points = 0
        for card_ui in player.tricks:
            card = card_ui.card
            if card.suit is Heart.suits_str["Hearts"]:
                points += 1
            elif card.suit is Heart.suits_str["Spades"]:
                if card.value is Heart.values_str["Queen"]:
                    points += 13

        return points
