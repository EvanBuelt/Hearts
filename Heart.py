import CardEngine.Engine as Cards
import pygame
import StateMachine.StateMachine as StateMachine
import StateMachine.State as State
import CardEngine.CardLogging as CardLogging

suits = {1: "Clubs",
         2: "Diamonds",
         3: "Spades",
         4: "Hearts"}

suits_str = {"Clubs": 1,
             "Diamonds": 2,
             "Spades": 3,
             "Hearts": 4}

values = {14: "Ace",
          2: "2",
          3: "3",
          4: "4",
          5: "5",
          6: "6",
          7: "7",
          8: "8",
          9: "9",
          10: "10",
          11: "Jack",
          12: "Queen",
          13: "King"}

values_str = {"Ace": 14,
              "2": 2,
              "3": 3,
              "4": 4,
              "5": 5,
              "6": 6,
              "7": 7,
              "8": 8,
              "9": 9,
              "10": 10,
              "Jack": 11,
              "Queen": 12,
              "King": 13}


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

    def play_card(self, current_suit):
        return self.ai.play_card(self, current_suit)

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

    def play_card(self, computer_player, current_suit):
        return

    def handle_card_click(self, card_ui, current_suit):
        if card_ui is self._selected_card_ui:
            self.player_deselect_card(card_ui)

        elif card_ui.card in self.player.hand:
            card_ui.play_sound()
            if self.is_suit_in_hand(current_suit):
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
    player = None
    def __init__(self):
        return

    def set_player(self, player):
        self.player = player

    def pass_cards(self, computer_player):
        CardLogging.log_file.log('ComputerAI: ' + self.player.name + ': pass cards')

        passing = computer_player.passing

        cards_to_pass = self.determine_cards_to_pass()
        for i in range(0, 3):
            passing.append(cards_to_pass[i])

        return

    def play_card(self, computer_player, current_suit):
        hand = computer_player.hand

        for i in range(0, len(hand)):
            if hand[i].suit is current_suit:
                return hand.pop(i)

        return hand.pop()

    def handle_card_click(self, card_ui, current_suit):
        return

    def handle_keypress(self, event):
        return

    def determine_cards_to_pass(self):

        cards_to_pass = []

        # Pass queen of spades if it's in hand
        queen_of_spades_exists, card = self.has_card(values_str["Queen"], suits_str["Spades"])
        if queen_of_spades_exists:
            cards_to_pass.append(card)

        # Pass ace of spades if it's in hand
        ace_of_spades_exists, card = self.has_card(values_str["Ace"], suits_str["Spades"])
        if ace_of_spades_exists:
            cards_to_pass.append(card)

        # Pass king of spades if it's in hand
        king_of_spades_exists, card = self.has_card(values_str["King"], suits_str["Spades"])
        if king_of_spades_exists:
            cards_to_pass.append(card)

        # Pass highest hearts in hand
        hearts_list = self.get_highest_cards(suits_str["Hearts"], 3 - len(cards_to_pass))
        while len(hearts_list) > 0:
            cards_to_pass.append(hearts_list.pop())

        num_hearts = self.get_number_of_cards_with_suit(suits_str["Hearts"])
        num_clubs = self.get_number_of_cards_with_suit(suits_str["Clubs"])
        num_diamonds = self.get_number_of_cards_with_suit(suits_str["Diamonds"])
        num_spades = self.get_number_of_cards_with_suit(suits_str["Spades"])

        # If the computer can get rid of all hearts, get rid of them
        if num_hearts <= (3 - len(cards_to_pass)):
            hearts_list = self.get_highest_cards(suits_str["Hearts"], 3 - len(cards_to_pass))
            while len(hearts_list) > 0:
                cards_to_pass.append(hearts_list.pop())

        # If the computer can get rid of all clubs, get rid of them
        if num_clubs <= (3 - len(cards_to_pass)):
            clubs_list = self.get_highest_cards(suits_str["Clubs"], 3 - len(cards_to_pass))
            while len(clubs_list) > 0:
                cards_to_pass.append(clubs_list.pop())

        # If the computer can get rid of all diamonds, get rid of them
        if num_diamonds <= (3 - len(cards_to_pass)):
            diamonds_list = self.get_highest_cards(suits_str["Diamonds"], 3 - len(cards_to_pass))
            while len(diamonds_list) > 0:
                cards_to_pass.append(diamonds_list.pop())

        # If the computer can get rid of all spades, get rid of them
        if num_spades <= (3 - len(cards_to_pass)):
            spades_list = self.get_highest_cards(suits_str["Spades"], 3 - len(cards_to_pass))
            while len(spades_list) > 0:
                cards_to_pass.append(spades_list.pop())

        # Get rid of highest diamonds
        diamonds_list = self.get_highest_cards(suits_str["Diamonds"], 3 - len(cards_to_pass))
        while len(diamonds_list) > 0:
            cards_to_pass.append(diamonds_list.pop())

        # Get rid of highest clubs
        clubs_list = self.get_highest_cards(suits_str["Clubs"], 3 - len(cards_to_pass))
        while len(clubs_list) > 0:
            cards_to_pass.append(clubs_list.pop())

        # Get rid of highest hearts
        hearts_list = self.get_highest_cards(suits_str["Hearts"], 3 - len(cards_to_pass))
        while len(hearts_list) > 0:
            cards_to_pass.append(hearts_list.pop())

        # Get rid of highest spades
        spades_list = self.get_highest_cards(suits_str["Spades"], 3 - len(cards_to_pass))
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
        CardLogging.log_file.log('ComputerAI: Number of ' + suits[suit] + ': ' + str(number))
        return number


