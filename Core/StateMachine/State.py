import pygame
from CardEngine import Engine as Cards
from CardEngine import UI
from Core import CardLogging
from Core import Constant


# InheritanceError is used to ensure certain class methods are inherited.
class InheritanceError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class State(object):
    def __init__(self, game, name):
        CardLogging.log_file.log('---State __init__() enter---')
        self.game = game
        self.name = name
        self.next_state = None
        CardLogging.log_file.log('State: Initializing ' + name)
        CardLogging.log_file.log('---State __init__() exit---')
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
        CardLogging.log_file.log('---SetupState __init__() enter---')
        State.__init__(self, game, name)
        self.card_values = [Constant.Value.Two,
                            Constant.Value.Three,
                            Constant.Value.Four,
                            Constant.Value.Five,
                            Constant.Value.Six,
                            Constant.Value.Seven,
                            Constant.Value.Eight,
                            Constant.Value.Nine,
                            Constant.Value.Ten,
                            Constant.Value.Jack,
                            Constant.Value.Queen,
                            Constant.Value.King,
                            Constant.Value.Ace]

        self.card_suits = [Constant.Suit.Clubs,
                           Constant.Suit.Diamonds,
                           Constant.Suit.Spades,
                           Constant.Suit.Hearts]

        # Deck is only referenced to create shuffled deck. Only needs to be created once.
        self.game.deck = Cards.CardEngine.create_deck(self.card_suits, self.card_values)
        self.game.create_card_ui()
        self.shuffled_deck = []

        CardLogging.log_file.log('---SetupState __init__() exit---')

    def enter(self):
        CardLogging.log_file.log('---SetupState enter() enter---')
        self.shuffled_deck = Cards.CardEngine.shuffle(self.game.deck)
        CardLogging.log_file.log('SetupState: Size of deck: ' + str(len(self.game.deck)))
        CardLogging.log_file.log('SetupState: Size of shuffled deck: ' + str(len(self.shuffled_deck)))
        self.setup_hands()
        self.game.setup_ui()
        self.game.hearts_broken = False

        self.next_state = "Passing"
        CardLogging.log_file.log('State: Set next state to Passing')
        CardLogging.log_file.log('---SetupState enter() exit---')

    def exit(self):
        CardLogging.log_file.log('---SetupState exit() enter---')

        CardLogging.log_file.log('SetupState: Set next state to None')
        self.next_state = None
        CardLogging.log_file.log('---SetupState exit() exit---')

    def handle_keypress(self, event):
        CardLogging.log_file.log('---SetupState handle_keypress() enter---')
        CardLogging.log_file.log('---SetupState handle_keypress() exit---')
        return

    def handle_card_click(self, card_ui):
        CardLogging.log_file.log('---SetupState handle_card_click() enter---')
        CardLogging.log_file.log('---SetupState handle_card_click() exit---')
        return

    def update(self):
        CardLogging.log_file.log('---SetupState update() enter---')
        CardLogging.log_file.log('---SetupState update() exit---')
        return self.next_state

    def setup_hands(self):
        for i in range(0, 13):
            Cards.CardEngine.deal_cards(self.shuffled_deck, self.game.player_one.hand, 1)
            Cards.CardEngine.deal_cards(self.shuffled_deck, self.game.player_two.hand, 1)
            Cards.CardEngine.deal_cards(self.shuffled_deck, self.game.player_three.hand, 1)
            Cards.CardEngine.deal_cards(self.shuffled_deck, self.game.player_four.hand, 1)

        self.game.player_one.set_hand_owner()
        self.game.player_two.set_hand_owner()
        self.game.player_three.set_hand_owner()
        self.game.player_four.set_hand_owner()

        self.game.player_one.sort_hand()
        self.game.player_two.sort_hand()
        self.game.player_three.sort_hand()
        self.game.player_four.sort_hand()


