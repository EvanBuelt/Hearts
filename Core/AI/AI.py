from CardEngine import Engine
from Core import CardLogging
from Core import Constant

class HumanAI:
    player = None
    _selected_card_ui = None

    def __init__(self):
        return

    def set_player(self, player):
        self.player = player

    def pass_card(self, human_player, card):
        return

    def play_card(self, current_suit, trick_pile):
        return

    def handle_card_click(self, card_ui, current_suit):
        if card_ui is self._selected_card_ui:
            self.player_deselect_card(card_ui)

        elif card_ui.card in self.player.hand:
            card_ui.play_sound()
            if self.has_two_of_clubs():
                if card_ui.card.suit is Constant.Suit.Clubs:
                    if card_ui.card.value is Constant.Value.Two:
                        self.player_deselect_card(self._selected_card_ui)
                        self.player_select_card(card_ui)

            elif self.is_suit_in_hand(current_suit):
                if card_ui.card.suit is current_suit:
                    self.player_deselect_card(self._selected_card_ui)
                    self.player_select_card(card_ui)

            else:
                self.player_deselect_card(self._selected_card_ui)
                self.player_select_card(card_ui)

        return

    def handle_keypress(self, event):
        card_ui = self._selected_card_ui
        self._selected_card_ui = None
        return card_ui

    def has_two_of_clubs(self):
        for card in self.player.hand:
            if card.suit is Constant.Suit.Clubs:
                if card.value is Constant.Value.Two:
                    return True
        return False

    def is_suit_in_hand(self, current_suit):
        suit_in_hand = False
        if self.player is not None:

            for card in self.player.hand:
                if card.suit is current_suit:
                    suit_in_hand = True

        return suit_in_hand

    def player_select_card(self, card_ui):
        card_ui.move(0, -25, 0)
        self._selected_card_ui = card_ui
        return

    def player_deselect_card(self, card_ui):
        if self._selected_card_ui is card_ui:
            if card_ui is not None:
                card_ui.move(0, 25, 0)
            self._selected_card_ui = None
        return


