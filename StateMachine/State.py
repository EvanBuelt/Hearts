import CardEngine.Engine as Cards
import Heart
import pygame
import CardEngine.CardLogging as CardLogging

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
        CardLogging.log_file.log('State: Initializing ' + name)
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
        CardLogging.log_file.log('SetupState: Setup enter')
        self.game.deck = Cards.CardEngine.create_deck(Heart.suits, Heart.values)
        self.game.shuffled_deck = Cards.CardEngine.shuffle(self.game.deck)
        CardLogging.log_file.log('SetupState: Size of deck: ' + str(len(self.game.deck)))
        CardLogging.log_file.log('SetupState: Size of shuffled deck: ' + str(len(self.game.shuffled_deck)))
        self.game.create_card_ui()
        self.game.setup_hands()
        self.game.player_one.sort_hand()
        self.game.player_two.sort_hand()
        self.game.player_three.sort_hand()
        self.game.player_four.sort_hand()
        self.game.setup_ui()
        self.game.hearts_broken = False

        self.next_state = "Passing"
        CardLogging.log_file.log('State: Set next state to Passing')

    def exit(self):
        CardLogging.log_file.log('SetupState: Setup exit')
        self.game.player_one.set_hand_owner()
        self.game.player_two.set_hand_owner()
        self.game.player_three.set_hand_owner()
        self.game.player_four.set_hand_owner()

        CardLogging.log_file.log('SetupState: Set next state to None')
        self.next_state = None

    def handle_keypress(self, event):
        CardLogging.log_file.log('SetupState: Keypress handled in Setup')
        return

    def handle_card_click(self, card_ui):
        CardLogging.log_file.log('SetupState: Card Click handled in Setup')
        return

    def update(self):
        CardLogging.log_file.log('SetupState: Setup update')
        return self.next_state