class PassingState(State):
    def __init__(self, game, name):
        CardLogging.log_file.log('---PassingState __init__() enter---')
        State.__init__(self, game, name)
        self.passing_order = "Left"
        CardLogging.log_file.log('PassingState: Passing order set to ' + self.passing_order)
        CardLogging.log_file.log('---PassingState __init__() exit---')
        # Passing states are 'Left', 'Right', 'Straight', 'None', in that order.

    def enter(self):
        CardLogging.log_file.log('---PassingState enter() enter---')

        CardLogging.log_file.log('PassingState: Players passing hand set to empty list ')

        self.game.player_one.passing = []
        self.game.player_two.passing = []
        self.game.player_three.passing = []
        self.game.player_four.passing = []

        if self.passing_order is "None":
            self.get_next_passing()
            self.next_state = "Playing"

            CardLogging.log_file.log('PassingState: Passing order set to ' + self.passing_order)
            CardLogging.log_file.log('PassingState: Next state set to ' + self.next_state)

        CardLogging.log_file.log('---PassingState enter() exit---')
        return

    def exit(self):
        CardLogging.log_file.log('---PassingState exit() enter---')

        self.game.player_one.set_hand_owner()
        self.game.player_two.set_hand_owner()
        self.game.player_three.set_hand_owner()
        self.game.player_four.set_hand_owner()

        self.game.player_one.sort_hand()
        self.game.player_two.sort_hand()
        self.game.player_three.sort_hand()
        self.game.player_four.sort_hand()

        self.game.setup_ui()

        CardLogging.log_file.log('PassingState: Set next state to None')
        self.next_state = None
        CardLogging.log_file.log('---PassingState exit() exit---')

    def handle_keypress(self, event):
        CardLogging.log_file.log('---PassingState handle_keypress() enter---')
        CardLogging.log_file.log('PassingState: Keypress handled in Passing')
        # Possible to have a card click before transition to the next state.
        if self.next_state is not None:
            CardLogging.log_file.log('---PassingState handle_keypress() exit---')
            return

        if event.type is pygame.KEYUP:
            if len(self.game.player_one.passing) is 3:
                self.passing_round()
                self.next_state = "Playing"
        CardLogging.log_file.log('---PassingState handle_keypress() exit---')

    def handle_card_click(self, card_ui):
        CardLogging.log_file.log('---PassingState handle_card_click() enter---')
        CardLogging.log_file.log('PassingState: Card click handled in Passing')
        # Possible to have a card click before transition to the next state.
        if self.next_state is not None:
            CardLogging.log_file.log('---PassingState handle_card_click() exit---')
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
        CardLogging.log_file.log('---PassingState handle_card_click() exit---')

    def update(self):
        # CardLogging.log_file.log('---PassingState update() enter---')
        # CardLogging.log_file.log('---PassingState update() exit---')
        return self.next_state

    def passing_round(self):
        CardLogging.log_file.log('---PassingState passing_round() enter---')
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

        CardLogging.log_file.log('PassingState: P1 has ' + str(len(player_one.passing)) + ' passing cards')
        CardLogging.log_file.log('PassingState: P2 has ' + str(len(player_two.passing)) + ' passing cards')
        CardLogging.log_file.log('PassingState: P3 has ' + str(len(player_three.passing)) + ' passing cards')
        CardLogging.log_file.log('PassingState: P4 has ' + str(len(player_four.passing)) + ' passing cards')

        # Syntactic sugar for cards to pass
        player_one_pass = player_one.passing
        player_two_pass = player_two.passing
        player_three_pass = player_three.passing
        player_four_pass = player_four.passing

        '''
        print ""
        print "Pass 1"
        print ""

        for card in player_one_pass:
            print Constant.suit_str[card.suit], Constant.value_str[card.value]

        print ""
        print "Hands 1"
        print ""

        for card in player_one.hand:
            print Constant.suit_str[card.suit], Constant.value_str[card.value]

        print ""
        print "Pass 2"
        print ""

        for card in player_two_pass:
            print Constant.suit_str[card.suit], Constant.value_str[card.value]

        print ""
        print "Hands 2"
        print ""

        for card in player_two.hand:
            print Constant.suit_str[card.suit], Constant.value_str[card.value]

        print ""
        print "Pass 3"
        print ""

        for card in player_three_pass:
            print Constant.suit_str[card.suit], Constant.value_str[card.value]

        print ""
        print "Hands 3"
        print ""

        for card in player_three.hand:
            print Constant.suit_str[card.suit], Constant.value_str[card.value]

        print ""
        print "Pass 4"
        print ""

        for card in player_four_pass:
            print Constant.suit_str[card.suit], Constant.value_str[card.value]

        print ""
        print "Hands 4"
        print ""

        for card in player_four.hand:
            print Constant.suit_str[card.suit], Constant.value_str[card.value]

        print ""
        print len(player_one_pass)
        print len(player_two_pass)
        print len(player_three_pass)
        print len(player_four_pass)
        print ""
        print len(player_one.hand)
        print len(player_two.hand)
        print len(player_three.hand)
        print len(player_four.hand)
        print ""
        print self.passing_order
        print ""
        '''

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

        elif self.passing_order is "None":
            CardLogging.log_file.log('PassingState: Pass cards to None')

        self.get_next_passing()

        '''
        print len(player_one_pass)
        print len(player_two_pass)
        print len(player_three_pass)
        print len(player_four_pass)
        print ""
        print len(player_one.hand)
        print len(player_two.hand)
        print len(player_three.hand)
        print len(player_four.hand)
        print ""
        print self.passing_order
        print ""
        '''

        CardLogging.log_file.log('---PassingState passing_round() exit---')
        return

    def get_next_passing(self):
        if self.passing_order is "None":
            self.passing_order = "Left"
            self.next_state = "Playing"

        elif self.passing_order is "Left":
            self.passing_order = "Right"

        elif self.passing_order is "Right":
            self.passing_order = "Straight"

        elif self.passing_order is "Straight":
            self.passing_order = "None"


