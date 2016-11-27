import pygame

from CardEngine import Engine
import CardEngine.UI
from Core.StateMachine import StateMachine
from Core.StateMachine import State
from Core.Player.AI import AI
import Constant


'''
11/26/2016
General setup:
Hearts
-Variables:
    -Players
    -Trick Pile
    -Deck
    -Hearts Broken
    -Current Suit

-Internal Variables:
    -_State_Machine
    -_Internal Deck (used in conjunction with card UI)
    -_Front Sprites
    -_Back Sprites
    -_Image Path
    -_Image Type
    -_Sound Path
    -_Sound Type
    -_clock

-Setup:
    -Setup four players with appropriate AI
    -Setup deck
    -Setup State Machine with appropriate states
    -Setup defaults for hearts broken and current suit
    -Setup Clock for looping
    -Link Engine Callbacks appropriately
    -Load sprites and sounds
    -Setup Card UIs
    -Setup locations of cards in hand

States
-Setup:
    -Take deck and shuffle it
    -Deal shuffled deck to players hand
    -Set hearts broken to false
    -Set initial suit to Clubs
    -Set initial passing hands for all players to empty
    -Set initial trick pile to empty
-Passing:
    -Determine passing direction for round
    -Get passing cards for computer players
    -Wait for human player to choose cards
    -Pass cards to appropriate players
-Playing:
    -Wait for each player to play a card
    -Determine who receive a trick pile
    -

'''