class PassingState(State):
    def __init__(self, game, name):
        State.__init__(self, game, name)
        self.passing_order = "Left"
        CardLogging.log_file.log('PassingState: Passing order set to ' + self.passing_order)
        # Passing states are 'Left', 'Right', 'Straight', 'None', in that order.

    def enter(self):

        CardLogging.log_file.log('PassingState: Passing enter')

        CardLogging.log_file.log('PassingState: Players passing hand set to empty list ')

        self.game.player_one.passing = []
        self.game.player_two_passing = []
        self.game.player_three_passing = []
        self.game.player_four_passing = []

        if self.passing_order is "None":
            self.passing_order = "Left"
            self.next_state = "Playing"

            CardLogging.log_file.log('PassingState: Passing order set to ' + self.passing_order)
            CardLogging.log_file.log('PassingState: Next state set to ' + self.next_state)

        return

    def exit(self):
        CardLogging.log_file.log('PassingState: Passing exit')

        self.game.player_one.set_hand_owner()
        self.game.player_two.set_hand_owner()
        self.game.player_three.set_hand_owner()
        self.game.player_four.set_hand_owner()

        CardLogging.log_file.log('PassingState: Set next state to None')
        self.next_state = None

    def handle_keypress(self, event):
        CardLogging.log_file.log('PassingState: Keypress handled in Passing')
        # Possible to have a card click before transition to the next state.
        if self.next_state is not None:
            return

        if event.type is pygame.KEYUP:
            if len(self.game.player_one.passing) is 3:
                self.passing_round()
                self.next_state = "Playing"

    def handle_card_click(self, card_ui):
        CardLogging.log_file.log('PassingState: Card click handled in Passing')
        # Possible to have a card click before transition to the next state.
        if self.next_state is not None:
            return

        card = card_ui.card

        if card in self.game.player_one.hand:
            if card not in self.game.player_one.passing:
                if len(self.game.player_one.passing) < 3:
                    CardLogging.log_file.log('PassingState: Move card up')
                    card_ui.move(0, -25, 0)
                    CardLogging.log_file.log('PassingState: Add card to passing hand')
                    self.game.player_one.passing.append(card)
            else:
                CardLogging.log_file.log('PassingState: Remove card from passing hand')
                self.game.player_one.passing.remove(card)
                CardLogging.log_file.log('PassingState: Move card down')
                card_ui.move(0, 25, 0)

    def update(self):
        return self.next_state

    def passing_round(self):
        CardLogging.log_file.log('PassingState: Pass cards')

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
            CardLogging.log_file.log('PassingState: Pass cards Left')

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
            CardLogging.log_file.log('PassingState: Pass cards Right')

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
            CardLogging.log_file.log('PassingState: Pass cards Across')

            Cards.CardEngine.transfer_cards(player_one_pass, player_one.hand, player_three.hand)
            Cards.CardEngine.transfer_cards(player_two_pass, player_two.hand, player_four.hand)
            Cards.CardEngine.transfer_cards(player_three_pass, player_three.hand, player_one.hand)
            Cards.CardEngine.transfer_cards(player_four_pass, player_four.hand, player_two.hand)

            # Human to computer two
            # Computer one to computer three
            # Computer two to Human
            # Computer three to computer one
            self.passing_order = "None"

        elif self.passing_order is "None":
            CardLogging.log_file.log('PassingState: Pass cards to None')
            self.passing_order = "Left"

            CardLogging.log_file.log('PassingState: Passing order set to ' + self.passing_order)

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

        CardLogging.log_file.log('PlayingState: Set current suit to Current Player')
        CardLogging.log_file.log('PlayingState: Set current suit to Clubs')
        CardLogging.log_file.log('PlayingState: Set trick pile to empty list')
        CardLogging.log_file.log('PlayingState: Set hearts broken to False')
        CardLogging.log_file.log('PlayingState: Set current card to None')

        self.currentPlayer = None
        self.currentSuit = Heart.suits_str["Clubs"]
        self.trickPile = []
        self.heartsBroken = False
        self.currentCard = None

        self.set_trick_pile_locations()

    def enter(self):

        CardLogging.log_file.log('PlayingState: Playing enter')

        CardLogging.log_file.log('PlayingState: Set current suit to Clubs')
        CardLogging.log_file.log('PlayingState: Set trick pile to empty list')
        CardLogging.log_file.log('PlayingState: Set hearts broken to False')
        CardLogging.log_file.log('PlayingState: Set current card to None')

        self.currentSuit = Heart.suits_str["Clubs"]
        self.trickPile = []
        self.heartsBroken = False
        self.currentCard = None

        for i in range(0, 13):
            CardLogging.log_file.log('PlayingState: Check card ' + str(i + 1) + ' is 2 of clubs P1 to P4')

            if self.game.player_one.hand[i].suit is Heart.suits_str["Clubs"] \
                    and self.game.player_one.hand[i].value is Heart.values_str["2"]:
                CardLogging.log_file.log('PlayingState: 2 of clubs found P1')
                self.currentPlayer = self.game.player_one

            elif self.game.player_two.hand[i].suit is Heart.suits_str["Clubs"] \
                    and self.game.player_two.hand[i].value is Heart.values_str["2"]:
                CardLogging.log_file.log('PlayingState: 2 of clubs found P2')
                self.currentPlayer = self.game.player_two

            elif self.game.player_three.hand[i].suit is Heart.suits_str["Clubs"] \
                    and self.game.player_three.hand[i].value is Heart.values_str["2"]:
                CardLogging.log_file.log('PlayingState: 2 of clubs found P3')
                self.currentPlayer = self.game.player_three

            elif self.game.player_four.hand[i].suit is Heart.suits_str["Clubs"] \
                    and self.game.player_four.hand[i].value is Heart.values_str["2"]:
                CardLogging.log_file.log('PlayingState: 2 of clubs found P4')
                self.currentPlayer = self.game.player_four
        # TO DO:
        # Set current player as player with 2 of clubs
        # Setup hearts not broken
        # Setup trick pile
        # Setup current suit as clubs

        return

    def exit(self):
        CardLogging.log_file.log('PlayingState: Playing exit')
        self.next_state = None

    def handle_keypress(self, event):
        CardLogging.log_file.log('PlayingState: Playing handle keypress')
        if self.currentPlayer is self.game.player_one:
            self.currentCard = self.currentPlayer.handle_keypress(event)
            if self.currentCard is not None:
                if self.currentSuit is None:
                    self.currentSuit = self.currentCard.card.suit

                self.move_card_to_trick_pile(self.currentCard.card)
                self.set_next_player()

                self.game.player_one.hand.remove(self.currentCard.card)
                self.currentCard = None
        return

    def handle_card_click(self, card_ui):
        CardLogging.log_file.log('PlayingState: Playing handle card click')
        if self.currentPlayer is self.game.player_one:
            self.currentPlayer.handle_card_click(card_ui, self.currentSuit)
        return

    def update(self):
        CardLogging.log_file.log('PlayingState: update')
        if len(self.trickPile) is 4:
            CardLogging.log_file.log('PlayingState: Trick pile has 4 cards')
            highest_card = self.find_highest_card()

            trick_player = highest_card.card.owner
            self.currentPlayer = highest_card.card.owner

            CardLogging.log_file.log('PlayingState: Trick player is ' + self.currentPlayer.name)
            CardLogging.log_file.log('PlayingState: Playing handle card click')

            while len(self.trickPile) > 0:


                card = self.trickPile[0]
                CardLogging.log_file.log('PlayingState: Transfer card: ' + str(card.value) + ' of ' + str(card.suit))
                Cards.CardEngine.transfer_card(card, self.trickPile, trick_player.tricks)

            self.currentSuit = None

        elif self.is_done():
            CardLogging.log_file.log('PlayingState: Setting next state to Scoring')
            self.next_state = "Scoring"

        elif self.currentPlayer is not self.game.player_one:
            CardLogging.log_file.log('PlayingState: Allow computer to play card')
            card = self.currentPlayer.play_card(self.currentSuit)

            if self.currentSuit is None:
                self.currentSuit = card.suit
                CardLogging.log_file.log('PlayingState: Set suit to ' + str(self.currentSuit))

            self.move_card_to_trick_pile(card)
            self.set_next_player()

        return self.next_state

    def set_trick_pile_locations(self):

        CardLogging.log_file.log('PlayingState: Set trick pile locations')

        # Size of card: 75w 105h
        # Size of screen: 800w 800h

        self.player_one_x = 362
        self.player_one_y = 400

        CardLogging.log_file.log('PlayingState: P1 ' + str(self.player_one_x) + ',' + str(self.player_one_y))

        self.player_two_x = 400
        self.player_two_y = 362

        CardLogging.log_file.log('PlayingState: P2 ' + str(self.player_two_x) + ',' + str(self.player_two_y))

        self.player_three_x = 438
        self.player_three_y = 400

        CardLogging.log_file.log('PlayingState: P3 ' + str(self.player_three_x) + ',' + str(self.player_three_y))

        self.player_four_x = 400
        self.player_four_y = 438

        CardLogging.log_file.log('PlayingState: P4 ' + str(self.player_four_x) + ',' + str(self.player_four_y))

        return

    def move_card_to_trick_pile(self, card):

        CardLogging.log_file.log('PlayingState: Move card to trick pile')

        for card_ui in self.game.card_ui_elements:
            if card is card_ui.card:
                self.trickPile.append(card_ui)
                if self.currentPlayer is self.game.player_one:
                    CardLogging.log_file.log('PlayingState: P1: ' + str(card.value) + ' of ' + str(card.suit))
                    card_ui.set_location(self.player_one_x, self.player_one_y)
                    card_ui.front_view = True

                if self.currentPlayer is self.game.player_two:
                    CardLogging.log_file.log('PlayingState: P2: ' + str(card.value) + ' of ' + str(card.suit))
                    card_ui.set_location(self.player_two_x, self.player_two_y)
                    card_ui.front_view = True

                elif self.currentPlayer is self.game.player_three:
                    CardLogging.log_file.log('PlayingState: P3: ' + str(card.value) + ' of ' + str(card.suit))
                    card_ui.set_location(self.player_three_x, self.player_three_y)
                    card_ui.front_view = True

                elif self.currentPlayer is self.game.player_four:
                    CardLogging.log_file.log('PlayingState: P4: ' + str(card.value) + ' of ' + str(card.suit))
                    card_ui.set_location(self.player_four_x, self.player_four_y)
                    card_ui.front_view = True
        return

    def set_next_player(self):

        if self.currentPlayer is self.game.player_one:
            CardLogging.log_file.log('PlayingState: Set next player to P4')
            self.currentPlayer = self.game.player_four

        elif self.currentPlayer is self.game.player_two:
            CardLogging.log_file.log('PlayingState: Set next player to P1')
            self.currentPlayer = self.game.player_one

        elif self.currentPlayer is self.game.player_three:
            CardLogging.log_file.log('PlayingState: Set next player to P2')
            self.currentPlayer = self.game.player_two

        elif self.currentPlayer is self.game.player_four:
            CardLogging.log_file.log('PlayingState: Set next player to P3')
            self.currentPlayer = self.game.player_three

    def find_highest_card(self):
        CardLogging.log_file.log('PlayingState: Find highest card')
        highest_card = None
        highest_value = -1

        for card_ui in self.trickPile:

            CardLogging.log_file.log('PlayingState: Set card location to 1200, 1200')
            CardLogging.log_file.log('PlayingState: Set card visible to false')
            card_ui.set_location(1200, 1200)
            card_ui.visible = False
            if card_ui.card.suit is self.currentSuit:
                if card_ui.card.value > highest_value:
                    CardLogging.log_file.log('PlayingState: Highest card of suit ' + str(self.currentSuit))
                    highest_card = card_ui
                    highest_value = card_ui.card.value
                    CardLogging.log_file.log('PlayingState: Value of card is ' + str(highest_value))

        return highest_card

    def is_done(self):
        CardLogging.log_file.log('PlayingState: Check if done')
        num_cards = 0
        num_cards += len(self.game.player_one.hand)
        num_cards += len(self.game.player_two.hand)
        num_cards += len(self.game.player_three.hand)
        num_cards += len(self.game.player_four.hand)

        CardLogging.log_file.log('PlayingState: Cards remaining: ' + str(num_cards))

        if num_cards is 0:
            CardLogging.log_file.log('PlayingState: No card found')
            return True

        else:
            CardLogging.log_file.log('PlayingState: Cards found')
            return False

    def player_select_card(self, card_ui):
        card = card_ui.card
        CardLogging.log_file.log('PlayingState: Move: ' + str(card.value) + ' of ' + str(card.suit) + ' up')
        card_ui.move(0, -25, 0)
        self.currentCard = card_ui
        return

    def player_deselect_card(self, card_ui):
        if self.currentCard is card_ui:
            if card_ui is not None:
                card = card_ui.card
                CardLogging.log_file.log('PlayingState: Move: ' + str(card.value) + ' of ' + str(card.suit) + ' down')
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

        player_one_round_points = self.get_points(self.game.player_one)
        player_two_round_points = self.get_points(self.game.player_two)
        player_three_round_points = self.get_points(self.game.player_three)
        player_four_round_points = self.get_points(self.game.player_four)

        CardLogging.log_file.log('ScoringState: P1 Temp Points: ' + str(player_one_round_points))
        CardLogging.log_file.log('ScoringState: P2 Temp Points: ' + str(player_two_round_points))
        CardLogging.log_file.log('ScoringState: P3 Temp Points: ' + str(player_three_round_points))
        CardLogging.log_file.log('ScoringState: P4 Temp Points: ' + str(player_four_round_points))

        if player_one_round_points is 26:
            CardLogging.log_file.log('ScoringState: P1 shot the moon')
            player_one_round_points = 0
            player_two_round_points = 26
            player_three_round_points = 26
            player_four_round_points = 26

        elif player_two_round_points is 26:
            CardLogging.log_file.log('ScoringState: P2 shot the moon')
            player_one_round_points = 26
            player_two_round_points = 0
            player_three_round_points = 26
            player_four_round_points = 26

        elif player_three_round_points is 26:
            CardLogging.log_file.log('ScoringState: P3 shot the moon')
            player_one_round_points = 26
            player_two_round_points = 26
            player_three_round_points = 0
            player_four_round_points = 26

        elif player_four_round_points is 26:
            CardLogging.log_file.log('ScoringState: P4 shot the moon')
            player_one_round_points = 26
            player_two_round_points = 26
            player_three_round_points = 26
            player_four_round_points = 0

        self.player_one_points += player_one_round_points
        self.player_two_points += player_two_round_points
        self.player_three_points += player_three_round_points
        self.player_four_points += player_four_round_points

        CardLogging.log_file.log('ScoringState: P1 Points: ' + str(self.player_one_points))
        CardLogging.log_file.log('ScoringState: P2 Points: ' + str(self.player_two_points))
        CardLogging.log_file.log('ScoringState: P3 Points: ' + str(self.player_three_points))
        CardLogging.log_file.log('ScoringState: P4 Points: ' + str(self.player_four_points))

        if self.any_player_lost():
            CardLogging.log_file.log('ScoringState: Setting next state to None.  A player lost')
            self.next_state = None

        else:
            CardLogging.log_file.log('ScoringState: Setting next state to Setup.')
            self.next_state = "Setup"
        return

    def exit(self):
        CardLogging.log_file.log('ScoringState: exit')
        CardLogging.log_file.log('ScoringState: set P1-P4 trick piles to empty list')
        self.game.player_one.tricks = []
        self.game.player_two.tricks = []
        self.game.player_three.tricks = []
        self.game.player_four.tricks = []
        self.next_state = None

    def handle_keypress(self, event):
        CardLogging.log_file.log('ScoringState: handle key press')
        return

    def handle_card_click(self, card_ui):
        CardLogging.log_file.log('ScoringState: handle card click')
        return

    def update(self):
        CardLogging.log_file.log('ScoringState: update')
        return self.next_state

    def any_player_lost(self):
        CardLogging.log_file.log('ScoringState: any player lost?')
        if self.player_one_points >= 100:
            CardLogging.log_file.log('ScoringState: P1 had 100 or more points')
            return True

        if self.player_two_points >= 100:
            CardLogging.log_file.log('ScoringState: P2 had 100 or more points')
            return True

        if self.player_three_points >= 100:
            CardLogging.log_file.log('ScoringState: P3 had 100 or more points')
            return True

        if self.player_four_points >= 100:
            CardLogging.log_file.log('ScoringState: P4 had 100 or more points')
            return True

        CardLogging.log_file.log('ScoringState: No player had 100 or more points')
        return False

    def determine_lowest_points(self):
        CardLogging.log_file.log('ScoringState: Determine lowest points')
        lowest_points = 150
        lowest_player = None

        if self.player_one_points < lowest_points:
            CardLogging.log_file.log('ScoringState: P1 less than ' + str(lowest_points))
            lowest_points = self.player_one_points
            lowest_player = self.game.player_one

        if self.player_two_points < lowest_points:
            CardLogging.log_file.log('ScoringState: P2 less than ' + str(lowest_points))
            lowest_points = self.player_two_points
            lowest_player = self.game.player_two

        if self.player_three_points < lowest_points:
            CardLogging.log_file.log('ScoringState: P3 less than ' + str(lowest_points))
            lowest_points = self.player_three_points
            lowest_player = self.game.player_three

        if self.player_four_points < lowest_points:
            CardLogging.log_file.log('ScoringState: P4 less than ' + str(lowest_points))
            lowest_points = self.player_three_points
            lowest_player = self.game.player_four

        CardLogging.log_file.log('ScoringState: Player with lowest points: ' + lowest_player.name)
        CardLogging.log_file.log('ScoringState: Points: ' + str(lowest_points))
        return lowest_player

    def get_points(self, player):
        points = 0
        for card_ui in player.tricks:
            card = card_ui.card
            if card.suit is Heart.suits_str["Hearts"]:
                CardLogging.log_file.log('ScoringState: Hearts found')
                points += 1
            elif card.suit is Heart.suits_str["Spades"]:
                if card.value is Heart.values_str["Queen"]:
                    CardLogging.log_file.log('ScoringState: Queen of Spades found')
                    points += 13

        CardLogging.log_file.log('ScoringState: ' + player.name + ': ' + str(points))
        return points
