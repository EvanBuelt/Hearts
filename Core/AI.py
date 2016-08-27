import CardLogging
import Constant


class Player:
    def __init__(self, name, ai):
        self.name = name
        self.ai = ai
        self.hand = []
        self.tricks = []
        self.passing = []
        self.selected_card = None

        self.ai.set_player(self)

    def sort_hand(self):
        for i in range(0, len(self.hand)):
            for j in range(0, i):
                if self.hand[j].suit > self.hand[j + 1].suit:
                    temp = self.hand[j]
                    self.hand[j] = self.hand[j + 1]
                    self.hand[j + 1] = temp

        for i in range(0, len(self.hand)):
            for j in range(0, i):
                if self.hand[j].value > self.hand[j + 1].value:
                    temp = self.hand[j]
                    self.hand[j] = self.hand[j + 1]
                    self.hand[j + 1] = temp

    def set_hand_owner(self):
        for card in self.hand:
            card.owner = self

    def pass_cards(self):
        return self.ai.pass_cards(self)

    def play_card(self, current_suit, trick_pile):
        return self.ai.play_card(current_suit, trick_pile)

    def handle_card_click(self, card_ui, current_suit):
        return self.ai.handle_card_click(card_ui, current_suit)

    def handle_keypress(self, event):
        return self.ai.handle_keypress(event)


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
                if card_ui.card.suit is Constant.suits_str["Clubs"]:
                    if card_ui.card.value is Constant.values_str["2"]:
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
            if card.suit is Constant.suits_str["Clubs"]:
                if card.value is Constant.values_str["2"]:
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

        computer_player.passing = []
        passing = computer_player.passing

        cards_to_pass = self.determine_cards_to_pass()
        for i in range(0, 3):
            passing.append(cards_to_pass[i])

        return

    def play_card(self, current_suit, trick_pile):
        hand = self.player.hand

        if current_suit is Constant.suits_str["Hearts"]:
            return

        elif current_suit is Constant.suits_str["Spades"]:
            return

        elif current_suit is Constant.suits_str["Clubs"]:
            return

        elif current_suit is Constant.suits_str["Diamonds"]:
            return

        elif current_suit is None:
            return

        else:
            for i in range(0, len(hand)):
                if hand[i].suit is current_suit:
                    return hand.pop(i)

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
        return hand.pop()

    def handle_card_click(self, card_ui, current_suit):
        return

    def handle_keypress(self, event):
        return

    # Functions used to pass Cards
    def determine_cards_to_pass(self):

        cards_to_pass = []

        # Pass queen of spades if it's in hand
        queen_of_spades_exists, card = self.has_card(Constant.values_str["Queen"], Constant.suits_str["Spades"])
        if queen_of_spades_exists:
            cards_to_pass.append(card)

        # Pass ace of spades if it's in hand
        ace_of_spades_exists, card = self.has_card(Constant.values_str["Ace"], Constant.suits_str["Spades"])
        if ace_of_spades_exists:
            cards_to_pass.append(card)

        # Pass king of spades if it's in hand
        king_of_spades_exists, card = self.has_card(Constant.values_str["King"], Constant.suits_str["Spades"])
        if king_of_spades_exists:
            cards_to_pass.append(card)

        # Pass highest hearts in hand
        hearts_list = self.get_highest_cards(Constant.suits_str["Hearts"], 3 - len(cards_to_pass))
        while len(hearts_list) > 0:
            cards_to_pass.append(hearts_list.pop())

        num_hearts = self.get_number_of_cards_with_suit(Constant.suits_str["Hearts"])
        num_clubs = self.get_number_of_cards_with_suit(Constant.suits_str["Clubs"])
        num_diamonds = self.get_number_of_cards_with_suit(Constant.suits_str["Diamonds"])
        num_spades = self.get_number_of_cards_with_suit(Constant.suits_str["Spades"])

        # If the computer can get rid of all hearts, get rid of them
        if num_hearts <= (3 - len(cards_to_pass)):
            hearts_list = self.get_highest_cards(Constant.suits_str["Hearts"], 3 - len(cards_to_pass))
            while len(hearts_list) > 0:
                cards_to_pass.append(hearts_list.pop())

        # If the computer can get rid of all clubs, get rid of them
        if num_clubs <= (3 - len(cards_to_pass)):
            clubs_list = self.get_highest_cards(Constant.suits_str["Clubs"], 3 - len(cards_to_pass))
            while len(clubs_list) > 0:
                cards_to_pass.append(clubs_list.pop())

        # If the computer can get rid of all diamonds, get rid of them
        if num_diamonds <= (3 - len(cards_to_pass)):
            diamonds_list = self.get_highest_cards(Constant.suits_str["Diamonds"], 3 - len(cards_to_pass))
            while len(diamonds_list) > 0:
                cards_to_pass.append(diamonds_list.pop())

        # If the computer can get rid of all spades, get rid of them
        if num_spades <= (3 - len(cards_to_pass)):
            spades_list = self.get_highest_cards(Constant.suits_str["Spades"], 3 - len(cards_to_pass))
            while len(spades_list) > 0:
                cards_to_pass.append(spades_list.pop())

        # Get rid of highest diamonds
        diamonds_list = self.get_highest_cards(Constant.suits_str["Diamonds"], 3 - len(cards_to_pass))
        while len(diamonds_list) > 0:
            cards_to_pass.append(diamonds_list.pop())

        # Get rid of highest clubs
        clubs_list = self.get_highest_cards(Constant.suits_str["Clubs"], 3 - len(cards_to_pass))
        while len(clubs_list) > 0:
            cards_to_pass.append(clubs_list.pop())

        # Get rid of highest hearts
        hearts_list = self.get_highest_cards(Constant.suits_str["Hearts"], 3 - len(cards_to_pass))
        while len(hearts_list) > 0:
            cards_to_pass.append(hearts_list.pop())

        # Get rid of highest spades
        spades_list = self.get_highest_cards(Constant.suits_str["Spades"], 3 - len(cards_to_pass))
        while len(spades_list) > 0:
            cards_to_pass.append(spades_list.pop())

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

    def get_highest_cards(self, suit, number_cards_to_move):
        possible_card_list = []
        card_list = []

        for card in self.player.hand:
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
        CardLogging.log_file.log('ComputerAI: Number of ' + Constant.suits[suit] + ': ' + str(number))
        return number

    def find_highest_card_under_value(self, suit, trick_pile):

        card_list = []

        for card_ui in self.player.hand:
            if card_ui.suit is suit:
                card_list.append(card_ui)

        return
