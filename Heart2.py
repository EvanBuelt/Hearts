__author__ = 'Evan'
import CardEngine.Engine as Cards
import CardEngine.UI as UI
import pygame

suits = {1: "Clubs",
         2: "Diamonds",
         3: "Spades",
         4: "Hearts"}

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

    def play_card(self, computer_player, trick_pile):
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

    def play_card(self, computer_player, trick_pile):
        return


class Hearts:
    def __init__(self, width=800, height=800):
        Cards.CardEngine.init(width, height)

        # Initialize clock to limit fps
        self.clock = pygame.time.Clock()

        # Initialize the players for the game
        # Bottom is Human Player. Goes clockwise for computers
        # i.e. one is left, two is top, three is right
        self.human_player   = Player("Human", HumanAI())
        self.computer_one   = Player("Sarah", ComputerAI())
        self.computer_two   = Player("Jane" , ComputerAI())
        self.computer_three = Player("Smith", ComputerAI())

        # Initialize the trick pile and deck
        self.trick_pile = []
        self.deck = []

        # Variables to keep track of passing order and whether hearts have been broken
        self.hearts_broken = False
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

        # Link events to the correct functions
        Cards.CardEngine.keyPress += self.handle_keypress

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
            Cards.CardEngine.deal_cards(self.deck, self.human_player.hand, 1)
            Cards.CardEngine.deal_cards(self.deck, self.computer_one.hand, 1)
            Cards.CardEngine.deal_cards(self.deck, self.computer_two.hand, 1)
            Cards.CardEngine.deal_cards(self.deck, self.computer_three.hand, 1)
        return

    def setup_ui(self):
        human_x = 212
        human_y = 645

        one_x = 50
        one_y = 212

        two_x = 512
        two_y = 50

        three_x = 650
        three_y = 512

        print "YO"

        for card_ui in self.card_ui_elements:
            print card_ui
            card = card_ui.card

            if card in self.human_player.hand:
                card_ui.angle_degrees = 0
                card_ui.set_location(human_x, human_y)
                card_ui.visible = True
                card_ui.front_view = True
                human_x += 25

            elif card in self.computer_one.hand:
                card_ui.angle_degrees = 90
                card_ui.set_location(one_x, one_y)
                card_ui.visible = True
                card_ui.front_view = False
                one_y += 25

            elif card in self.computer_two.hand:
                card_ui.angle_degrees = 180
                card_ui.set_location(two_x, two_y)
                card_ui.visible = True
                card_ui.front_view = False
                two_x -= 25

            elif card in self.computer_three.hand:
                card_ui.angle_degrees = 270
                card_ui.set_location(three_x, three_y)
                card_ui.visible = True
                card_ui.front_view = False
                three_y -= 25

        return

    def passing_round(self):

        self.computer_one.ai.pass_cards(self.computer_one)
        self.computer_two.ai.pass_cards(self.computer_two)
        self.computer_three.ai.pass_cards(self.computer_three)

        player_one_pass = self.human_player.passing
        player_two_pass = self.computer_one.passing
        player_three_pass = self.computer_two.passing
        player_four_pass = self.computer_three.passing

        if self.passing_order is "Left":

            # Human to computer one
            # Computer one to computer two
            # Computer two to computer three
            # Computer three to Human
            self.passing_order = "Right"

        elif self.passing_order is "Right":
            # Human to computer three
            # Computer one to Human
            # Computer two to computer one
            # Computer three to computer two
            self.passing_order = "Straight"

        elif self.passing_order is "Straight":
            # Human to computer two
            # Computer one to computer three
            # Computer two to Human
            # Computer three to computer one
            self.passing_order = "None"

        elif self.passing_order is "None":
            self.passing_order = "Left"

        return

    def create_card_ui(self):
        z = 0
        for card in self.deck:
            front_sprite_name = values[card.value] + " of " + suits[card.suit]
            back_sprite_name = "Card Back 1"

            front_sprite = self.front_sprites[front_sprite_name]
            back_sprite = self.back_sprites[back_sprite_name]
            card_ui = Cards.Card(Cards.CardEngine, card, front_sprite, back_sprite, x=0, y=0, z=z,
                                 callback_function=self.handle_card_click, angle_degrees=0)

            # card_ui.visible = False
            self.card_ui_elements.append(card_ui)
            z += .1

    def handle_card_click(self, card_ui):
        if self.state is "Start":
            print self.state

        elif self.state is "Setup":
            print self.state

        elif self.state is "Passing":
            card = card_ui.card

            if card in self.human_player.hand:
                if card not in self.human_player.passing:
                    if len(self.human_player.passing) < 3:
                        card_ui.move(0, -25, 0)
                        self.human_player.passing.append(card)
                else:
                    self.human_player.passing.remove(card)
                    card_ui.move(0, 25, 0)

            print self.state

        elif self.state is "Play":
            print self.state

        elif self.state is "Scoring":
            print self.state

        elif self.state is "End":
            print self.state

        print values[card_ui.card.value], "of", suits[card_ui.card.suit]
        return

    def handle_keypress(self, event):
        if self.state is "Start":
            print self.state

        elif self.state is "Setup":
            print self.state

        elif self.state is "Passing":
            if event.type is pygame.KEYDOWN:
                if len(self.human_player.passing) is 3:
                    self.passing_round()
                    self.state = "Play"

            print self.state

        elif self.state is "Play":
            print self.state

        elif self.state is "Scoring":
            print self.state

        elif self.state is "End":
            print self.state

        print event.key, event.type
        return

    def play(self):
        while True:
            if self.state is "Start":
                print self.state

                self.passing_order = "Left"

                self.state = "Setup"

            elif self.state is "Setup":
                print self.state

                self.deck = Cards.CardEngine.create_deck(suits, values)
                Cards.CardEngine.shuffle(self.deck)
                self.create_card_ui()
                self.setup_hands()
                self.setup_ui()
                self.hearts_broken = False

                self.state = "Passing"

            elif self.state is "Passing":
                print self.state

                if self.passing_order is "None":
                    self.passing_order = "Left"
                    self.state = "Play"

            elif self.state is "Play":
                print self.state

            elif self.state is "Scoring":
                print self.state

            elif self.state is "End":
                print self.state

            Cards.CardEngine.update()
            Cards.CardEngine.render()
            self.clock.tick(40)

        return

game = Hearts()
game.play()