class Hearts:
    def __init__(self, width=800, height=800):
        Cards.CardEngine.init(width, height)

        # Initialize clock to limit fps
        self.clock = pygame.time.Clock()

        # Initialize the players for the game
        # Bottom is Human Player. Goes clockwise for computers
        # i.e. one is left, two is top, three is right
        self.player_one = Player("Human", HumanAI())
        self.player_two = Player("Sarah", ComputerAI())
        self.player_three = Player("Jane", ComputerAI())
        self.player_four = Player("Smith", ComputerAI())

        # Initialize the trick pile and deck
        self.trick_pile = []
        self.deck = []
        self.shuffled_deck = []

        # Variables to keep track of passing order and whether hearts have been broken
        self.hearts_broken = False
        self.current_suit = suits_str["Clubs"]
        self.current_player = None
        self.passing_order = "Left"
        self.passing_order_list = ["Left", "Right", "Straight", "None"]

        # States the game can be in
        self.state = "Start"
        self.state_list = ["Start", "Passing", "Play", "Scoring", "End"]

        # Load the sprites for the cards into the game
        self.front_sprites = {}
        self.back_sprites = {}
        self.card_ui_elements = []
        self.imagePath = "img/Cards/"
        self.imageType = ".png"
        self.load_sprites()
        self.create_card_ui()

        # Setup the UI elements for the different screens
        self.score_text = []
        self.menu_text = "Welcome to Hearts!  Press start to play."
        self.menu_button = None

        # Setup State Machine for handling game play
        self.stateMachine = StateMachine.StateMachine()

        self.stateMachine.add_state(State.SetupState(self, "Setup"), "Setup")
        self.stateMachine.add_state(State.PassingState(self, "Passing"), "Passing")
        self.stateMachine.add_state(State.PlayingState(self, "Playing"), "Playing")
        self.stateMachine.add_state(State.ScoringState(self, "Scoring"), "Scoring")

        self.stateMachine.set_initial_state("Setup")

        # Link events to the correct functions
        Cards.CardEngine.keyPress += self.stateMachine.handle_keypress

    def load_sprites(self):
        for suit in range(1, 5):
            for value in range(2, 15):
                name = values[value] + " of " + suits[suit]
                sprite = pygame.image.load(self.imagePath + name + self.imageType)
                self.front_sprites[name] = sprite

        for i in range(1, 5):
            name = "Card Back " + str(i)
            sprite = pygame.image.load(self.imagePath + name + self.imageType)
            self.back_sprites[name] = sprite
        return

    def setup_hands(self):
        for i in range(0, 13):
            Cards.CardEngine.deal_cards(self.shuffled_deck, self.player_one.hand, 1)
            Cards.CardEngine.deal_cards(self.shuffled_deck, self.player_two.hand, 1)
            Cards.CardEngine.deal_cards(self.shuffled_deck, self.player_three.hand, 1)
            Cards.CardEngine.deal_cards(self.shuffled_deck, self.player_four.hand, 1)

        self.player_one.set_hand_owner()
        self.player_two.set_hand_owner()
        self.player_three.set_hand_owner()
        self.player_four.set_hand_owner()

    def setup_ui(self):
        one_x = 212
        one_y = 645

        two_x = 150
        two_y = 200

        three_x = 588
        three_y = 150

        four_x = 650
        four_y = 575

        for card_ui in self.card_ui_elements:
            card = card_ui.card

            if card in self.player_one.hand:
                card_ui.angle_degrees = 0
                card_ui.set_location(one_x, one_y)
                card_ui.visible = True
                card_ui.front_view = True
                card_ui.card.owner = self.player_one
                one_x += 25

            elif card in self.player_two.hand:
                card_ui.angle_degrees = 270
                card_ui.set_location(two_x, two_y)
                card_ui.visible = True
                card_ui.front_view = False
                card_ui.card.owner = self.player_two
                two_y += 25

            elif card in self.player_three.hand:
                card_ui.angle_degrees = 180
                card_ui.set_location(three_x, three_y)
                card_ui.visible = True
                card_ui.front_view = False
                card_ui.card.owner = self.player_three
                three_x -= 25

            elif card in self.player_four.hand:
                card_ui.angle_degrees = 90
                card_ui.set_location(four_x, four_y)
                card_ui.visible = True
                card_ui.front_view = False
                card_ui.card.owner = self.player_four
                four_y -= 25

            if card.value is values_str["Ace"] and card.suit is suits_str["Spades"]:
                card_ui.load_sound_file("Sound/The Ace of Spades.wav")

        return

    def create_card_ui(self):
        z = 0
        for card in self.deck:
            front_sprite_name = values[card.value] + " of " + suits[card.suit]
            back_sprite_name = "Card Back 1"

            front_sprite = self.front_sprites[front_sprite_name]
            back_sprite = self.back_sprites[back_sprite_name]
            card_ui = Cards.Card(Cards.CardEngine, card, front_sprite, back_sprite, x=0, y=0, z=z,
                                 callback_function=self.stateMachine.handle_card_click, angle_degrees=0)

            # card_ui.visible = False
            self.card_ui_elements.append(card_ui)
            z += .1

    def play(self):
        while True:
            self.stateMachine.update()
            Cards.CardEngine.update()
            Cards.CardEngine.render()
            self.clock.tick(20)

        return