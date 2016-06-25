import CardEngine.Engine as Cards
import CardEngine.UI as UI
import pygame
import StateMachine.StateMachine as StateMachine
import StateMachine.State as State

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
        passing = computer_player.passing
        hand = computer_player.hand

        passing.append(hand[0])
        passing.append(hand[1])
        passing.append(hand[2])
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

        return

    def create_card_ui(self):
        z = 0
        for card in self.deck:
            print card.value, card.suit
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