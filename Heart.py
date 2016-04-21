import CardEngine.Engine as Cards
import CardEngine.UI as UI
import pygame
import StateMachine

suits = {1: "Clubs",
         2: "Diamonds",
         3: "Spades",
         4: "Hearts"}\

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


class Player:
    def __init__(self, name, ai):
        self.name = name
        self.ai = ai
        self.hand = []
        self.tricks = []
        self.passing = []
        self.selected_card = None

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


class HumanAI:
    def __init__(self):
        return

    def pass_card(self, human_player, card):
        return

    def play_card(self, computer_player, current_suit):
        return


class ComputerAI:
    def __init__(self):
        return

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

        self.stateMachine.add_state(StateMachine.SetupState(self, "Setup"), "Setup")
        self.stateMachine.add_state(StateMachine.PassingState(self, "Passing"), "Passing")
        self.stateMachine.add_state(StateMachine.PlayingState(self, "Playing"), "Playing")
        self.stateMachine.add_state(StateMachine.ScoringState(self, "Scoring"), "Scoring")

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
        return

    def setup_ui(self):
        one_x = 212
        one_y = 645

        two_x = 75
        two_y = 275

        three_x = 588
        three_y = 150

        four_x = 720
        four_y = 500

        for card_ui in self.card_ui_elements:
            card = card_ui.card

            if card in self.player_one.hand:
                card_ui.angle_degrees = 0
                card_ui.set_location(one_x, one_y)
                card_ui.visible = True
                card_ui.front_view = True
                one_x += 25

            elif card in self.player_two.hand:
                card_ui.angle_degrees = 90
                card_ui.set_location(two_x, two_y)
                card_ui.visible = True
                card_ui.front_view = False
                two_y += 25

            elif card in self.player_three.hand:
                card_ui.angle_degrees = 180
                card_ui.set_location(three_x, three_y)
                card_ui.visible = True
                card_ui.front_view = False
                three_x -= 25

            elif card in self.player_four.hand:
                card_ui.angle_degrees = 270
                card_ui.set_location(four_x, four_y)
                card_ui.visible = True
                card_ui.front_view = False
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