class Player(object):
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

        # Selection sort by value first
        for i in range(1, len(self.hand)):
            j = i
            while j > 0 and self.hand[j - 1].value > self.hand[j].value:
                temp = self.hand[j]
                self.hand[j] = self.hand[j - 1]
                self.hand[j - 1] = temp
                j -= 1

        # Selection sort by suit second
        for i in range(1, len(self.hand)):
            j = i
            while j > 0 and self.hand[j - 1].suit > self.hand[j].suit:
                temp = self.hand[j]
                self.hand[j] = self.hand[j - 1]
                self.hand[j - 1] = temp
                j -= 1

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
        # Initialize the pygame Engine
        Engine.CardEngine.init(width, height)

        # Initialize the players for the game
        # Bottom is Human Player.  Goes clockwise for computers
        self.player_one = Player("Human", AI.HumanAI())
        self.player_two = Player("Sarah", AI.ComputerAI())
        self.player_three = Player("Jane", AI.ComputerAI())
        self.player_four = Player("Smith", AI.ComputerAI())

        # Initialize the deck
        self.trick_pile = []
        self.deck = []

        # Variables for playing
        self.heartsBroken = False
        self.currentSuit = Constant.Suit.Clubs

        # Load the sprites for the cards into the game
        self.front_sprites = {}
        self.back_sprites = {}
        self.card_ui_elements = []
        self.imagePath = "Res/img/Cards/"
        self.imageType = ".png"
        self.load_sprites()
        self.setup_deck()

        # Setup State Machine for handling game play
        self.stateMachine = StateMachine.StateMachine()

        self.stateMachine.add_state(State.SetupState(self, "Setup"), "Setup")
        self.stateMachine.add_state(State.PassingState(self, "Passing"), "Passing")
        self.stateMachine.add_state(State.PlayingState(self, "Playing"), "Playing")
        self.stateMachine.add_state(State.ScoringState(self, "Scoring"), "Scoring")

        self.stateMachine.set_initial_state("Setup")

        # Link events to the correct functions
        Engine.CardEngine.keyPress += self.stateMachine.handle_keypress

        # Initialize clock to limit fps
        self.clock = pygame.time.Clock()

    # Initialization functions
    def load_sprites(self):
        for suit in range(1, 5):
            for value in range(2, 15):
                name = Constant.value_str[value] + " of " + Constant.suit_str[suit]
                sprite = pygame.image.load(self.imagePath + name + self.imageType)
                self.front_sprites[name] = sprite

        for i in range(1, 5):
            name = "Card Back " + str(i)
            sprite = pygame.image.load(self.imagePath + name + self.imageType)
            self.back_sprites[name] = sprite
        return

    def setup_ui(self):
        # Card width: 75
        # Card height: 105
        # Card width/2: 37.5
        # Card height/2: 52.5

        # Hand Width: 75 + 12 * 25 = 375
        # Hand width/2: 187.5

        # Horizontal center: 400
        # Left Card left side: 400 - 187.5 = 212.5
        one_x = 212
        one_y = 615
        one_z = 0

        # Vertical center: 400
        # Top card top side: 400 - 187.5 - 37.5 = 175
        two_x = 80
        two_y = 212
        two_z = 0

        # Horizontal center: 400
        # Right card right side: 400 + 187.5 = 550
        three_x = 512
        three_y = 80
        three_z = 0

        four_x = 615
        four_y = 512
        four_z = 0

        self.player_one.sort_hand()
        self.player_two.sort_hand()
        self.player_three.sort_hand()
        self.player_four.sort_hand()

        for card_ui in self.card_ui_elements:
            card = card_ui.card

            if card in self.player_one.hand:
                card_ui.angle_degrees = 0
                card_ui.set_location(one_x, one_y)
                card_ui.visible = True
                card_ui.front_view = True
                card_ui.card.owner = self.player_one
                card_ui.z = one_z
                one_x += 25
                one_z += .1

            elif card in self.player_two.hand:
                card_ui.angle_degrees = 270
                card_ui.set_location(two_x, two_y)
                card_ui.visible = True
                card_ui.front_view = False
                card_ui.card.owner = self.player_two
                card_ui.z = two_z
                two_y += 25
                two_z += .1

            elif card in self.player_three.hand:
                card_ui.angle_degrees = 180
                card_ui.set_location(three_x, three_y)
                card_ui.visible = True
                card_ui.front_view = False
                card_ui.card.owner = self.player_three
                card_ui.z = three_z
                three_x -= 25
                three_z += .1

            elif card in self.player_four.hand:
                card_ui.angle_degrees = 90
                card_ui.set_location(four_x, four_y)
                card_ui.visible = True
                card_ui.front_view = False
                card_ui.card.owner = self.player_four
                card_ui.z = four_z
                four_y -= 25
                four_z += .1

            if card.value is Constant.Value.Ace and card.suit is Constant.Suit.Spades:
                card_ui.load_sound_file("Res/Sound/The Ace of Spades.wav")

        return

    def _create_card_ui(self):
        z = 0
        for card in self.deck:
            front_sprite_name = Constant.value_str[card.value] + " of " + Constant.suit_str[card.suit]
            back_sprite_name = "Card Back 1"

            front_sprite = self.front_sprites[front_sprite_name]
            back_sprite = self.back_sprites[back_sprite_name]
            card_ui = CardEngine.UI.CardUI(card, front_sprite, back_sprite, x=0, y=0, z=z,
                                           callback_function=self.stateMachine.handle_card_click, angle_degrees=0)

            card_ui.visible = False
            self.card_ui_elements.append(card_ui)
            z += .1

    def setup_deck(self):
        self.deck = []
        card_values = [Constant.Value.Two,
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

        card_suits = [Constant.Suit.Clubs,
                      Constant.Suit.Diamonds,
                      Constant.Suit.Spades,
                      Constant.Suit.Hearts]

        self.deck = Engine.CardEngine.create_deck(card_suits, card_values)

    # Utility functions
    def determine_playable_cards(self, hand):
        playable_cards = []
        # Player will play first card.  Can only play hearts if broken
        if self.currentSuit is None:
            for card in hand:
                if not self.heartsBroken:
                    if card.suit is not Constant.Suit.Hearts:
                        playable_cards.append(card)
                else:
                    playable_cards.append(card)
        # Otherwise, player is not going first, and player must follow the suit
        else:
            for card in hand:
                if card.suit is self.currentSuit:
                    playable_cards.append(card)

        # Player either has no card of current suit or only has hearts left.  Therefore, player can play anything
        if len(playable_cards) is 0:
            for card in hand:
                playable_cards.append(card)

        return playable_cards


    # Entry Function for playing hearts
    def play(self):
        while True:
            self.stateMachine.update()
            Engine.CardEngine.update()
            Engine.CardEngine.render()
            self.clock.tick(20)

        return
