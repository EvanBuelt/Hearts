import sys
import random
import pygame
import UI
import Core.Constant


class EventHandler:
    def __init__(self):
        self.functions = []

    def __iadd__(self, function):
        if function not in self.functions:
            self.functions.append(function)
        return self

    def __isub__(self, function):
        if function in self.functions:
            self.functions.remove(function)
        return self

    def notify(self, *args):
        for function in self.functions:
            function(*args)


class StandardPlayingCard:
    def __init__(self, suit, value, owner=None):
        self.suit = suit
        self.value = value
        self.owner = owner

    def __eq__(self, other):
        if self.suit == other.suit and self.value == other.value:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.suit != other.suit or self.value != other.value:
            return True
        else:
            return False


class CardEngine:
    # Pygame Display
    DISPLAYSURFACE = None
    width = 0
    height = 0

    # Event handlers for various events, to be linked internally and externally
    mouseClick = EventHandler()
    cardClick = EventHandler()
    mouseMovement = EventHandler()
    keyPress = EventHandler()
    gameQuit = EventHandler()

    # List of UI Elements
    UIElements = []

    # List of Cards
    CardElements = []

    def __init__(self):
        raise NotImplementedError("CardEngine cannot be instantiated.")

    @classmethod
    def init(cls, width=800, height=600, display_caption='A Card Game'):
        # Seed needed for shuffling function
        random.seed()

        # Setup the pygame display for use in the Engine
        pygame.init()
        UI.init()
        cls.width = width
        cls.height = height
        cls.DISPLAYSURFACE = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption(display_caption)

    @classmethod
    def update(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Notify other parts before closing the window and exiting program.
                cls.gameQuit.notify()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                cls.mouseClick.notify(event)

            elif event.type == pygame.MOUSEBUTTONUP:
                cls.mouseClick.notify(event)

            elif event.type == pygame.MOUSEMOTION:
                cls.mouseMovement.notify(event)

            elif event.type == pygame.KEYDOWN:
                cls.keyPress.notify(event)

            elif event.type == pygame.KEYUP:
                cls.keyPress.notify(event)

            # Handle events for cards
            cls._handle_card_click(event)

            # Let UI handle events
            for ui in cls.UIElements:
                ui.handle_event(event)

    @classmethod
    def render(cls):
        cls.DISPLAYSURFACE.fill((70, 200, 70))
        cls._sort_ui_elements()
        cls._sort_card_elements()

        for ui in cls.UIElements:
            ui.render(cls.DISPLAYSURFACE)
        for card in cls.CardElements:
            card.render(cls.DISPLAYSURFACE)

        pygame.display.update()

    @classmethod
    def _handle_card_click(cls, event):
        if event.type not in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]:
            return

        x, y = event.pos
        clicked = []

        for card in cls.CardElements:
            if card.collide(x, y):
                clicked.append(card)

        if len(clicked) is 0:
            return

        card_display = clicked[0]
        for card in clicked:
            if card.z > card_display.z:
                card_display = card

        card_display.handle_event(event)

    # Methods below are used to handle the ui elements on screen.
    @classmethod
    def _sort_ui_elements(cls):
        for i in range(1, len(cls.UIElements)):
            j = i
            while (j > 0) and (cls.UIElements[j - 1].z > cls.UIElements[j].z):
                temp = cls.UIElements[j]
                cls.UIElements[j] = cls.UIElements[j - 1]
                cls.UIElements[j - 1] = temp
                j -= 1

    @classmethod
    def _sort_card_elements(cls):
        for i in range(1, len(cls.CardElements)):
            j = i
            while (j > 0) and (cls.CardElements[j - 1].z > cls.CardElements[j].z):
                temp = cls.CardElements[j]
                cls.CardElements[j] = cls.CardElements[j - 1]
                cls.CardElements[j - 1] = temp
                j -= 1

    @classmethod
    def add_ui_element(cls, ui_element):
        if ui_element not in cls.UIElements:
            cls.UIElements.append(ui_element)
        cls._sort_ui_elements()

    @classmethod
    def remove_ui_element(cls, ui_element):
        if ui_element in cls.UIElements:
            cls.UIElements.remove(ui_element)

    @classmethod
    def remove_all_ui_elements(cls):
        del cls.UIElements[:]

    @classmethod
    def add_card_element(cls, card):
        if card not in cls.UIElements:
            cls.CardElements.append(card)
        cls._sort_ui_elements()

    @classmethod
    def remove_card_element(cls, card):
        if card in cls.UIElements:
            cls.CardElements.remove(card)

    @classmethod
    def remove_all_card_elements(cls):
        del cls.CardElements[:]

    # Methods below are used to create and shuffle a deck.
    @staticmethod
    def create_deck(suits, values, special_cards=None):
        deck = []

        # Create a standard playing card with given suit and value
        for suit in suits:
            for value in values:
                deck.append(StandardPlayingCard(suit, value))

        # Add any special cards, such as jokers
        if special_cards is not None:
            for card in special_cards:
                deck.append(card)

        return deck

    @staticmethod
    def shuffle(deck):
        temp = []
        shuffled = []

        # Create a temporary deck to not mess with the original deck
        for i in range(0, len(deck)):
            temp.append(deck[i])

        # Get a random card from the temporary deck and move it to the end of the shuffled deck
        for i in range(0, len(deck)):
            rand = random.randrange(0, len(deck) - i)
            shuffled.append(temp.pop(rand))

        return shuffled

    # Methods below deal with transferring cards.
    @staticmethod
    def deal_cards(deck, hand, number_cards):
        # Ensure that you don't try to pass too many cards
        if len(deck) < number_cards:
            number_cards = len(deck)

        # Add hands from deck to hand
        for i in range(0, number_cards):
            hand.append(deck.pop())

        # Return number of cards passed, as it may be different than requested
        return number_cards

    @staticmethod
    def transfer_card(card, source, destination):
        if card in source:
            source.remove(card)
            destination.append(card)

    @staticmethod
    def transfer_cards(card_list, source, destination):
        for card in card_list:
            CardEngine.transfer_card(card, source, destination)

    @staticmethod
    def copy_card(card, source, destination):
        if card in source:
            destination.append(card)

    @staticmethod
    def copy_card_list(card_list, source, destination):
        for card in card_list:
            CardEngine.copy_card(card, source, destination)

    @staticmethod
    def transfer_list(source, destination):
        destination += source
        del source[:]

    @staticmethod
    def copy_list(old_list):
        new_list = []
        for item in old_list:
            new_list.append(item)
        return new_list