class PlayingState(State):
    def __init__(self, game, name):
        CardLogging.log_file.log('---PlayingState __init__() enter---')
        State.__init__(self, game, name)

        CardLogging.log_file.log('PlayingState: Set current suit to Current Player')
        CardLogging.log_file.log('PlayingState: Set current suit to Clubs')
        CardLogging.log_file.log('PlayingState: Set trick pile to empty list')
        CardLogging.log_file.log('PlayingState: Set hearts broken to False')
        CardLogging.log_file.log('PlayingState: Set current card to None')

        self.currentPlayer = None
        self.game.currentSuit = Constant.Suit.Clubs
        self.trickPile = []
        self.game.heartsBroken = False
        self.currentCard = None

        self.delay_trick_pile = False
        self.previous_time = 0

        self.player_one_x = 0
        self.player_one_y = 0

        self.player_two_x = 0
        self.player_two_y = 0

        self.player_three_x = 0
        self.player_three_y = 0

        self.player_four_x = 0
        self.player_four_y = 0

        self.set_trick_pile_locations()
        CardLogging.log_file.log('---PlayingState __init__() exit---')

    def enter(self):
        CardLogging.log_file.log('---PlayingState enter() enter---')

        CardLogging.log_file.log('PlayingState: Set current suit to Clubs')
        CardLogging.log_file.log('PlayingState: Set trick pile to empty list')
        CardLogging.log_file.log('PlayingState: Set hearts broken to False')
        CardLogging.log_file.log('PlayingState: Set current card to None')

        self.trickPile = []
        self.game.heartsBroken = False
        self.game.current_suit = Constant.Suit.Clubs
        self.currentCard = None

        self.currentPlayer = self.find_player_with_two_of_spades()
        CardLogging.log_file.log('---PlayingState enter() exit---')
        return

    def exit(self):
        CardLogging.log_file.log('---PlayingState exit() enter---')
        CardLogging.log_file.log('---PlayingState exit() exit---')
        self.next_state = None

    def handle_keypress(self, event):
        CardLogging.log_file.log('---PlayingState handle_keypress() enter---')
        if self.currentPlayer is self.game.player_one:
            self.currentCard = self.currentPlayer.handle_keypress(event)
            if self.currentCard is not None:
                if self.game.currentSuit is None:
                    self.game.currentSuit = self.currentCard.card.suit

                self.move_card_to_trick_pile(self.currentCard.card)
                self.set_next_player()

                self.game.player_one.hand.remove(self.currentCard.card)
                self.currentCard = None
        CardLogging.log_file.log('---PlayingState handle_keypress() exit---')
        return

    def handle_card_click(self, card_ui):
        CardLogging.log_file.log('---PlayingState handle_card_click() enter---')
        if self.currentPlayer is self.game.player_one:
            self.currentPlayer.handle_card_click(card_ui, self.game.currentSuit)
        CardLogging.log_file.log('---PlayingState handle_card_click() exit---')
        return

    def update(self):
        if self.delay_trick_pile:
            if (pygame.time.get_ticks() - self.previous_time) > 500:
                self.delay_trick_pile = False
                self.move_trick_pile_to_player()

        else:
            # CardLogging.log_file.log('---PlayingState update() enter---')
            if len(self.trickPile) is 4:
                self.previous_time = pygame.time.get_ticks()
                self.delay_trick_pile = True

            elif self.is_done():
                CardLogging.log_file.log('PlayingState: Setting next state to Scoring')
                self.next_state = "Scoring"

            elif self.currentPlayer is not self.game.player_one:
                self.handle_computer_player_turn()

        # CardLogging.log_file.log('---PlayingState update() exit---')
        return self.next_state

    def set_trick_pile_locations(self):

        CardLogging.log_file.log('---PlayingState set_trick_pile_locations() enter---')
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

        CardLogging.log_file.log('---PlayingState set_trick_pile_locations() exit---')
        return

    def move_card_to_trick_pile(self, card):

        CardLogging.log_file.log('---PlayingState move_card_to_trick_pile() enter---')
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

        CardLogging.log_file.log('---PlayingState move_card_to_trick_pile() exit---')
        return

    def move_trick_pile_to_player(self):
        CardLogging.log_file.log('---PlayingState move_trick_pile_to_player() enter---')
        CardLogging.log_file.log('PlayingState: Trick pile has 4 cards')
        highest_card = self.find_highest_card()

        trick_player = highest_card.card.owner
        self.currentPlayer = highest_card.card.owner

        CardLogging.log_file.log('PlayingState: Trick player is ' + self.currentPlayer.name)
        CardLogging.log_file.log('PlayingState: Playing handle card click')

        while len(self.trickPile) > 0:

            card_ui = self.trickPile[0]
            if card_ui.card.suit is Constant.Suit.Hearts:
                self.game.heartsBroken = True
            CardLogging.log_file.log('PlayingState: Transfer card: ' + Constant.value_str[card_ui.card.value] + ' of ' +
                                     Constant.suit_str[card_ui.card.suit])
            Cards.CardEngine.transfer_card(card_ui, self.trickPile, trick_player.tricks)
        CardLogging.log_file.log('---PlayingState move_trick_pile_to_player() exit---')
        self.game.currentSuit = None

    def find_player_with_two_of_spades(self):
        CardLogging.log_file.log('---PlayingState find_player_with_two_of_spades() enter---')
        for i in range(0, 13):
            CardLogging.log_file.log('PlayingState: Check card ' + str(i + 1) + ' is 2 of clubs P1 to P4')

            if self.game.player_one.hand[i].suit is Constant.Suit.Clubs \
                    and self.game.player_one.hand[i].value is Constant.Value.Two:
                CardLogging.log_file.log('PlayingState: 2 of clubs found P1')
                return self.game.player_one

            elif self.game.player_two.hand[i].suit is Constant.Suit.Clubs \
                    and self.game.player_two.hand[i].value is Constant.Value.Two:
                CardLogging.log_file.log('PlayingState: 2 of clubs found P2')
                return self.game.player_two

            elif self.game.player_three.hand[i].suit is Constant.Suit.Clubs \
                    and self.game.player_three.hand[i].value is Constant.Value.Two:
                CardLogging.log_file.log('PlayingState: 2 of clubs found P3')
                return self.game.player_three

            elif self.game.player_four.hand[i].suit is Constant.Suit.Clubs \
                    and self.game.player_four.hand[i].value is Constant.Value.Two:
                CardLogging.log_file.log('PlayingState: 2 of clubs found P4')
                return self.game.player_four
        CardLogging.log_file.log('---PlayingState find_player_with_two_of_spades() exit---')
        return None

    def handle_computer_player_turn(self):
        CardLogging.log_file.log('---PlayingState handle_computer_player_turn() enter---')
        CardLogging.log_file.log('PlayingState: Allow computer to play card')
        card = self.currentPlayer.play_card(self.game.currentSuit, self.trickPile)

        if self.game.currentSuit is None:
            self.game.currentSuit = card.suit
            CardLogging.log_file.log('PlayingState: Set suit to ' + str(self.game.currentSuit))

        self.move_card_to_trick_pile(card)
        self.set_next_player()
        CardLogging.log_file.log('---PlayingState handle_computer_player_turn() exit---')

    def set_next_player(self):
        CardLogging.log_file.log('---PlayingState set_next_player() enter---')
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
        CardLogging.log_file.log('---PlayingState set_next_player() exit---')

    def find_highest_card(self):
        CardLogging.log_file.log('---PlayingState find_highest_card() enter---')
        highest_card = None
        highest_value = -1

        for card_ui in self.trickPile:

            CardLogging.log_file.log('PlayingState: Set card location to 1200, 1200')
            CardLogging.log_file.log('PlayingState: Set card visible to false')
            card_ui.set_location(1200, 1200)
            card_ui.visible = False
            if card_ui.card.suit is self.game.currentSuit:
                if card_ui.card.value > highest_value:
                    CardLogging.log_file.log('PlayingState: Highest card of suit ' + str(self.game.currentSuit))
                    highest_card = card_ui
                    highest_value = card_ui.card.value
                    CardLogging.log_file.log('PlayingState: Value of card is ' + str(highest_value))
        CardLogging.log_file.log('---PlayingState find_highest_card() exit---')
        return highest_card

    def is_done(self):
        CardLogging.log_file.log('---PlayingState is_done() enter---')
        num_cards = 0
        num_cards += len(self.game.player_one.hand)
        num_cards += len(self.game.player_two.hand)
        num_cards += len(self.game.player_three.hand)
        num_cards += len(self.game.player_four.hand)

        CardLogging.log_file.log('PlayingState: Cards remaining: ' + str(num_cards))

        if num_cards is 0:
            CardLogging.log_file.log('PlayingState: No card found')
            CardLogging.log_file.log('---PlayingState is_done() exit---')
            return True

        else:
            CardLogging.log_file.log('PlayingState: Cards found')
            CardLogging.log_file.log('---PlayingState is_done() exit---')
            return False

    def player_select_card(self, card_ui):
        CardLogging.log_file.log('---PlayingState player_select_card() enter---')
        card = card_ui.card
        CardLogging.log_file.log('PlayingState: Move: ' + str(card.value) + ' of ' + str(card.suit) + ' up')
        card_ui.move(0, -25, 0)
        self.currentCard = card_ui
        CardLogging.log_file.log('---PlayingState player_select_card() exit---')
        return

    def player_deselect_card(self, card_ui):
        CardLogging.log_file.log('---PlayingState player_deselect_card() enter---')
        if self.currentCard is card_ui:
            if card_ui is not None:
                card = card_ui.card
                CardLogging.log_file.log('PlayingState: Move: ' + str(card.value) + ' of ' + str(card.suit) + ' down')
                card_ui.move(0, 25, 0)
            self.currentCard = None
        CardLogging.log_file.log('---PlayingState player_deselect_card() exit---')
        return


