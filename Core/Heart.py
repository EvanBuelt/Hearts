from CardEngine import Engine
from StateMachine import StateMachine
from StateMachine import State
import AI
import Constant
import pygame


class Player:
    def __init__(self, name, ai):
        self.name = name
        self.ai = ai
        self.hand = []
        self.tricks = []
        self.cards_to_pass = []
        self.selected_card = None
        self.round_points = []
        self.total_points = 0

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


class Hearts:
    def __init__(self, width=800, height=800):
        Engine.CardEngine.init(width, height)

        # Initialize clock to limit fps
        self.clock = pygame.time.Clock()

        # Initialize the players for the game
        # Bottom is Human Player. Goes clockwise for computers
        # i.e. one is left, two is top, three is right
        self.player_one = Player("Human", AI.HumanAI())
        self.player_two = Player("Sarah", AI.ComputerAI())
        self.player_three = Player("Jane", AI.ComputerAI())
        self.player_four = Player("Smith", AI.ComputerAI())

        # Initialize the deck
        self.trick_pile = []
        self.deck = []

        # Load the sprites for the cards into the game
        self.front_sprites = {}
        self.back_sprites = {}
        self.card_ui_elements = []
        self.imagePath = "img/Cards/"
        self.imageType = ".png"
        self.load_sprites()
        self.create_card_ui()

        # Setup State Machine for handling game play
        self.stateMachine = StateMachine.StateMachine()

        self.stateMachine.add_state(State.SetupState(self, "Setup"), "Setup")
        self.stateMachine.add_state(State.PassingState(self, "Passing"), "Passing")
        self.stateMachine.add_state(State.PlayingState(self, "Playing"), "Playing")
        self.stateMachine.add_state(State.ScoringState(self, "Scoring"), "Scoring")

        self.stateMachine.set_initial_state("Setup")

        # Link events to the correct functions
        Engine.CardEngine.keyPress += self.stateMachine.handle_keypress

    def load_sprites(self):
        for suit in range(1, 5):
            for value in range(2, 15):
                name = Constant.value_int_to_str[value] + " of " + Constant.suit_int_to_str[suit]
                sprite = pygame.image.load(self.imagePath + name + self.imageType)
                self.front_sprites[name] = sprite

        for i in range(1, 5):
            name = "Card Back " + str(i)
            sprite = pygame.image.load(self.imagePath + name + self.imageType)
            self.back_sprites[name] = sprite
        return

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

            if card.value is Constant.value_str_to_int["Ace"] and card.suit is Constant.suit_str_to_int["Spades"]:
                card_ui.load_sound_file("Sound/The Ace of Spades.wav")

        return

    def create_card_ui(self):
        z = 0
        for card in self.deck:
            front_sprite_name = Constant.value_int_to_str[card.value] + " of " + Constant.suit_int_to_str[card.suit]
            back_sprite_name = "Card Back 1"

            front_sprite = self.front_sprites[front_sprite_name]
            back_sprite = self.back_sprites[back_sprite_name]
            card_ui = Engine.Card(Engine.CardEngine, card, front_sprite, back_sprite, x=0, y=0, z=z,
                                  callback_function=self.stateMachine.handle_card_click, angle_degrees=0)

            card_ui.visible = False
            self.card_ui_elements.append(card_ui)
            z += .1

    def play(self):
        while True:
            self.stateMachine.update()
            Engine.CardEngine.update()
            Engine.CardEngine.render()
            self.clock.tick(20)

        return