class ComputerAI:
    def __init__(self):
        self.player = None
        return

    def set_player(self, player):
        self.player = player

    def pass_cards(self, computer_player):
        CardLogging.log_file.log('ComputerAI: ' + self.player.name + ': pass cards')
        computer_player.passing = self.determine_cards_to_pass()
        return

    def play_card(self, current_suit, trick_pile):

        '''
        Determine suit to follow and has suit:
        -Hearts:
            -Play highest hearts lower than highest heart
            -Play lowest heart
        -Spades:
            -Play Queen of Spades if King or Ace is in trick pile
            -Play King or Ace of spades if last player to have a spades
            -Play highest non-queen spade lower than highest spade
            -Play lowest spade
        -Clubs
            -Play highest club if first turn
            -Play highest club lower than highest club
            -Play lowest club
        -Diamonds:
            -Play highest diamond lower than highest diamond
            -Play lowest diamond
        -None:
            -Play lowest Spade
            -Play lowest Heart (if broken)
            -Play lowest Club
            -Play lowest Diamond

        If suit is not in hand:
        -Spades:
            -Play Queen of Spades
            -Play King or Ace of Spades

        -Hearts:
            -Play highest heart 7 or above

        -Play highest card 10 or above
        -Hearts:
            -Play highest hearts

        -Play highest card of suit with lowest number of cards
        '''

        hand = self.player.hand
        passing_card = None

        if current_suit is Constant.Suit.Hearts:
            passing_card = self.find_highest_card_under_value(current_suit, trick_pile)
            if passing_card is None:
                passing_card = self.find_lowest_card(current_suit)

        elif current_suit is Constant.Suit.Spades:
            highest_spade = self.get_highest_card_in_trick_pile(current_suit, trick_pile)
            if (highest_spade.value is Constant.Value.King) or (highest_spade.value is Constant.Value.Ace):
                if self.has_card(Constant.Suit.Spades, Constant.Value.Queen):
                    for card in self.player.hand:
                        if card.value is Constant.Value.Queen:
                            if card.suit is Constant.Suit.Spades:
                                passing_card = card
            if passing_card is None:
                if len(trick_pile) is 3:
                    passing_card = self.find_highest_card(Constant.Suit.Spades)
            if passing_card is None:
                passing_card = self.find_highest_card_under_value(current_suit, trick_pile)
            if passing_card is None:
                passing_card = self.find_lowest_card(current_suit)

        elif current_suit is Constant.Suit.Clubs:
            # passing_card = highest clubs if first turn
            passing_card = self.find_highest_card_under_value(current_suit, trick_pile)
            if passing_card is None:
                passing_card = self.find_lowest_card(current_suit)

        elif current_suit is Constant.Suit.Diamonds:
            passing_card = self.find_highest_card_under_value(current_suit, trick_pile)
            if passing_card is None:
                passing_card = self.find_lowest_card(current_suit)

        elif current_suit is None:
            passing_card = self.find_lowest_card(Constant.Suit.Spades)
            if passing_card is None:
                passing_card = self.find_lowest_card(Constant.Suit.Hearts)
            if passing_card is None:
                passing_card = self.find_lowest_card(Constant.Suit.Clubs)
            if passing_card is None:
                passing_card = self.find_lowest_card(Constant.Suit.Diamonds)
            # passing_card = self.lowest_card(["Spades"])
            # "Hearts"
            # "Clubs"
            # "Diamonds"

        if passing_card is not None:
            hand.remove(passing_card)
            return passing_card

        else:
            '''
            -Spades:
            -Play Queen of Spades
            -Play King or Ace of Spades

            -Hearts:
                -Play highest heart 7 or above

            -Play highest card 10 or above
            -Hearts:
                -Play highest hearts
            '''
            
            # Play Queen of Spades if it's in the hand
            queen_of_spades_exists, passing_card = self.has_card(Constant.Value.Queen,
                                                                 Constant.Suit.Spades)

            # Play Ace of Spades if it's in hand (and Queen of Spades is not in hand)
            if passing_card is None:
                ace_of_spades_exists, passing_card = self.has_card(Constant.Value.Ace,
                                                                   Constant.Suit.Spades)

            # Play King of Spades if it's in hand (and Queen or Ace of Spades is not in hand)
            if passing_card is None:
                king_of_spades_exists, passing_card = self.has_card(Constant.Value.King,
                                                                    Constant.Suit.Spades)

            # Play highest heart
            if passing_card is None:
                passing_card = self.find_highest_card(Constant.Suit.Hearts)

            # Play highest spade
            if passing_card is None:
                passing_card = self.find_highest_card(Constant.Suit.Spades)

            # Play highest diamond
            if passing_card is None:
                passing_card = self.find_highest_card(Constant.Suit.Diamonds)

            # Play highest club
            if passing_card is None:
                passing_card = self.find_highest_card(Constant.Suit.Clubs)

            # Fail safe if no passing card is found
            if passing_card is None:
                for i in range(0, len(hand)):
                    if hand[i].suit is current_suit:
                        return hand.pop(i)
                return hand.pop()
            else:
                hand.remove(passing_card)
                return passing_card

    def handle_card_click(self, card_ui, current_suit):
        return

    def handle_keypress(self, event):
        return

    # Functions used to pass Cards
    def determine_cards_to_pass(self):

        cards_to_pass = []

        # Pass queen of spades if it's in hand
        queen_of_spades_exists, card = self.has_card(Constant.Value.Queen, Constant.Suit.Spades)
        if queen_of_spades_exists:
            cards_to_pass.append(card)

        # Pass ace of spades if it's in hand
        ace_of_spades_exists, card = self.has_card(Constant.Value.Ace, Constant.Suit.Spades)
        if ace_of_spades_exists:
            cards_to_pass.append(card)

        # Pass king of spades if it's in hand
        king_of_spades_exists, card = self.has_card(Constant.Value.King, Constant.Suit.Spades)
        if king_of_spades_exists:
            cards_to_pass.append(card)

        self.pass_entire_suit(Constant.Suit.Hearts, cards_to_pass)
        self.pass_entire_suit(Constant.Suit.Clubs, cards_to_pass)
        self.pass_entire_suit(Constant.Suit.Diamonds, cards_to_pass)
        self.pass_entire_suit(Constant.Suit.Spades, cards_to_pass)

        # Get rid of highest hearts
        hearts_list = self.get_highest_cards(Constant.Suit.Hearts, cards_to_pass)
        Engine.CardEngine.transfer_list(hearts_list, cards_to_pass)

        # Get rid of highest diamonds
        diamonds_list = self.get_highest_cards(Constant.Suit.Diamonds, cards_to_pass)
        Engine.CardEngine.transfer_list(diamonds_list, cards_to_pass)

        # Get rid of highest clubs
        clubs_list = self.get_highest_cards(Constant.Suit.Clubs, cards_to_pass)
        Engine.CardEngine.transfer_list(clubs_list, cards_to_pass)

        # Get rid of highest spades
        spades_list = self.get_highest_cards(Constant.Suit.Spades, cards_to_pass)
        Engine.CardEngine.transfer_list(spades_list, cards_to_pass)

        for card in self.player.hand:
            if card not in cards_to_pass:
                if len(cards_to_pass) < 3:
                    cards_to_pass.append(card)

        return cards_to_pass
        # The logic to determine what to pass is as follows:
        # Pass the Queen of Spades
        # Pass the King and Ace of Spades
        # Pass Highest Hearts
        # Remove a suit if possible
        # Pass Highest Diamonds, Clubs, Hearts, Spades in that order

    def has_card(self, suit, value):
        for card in self.player.hand:
            if card.suit is suit:
                if card.value is value:
                    return True, card

        return False, None

    def get_highest_cards(self, suit, cards_to_pass):
        number_cards_to_move = 3 - len(cards_to_pass)
        possible_card_list = []
        card_list = []

        for card in self.player.hand:
            if card not in cards_to_pass:
                if card.suit is suit:
                    possible_card_list.append(card)

        while (len(card_list) < number_cards_to_move) and (len(possible_card_list) > 0):
            card_list.append(possible_card_list.pop())

        return card_list

    def get_number_of_cards_with_suit(self, suit):
        number = 0
        for card in self.player.hand:
            if card.suit is suit:
                number += 1
        CardLogging.log_file.log('ComputerAI: Number of ' + Constant.suit_str[suit] + ': ' + str(number))
        return number

    def find_lowest_card(self, current_suit):
        suit_pile = []
        lowest_card = None

        for card in self.player.hand:
            if card.suit is current_suit:
                suit_pile.append(card)

        if len(suit_pile) is 0:
            return None

        for card in suit_pile:
            if lowest_card is None:
                lowest_card = card
            else:
                if card.value < lowest_card.value:
                    lowest_card = card

        return lowest_card

    def find_highest_card(self, current_suit):
        suit_pile = []
        highest_card = None

        for card in self.player.hand:
            if card.suit is current_suit:
                suit_pile.append(card)

        if len(suit_pile) is 0:
            return None

        for card in suit_pile:
            if highest_card is None:
                highest_card = card
            else:
                if card.value > highest_card.value:
                    highest_card = card

        return highest_card

    def find_highest_card_under_value(self, current_suit, trick_pile):

        if trick_pile is None:
            return None

        highest_card = None

        highest_trick_card = self.get_highest_card_in_trick_pile(current_suit, trick_pile)
        card_list = self.get_all_cards_of_given_suit(current_suit)

        if len(card_list) is 0:
            return None

        elif highest_trick_card is None:
            return None

        else:
            for card in card_list:
                if card.value < highest_trick_card.value:
                    if highest_card is None:
                        highest_card = card
                    elif card.value > highest_card.value:
                        highest_card = card

        return highest_card

    def get_highest_card_in_trick_pile(self, current_suit, trick_pile):
        highest_trick_card = None
        for card_ui in trick_pile:
            if card_ui.card.suit is current_suit:
                if highest_trick_card is None:
                    highest_trick_card = card_ui.card
                elif card_ui.card.value > highest_trick_card.value:
                    highest_trick_card = card_ui.card

        return highest_trick_card

    def get_all_cards_of_given_suit(self, current_suit):
        card_list = []
        for card in self.player.hand:
            if card.suit is current_suit:
                card_list.append(card)

        return card_list

    def pass_entire_suit(self, suit, cards_to_pass):
        num_cards_in_suit = self.get_number_of_cards_with_suit(suit)
        if num_cards_in_suit <= (3 - len(cards_to_pass)):
            cards_to_move = self.get_highest_cards(suit, cards_to_pass)
            Engine.CardEngine.transfer_list(cards_to_move, cards_to_pass)
