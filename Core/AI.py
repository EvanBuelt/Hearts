from CardEngine import Engine
import CardLogging
import Constant


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
                if card_ui.card.suit is Constant.suit_str_to_int["Clubs"]:
                    if card_ui.card.value is Constant.value_str_to_int["2"]:
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
            if card.suit is Constant.suit_str_to_int["Clubs"]:
                if card.value is Constant.value_str_to_int["2"]:
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

        if current_suit is Constant.suit_str_to_int["Hearts"]:
            passing_card = self.find_highest_card_under_value(current_suit, trick_pile)

        elif current_suit is Constant.suit_str_to_int["Spades"]:
            passing_card = self.find_highest_card_under_value(current_suit, trick_pile)

        elif current_suit is Constant.suit_str_to_int["Clubs"]:
            passing_card = self.find_highest_card_under_value(current_suit, trick_pile)

        elif current_suit is Constant.suit_str_to_int["Diamonds"]:
            passing_card = self.find_highest_card_under_value(current_suit, trick_pile)

        elif current_suit is None:
            passing_card = None

        if passing_card is not None:
            hand.remove(passing_card)
            return passing_card

        else:
            for i in range(0, len(hand)):
                if hand[i].suit is current_suit:
                    return hand.pop(i)

            return hand.pop()

    def handle_card_click(self, card_ui, current_suit):
        return

    def handle_keypress(self, event):
        return

    # Functions used to pass Cards
    def determine_cards_to_pass(self):

        cards_to_pass = []

        # Pass queen of spades if it's in hand
        queen_of_spades_exists, card = self.has_card(Constant.value_str_to_int["Queen"], Constant.suit_str_to_int["Spades"])
        if queen_of_spades_exists:
            cards_to_pass.append(card)

        # Pass ace of spades if it's in hand
        ace_of_spades_exists, card = self.has_card(Constant.value_str_to_int["Ace"], Constant.suit_str_to_int["Spades"])
        if ace_of_spades_exists:
            cards_to_pass.append(card)

        # Pass king of spades if it's in hand
        king_of_spades_exists, card = self.has_card(Constant.value_str_to_int["King"], Constant.suit_str_to_int["Spades"])
        if king_of_spades_exists:
            cards_to_pass.append(card)

        self.pass_entire_suit(Constant.suit_str_to_int["Hearts"], cards_to_pass)
        self.pass_entire_suit(Constant.suit_str_to_int["Clubs"], cards_to_pass)
        self.pass_entire_suit(Constant.suit_str_to_int["Diamonds"], cards_to_pass)
        self.pass_entire_suit(Constant.suit_str_to_int["Spades"], cards_to_pass)

        # Get rid of highest hearts
        hearts_list = self.get_highest_cards(Constant.suit_str_to_int["Hearts"], cards_to_pass)
        Engine.CardEngine.transfer_list(hearts_list, cards_to_pass)

        # Get rid of highest diamonds
        diamonds_list = self.get_highest_cards(Constant.suit_str_to_int["Diamonds"], cards_to_pass)
        Engine.CardEngine.transfer_list(diamonds_list, cards_to_pass)

        # Get rid of highest clubs
        clubs_list = self.get_highest_cards(Constant.suit_str_to_int["Clubs"], cards_to_pass)
        Engine.CardEngine.transfer_list(clubs_list, cards_to_pass)

        # Get rid of highest spades
        spades_list = self.get_highest_cards(Constant.suit_str_to_int["Spades"], cards_to_pass)
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
        CardLogging.log_file.log('ComputerAI: Number of ' + Constant.suit_int_to_str[suit] + ': ' + str(number))
        return number

    def find_highest_card_under_value(self, current_suit, trick_pile):

        if trick_pile is None:
            return None

        card_list = []
        highest_trick_card = None
        highest_card = None

        for card_ui in trick_pile:
            if card_ui.card.suit is current_suit:
                if highest_trick_card is None:
                    highest_trick_card = card_ui.card
                elif card_ui.card.value > highest_trick_card.value:
                    highest_trick_card = card_ui.card

        for card in self.player.hand:
            if card.suit is current_suit:
                card_list.append(card)

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

    def pass_entire_suit(self, suit, cards_to_pass):
        num_cards_in_suit = self.get_number_of_cards_with_suit(suit)
        if num_cards_in_suit <= (3 - len(cards_to_pass)):
            cards_to_move = self.get_highest_cards(suit, cards_to_pass)
            Engine.CardEngine.transfer_list(cards_to_move, cards_to_pass)