class ScoringState(State):

    def __init__(self, game, name):
        CardLogging.log_file.log('---ScoringState __init__() enter---')
        State.__init__(self, game, name)
        self.player_one_points = [0]
        self.player_two_points = [0]
        self.player_three_points = [0]
        self.player_four_points = [0]

        self.player_one_point_text_list = []
        self.player_two_point_text_list = []
        self.player_three_point_text_list = []
        self.player_four_point_text_list = []

        self.player_one_total_points = 0
        self.player_two_total_points = 0
        self.player_three_total_points = 0
        self.player_four_total_points = 0

        self.button = UI.Button(rect=pygame.Rect((340, 400), (120, 30)))
        self.button.callbackFunction = self.handle_button_press
        self.button.visible = False
        self.button.text = "Start next round"

        size = (60, 30)
        y = 30
        p1_loc = (280, y)
        p2_loc = (340, y)
        p3_loc = (400, y)
        p4_loc = (460, y)

        player_one_point_text = UI.Text(rect=pygame.Rect(p1_loc, size))
        player_one_point_text.text = str(self.player_one_points[0])
        player_one_point_text.visible = False

        player_two_point_text = UI.Text(rect=pygame.Rect(p2_loc, size))
        player_two_point_text.text = str(self.player_two_points[0])
        player_two_point_text.visible = False

        player_three_point_text = UI.Text(rect=pygame.Rect(p3_loc, size))
        player_three_point_text.text = str(self.player_three_points[0])
        player_three_point_text.visible = False

        player_four_point_text = UI.Text(rect=pygame.Rect(p4_loc, size))
        player_four_point_text.text = str(self.player_four_points[0])
        player_four_point_text.visible = False

        self.player_one_point_text_list.append(player_one_point_text)
        self.player_two_point_text_list.append(player_two_point_text)
        self.player_three_point_text_list.append(player_three_point_text)
        self.player_four_point_text_list.append(player_four_point_text)

        CardLogging.log_file.log('---ScoringState __init__() exit---')

    def enter(self):
        # Evaluate points each player receives as follows:
        #   Heart: 1 point
        #   Queen of Spades: 13 points
        #   Shooting the moon: One player gets all hearts and Queen of Spades
        #       All other players receive 26 points
        # Determine if anyone has 100 points or more
        #   Determine winner: Lowest

        CardLogging.log_file.log('---ScoringState enter() enter---')

        player_one_round_points = self.get_points(self.game.player_one)
        player_two_round_points = self.get_points(self.game.player_two)
        player_three_round_points = self.get_points(self.game.player_three)
        player_four_round_points = self.get_points(self.game.player_four)

        CardLogging.log_file.log('ScoringState: P1 Temp Points: ' + str(player_one_round_points))
        CardLogging.log_file.log('ScoringState: P2 Temp Points: ' + str(player_two_round_points))
        CardLogging.log_file.log('ScoringState: P3 Temp Points: ' + str(player_three_round_points))
        CardLogging.log_file.log('ScoringState: P4 Temp Points: ' + str(player_four_round_points))

        player_one_round_points, player_two_round_points, player_three_round_points, player_four_round_points = \
            self.handle_shooting_the_moon(player_one_round_points, player_two_round_points,
                                          player_three_round_points, player_four_round_points)

        self.player_one_total_points += player_one_round_points
        self.player_two_total_points += player_two_round_points
        self.player_three_total_points += player_three_round_points
        self.player_four_total_points += player_four_round_points

        self.player_one_points.append(player_one_round_points)
        self.player_two_points.append(player_two_round_points)
        self.player_three_points.append(player_three_round_points)
        self.player_four_points.append(player_four_round_points)

        size = (60, 30)
        y = len(self.player_one_points)*30
        p1_loc = (280, y)
        p2_loc = (340, y)
        p3_loc = (400, y)
        p4_loc = (460, y)

        player_one_point_text = UI.Text(rect=pygame.Rect(p1_loc, size))
        player_one_point_text.visible = False
        player_one_point_text.text = str(self.player_one_total_points)
        self.player_one_point_text_list.append(player_one_point_text)

        player_two_point_text = UI.Text(rect=pygame.Rect(p2_loc, size))
        player_two_point_text.visible = False
        player_two_point_text.text = str(self.player_two_total_points)
        self.player_two_point_text_list.append(player_two_point_text)

        player_three_point_text = UI.Text(rect=pygame.Rect(p3_loc, size))
        player_three_point_text.visible = False
        player_three_point_text.text = str(self.player_three_total_points)
        self.player_three_point_text_list.append(player_three_point_text)

        player_four_point_text = UI.Text(rect=pygame.Rect(p4_loc, size))
        player_four_point_text.visible = False
        player_four_point_text.text = str(self.player_four_total_points)
        self.player_four_point_text_list.append(player_four_point_text)

        for text in self.player_one_point_text_list:
            text.visible = True

        for text in self.player_two_point_text_list:
            text.visible = True

        for text in self.player_three_point_text_list:
            text.visible = True

        for text in self.player_four_point_text_list:
            text.visible = True

        self.button.visible = True

        CardLogging.log_file.log('ScoringState: P1 Points: ' + str(self.player_one_points))
        CardLogging.log_file.log('ScoringState: P2 Points: ' + str(self.player_two_points))
        CardLogging.log_file.log('ScoringState: P3 Points: ' + str(self.player_three_points))
        CardLogging.log_file.log('ScoringState: P4 Points: ' + str(self.player_four_points))

        CardLogging.log_file.log('---ScoringState enter() exit---')
        return

    def exit(self):
        CardLogging.log_file.log('---ScoringState exit() enter---')
        CardLogging.log_file.log('ScoringState: set P1-P4 trick piles to empty list')
        self.game.player_one.tricks = []
        self.game.player_two.tricks = []
        self.game.player_three.tricks = []
        self.game.player_four.tricks = []
        self.next_state = None

        for text in self.player_one_point_text_list:
            text.visible = False

        for text in self.player_two_point_text_list:
            text.visible = False

        for text in self.player_three_point_text_list:
            text.visible = False

        for text in self.player_four_point_text_list:
            text.visible = False

        self.button.visible = False

        CardLogging.log_file.log('---ScoringState exit() exit---')

    def handle_keypress(self, event):
        CardLogging.log_file.log('---ScoringState handle_keypress() enter---')
        CardLogging.log_file.log('---ScoringState handle_keypress() exit---')
        return

    def handle_card_click(self, card_ui):
        CardLogging.log_file.log('---ScoringState handle_card_click() enter---')
        CardLogging.log_file.log('---ScoringState handle_card_click() exit---')
        return

    def update(self):
        # CardLogging.log_file.log('---ScoringState update() enter---')
        # CardLogging.log_file.log('---ScoringState update() exit---')
        return self.next_state

    def any_player_lost(self):
        CardLogging.log_file.log('---ScoringState any_player_lost() enter---')
        CardLogging.log_file.log('ScoringState: any player lost?')
        if self.player_one_total_points >= 100:
            CardLogging.log_file.log('ScoringState: P1 had 100 or more points')
            CardLogging.log_file.log('---ScoringState any_player_lost() exit---')
            return True

        if self.player_two_total_points >= 100:
            CardLogging.log_file.log('ScoringState: P2 had 100 or more points')
            CardLogging.log_file.log('---ScoringState any_player_lost() exit---')
            return True

        if self.player_three_total_points >= 100:
            CardLogging.log_file.log('ScoringState: P3 had 100 or more points')
            CardLogging.log_file.log('---ScoringState any_player_lost() exit---')
            return True

        if self.player_four_total_points >= 100:
            CardLogging.log_file.log('ScoringState: P4 had 100 or more points')
            CardLogging.log_file.log('---ScoringState any_player_lost() exit---')
            return True

        CardLogging.log_file.log('ScoringState: No player had 100 or more points')
        CardLogging.log_file.log('---ScoringState any_player_lost() exit---')
        return False

    def determine_lowest_points(self):
        CardLogging.log_file.log('---ScoringState determine_lowest_points() enter---')
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

        CardLogging.log_file.log('---ScoringState determine_lowest_points() exit---')
        return lowest_player

    def get_points(self, player):
        CardLogging.log_file.log('---ScoringState get_points() enter---')
        points = 0
        for card_ui in player.tricks:
            card = card_ui.card
            if card.suit is Constant.Suit.Hearts:
                CardLogging.log_file.log('ScoringState: Hearts found')
                points += 1
            elif card.suit is Constant.Suit.Spades:
                if card.value is Constant.Value.Queen:
                    CardLogging.log_file.log('ScoringState: Queen of Spades found')
                    points += 13

        CardLogging.log_file.log('ScoringState: ' + player.name + ': ' + str(points))
        CardLogging.log_file.log('---ScoringState get_points() exit---')
        return points

    def handle_shooting_the_moon(self, p1_round_points, p2_round_points, p3_round_points, p4_round_points):
        CardLogging.log_file.log('---ScoringState handle_shooting_the_moon() enter---')
        if p1_round_points is 26:
            CardLogging.log_file.log('ScoringState: P1 shot the moon')
            p1_round_points = 0
            p2_round_points = 26
            p3_round_points = 26
            p4_round_points = 26

        elif p2_round_points is 26:
            CardLogging.log_file.log('ScoringState: P2 shot the moon')
            p1_round_points = 26
            p2_round_points = 0
            p3_round_points = 26
            p4_round_points = 26

        elif p3_round_points is 26:
            CardLogging.log_file.log('ScoringState: P3 shot the moon')
            p1_round_points = 26
            p2_round_points = 26
            p3_round_points = 0
            p4_round_points = 26

        elif p4_round_points is 26:
            CardLogging.log_file.log('ScoringState: P4 shot the moon')
            p1_round_points = 26
            p2_round_points = 26
            p3_round_points = 26
            p4_round_points = 0

        CardLogging.log_file.log('---ScoringState handle_shooting_the_moon() exit---')
        return p1_round_points, p2_round_points, p3_round_points, p4_round_points

    def handle_button_press(self, button):
        if self.any_player_lost():
            CardLogging.log_file.log('ScoringState: Setting next state to None.  A player lost')
            self.next_state = None

        else:
            CardLogging.log_file.log('ScoringState: Setting next state to Setup.')
            self.next_state = "Setup"
