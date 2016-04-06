__author__ = 'Evan'
import sys
import pygame
import random
import UI
import Hitbox

class MouseButton:
    LEFT = 1
    MIDDLE = 2
    RIGHT = 3
    WHEEL_UP = 4
    WHEEL_DOWN = 5


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
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value


class Card(UI.UIElement):
    def __init__(self, engine, card=None, front_surface=None, back_surface=None, rect=None, x=0, y=0, z=0,
                 angle_degrees=0, callback_function=None):

        UI.UIElement.__init__(self, None, rect, z)

        if engine is not None:
            engine.add_card_element(self)

        # Suit and value to be returned on clicking card
        self.card = card

        # Set angle in radians.  Defaults to 0 radians
        self._angle = angle_degrees

        # Set rect if it doesnt exist
        if rect is None:
            self._rect = pygame.Rect(x, y, 60, 30)
        else:
            self._rect = rect
            self._rect.topleft = (x, y)

        # Setup front of card
        if front_surface is None:
            self._frontSurface = pygame.Surface(self._rect.size)
        else:
            self._frontSurface = front_surface.copy()

        # Setup back of card
        if back_surface is None:
            self._backSurface = pygame.Surface(self._rect.size)
        else:
            self._backSurface = back_surface.copy()

        # Create hitbox for the card
        x = self._rect.x  # Syntactic sugar
        y = self._rect.y  # Syntactic sugar
        width = self._frontSurface.get_width()  # Syntactic sugar
        height = self._frontSurface.get_height()  # Syntactic sugar

        self._hitbox = Hitbox.SquareHitbox(x, y, width, height, self._angle)

        # Variables for keeping track of mouse events
        self._lastMouseDownOverCard = False
        self._mouseOverCard = False
        self._cardDown = False
        self._frontView = True

        # Set callback function.
        self._callbackFunction = callback_function

    # Used to render an image to the screen.
    def render(self, surface):
        # As card may be rotated, the x and y positions do not correlate to the top left corner of the card.
        dx = 0
        dy = 0

        x = self._hitbox.rotatedPoints[0].x
        y = self._hitbox.rotatedPoints[0].y
        # Point 0 is reference used for hitbox, so need to offset the display to match the hitbox
        for point in self._hitbox.rotatedPoints:
            if (point.x - x) < dx:
                dx = point.x - x
            if (point.y - y) < dy:
                dy = point.y - y

        # Display front or back of the card
        if self._visible:
            if self._frontView:
                rotated_image = pygame.transform.rotate(self._frontSurface, self._angle)
            else:
                rotated_image = pygame.transform.rotate(self._backSurface, self._angle)

            surface.blit(rotated_image, (self._rect.x + dx, self._rect.y + dy))

    # Used to update the internal state of the UI Element.
    def _update(self):
        self._hitbox.update(x=self._rect.x, y=self._rect.y, angle=self._angle)
        return

    def collide(self, x, y):
        return self._hitbox.collide(x, y)

    def set_callback(self, new_callback_function):
        # Set the callback function to be called upon user hitting the enter key
        self._callbackFunction = new_callback_function

    def handle_event(self, event):
        if event.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN) or not self._visible:
            # The button only cares bout mouse-related events (or no events, if it is invisible)
            return

        x, y = event.pos

        if not self._mouseOverCard and self._hitbox.collide(x, y):
            # if mouse has entered the button:
            self._mouseOverCard = True
        elif self._mouseOverCard and not self._hitbox.collide(x, y):
            # if mouse has exited the button:
            self._mouseOverCard = False

        if self._hitbox.collide(x, y):
            # if mouse event happened over the button:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._cardDown = True
                self._lastMouseDownOverCard = True
        else:
            if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                # if an up/down happens off the button, then the next up won't cause mouseClick()
                self._lastMouseDownOverCard = False

        # mouse up is handled whether or not it was over the button
        do_mouse_click = False
        if event.type == pygame.MOUSEBUTTONUP:
            if self._lastMouseDownOverCard:
                do_mouse_click = True
                self._lastMouseDownOverCard = False

            if self._cardDown:
                self._cardDown = False

            if do_mouse_click:
                self._cardDown = False
                if self._callbackFunction is not None:
                    self._callbackFunction(self)

        self._update()

    def _prop_set_callback_function(self, new_callback_function):
        self._callbackFunction = new_callback_function
        self._update()

    def _prop_get_callback_function(self):
        return self._callbackFunction

    def _prop_set_front_view(self, front_view):
        self._frontView = front_view
        self._update()

    def _prop_get_front_view(self):
        return self._frontView

    def _prop_set_angle_radians(self, angle_radians):
        self._angle = angle_radians * 180 / 3.1415926

    def _prop_get_angle_radians(self):
        return self._angle * 3.1415926 / 180

    def _prop_set_angle_degrees(self, angle_degrees):
        self._angle = angle_degrees

    def _prop_get_angle_degrees(self):
        return self._angle

    callbackFunction = property(_prop_get_callback_function, _prop_set_callback_function)
    front_view = property(_prop_get_front_view, _prop_set_front_view)
    angle_radians = property(_prop_get_angle_radians, _prop_set_angle_radians)
    angle_degrees = property(_prop_get_angle_degrees, _prop_set_angle_degrees)


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
        raise NotImplementedError("CardEgnine cannot be instantiated.")

    @classmethod
    def init(cls, width=800, height=600, display_caption='A Card Game'):
        # Seed needed for shuffling function
        random.seed()

        # Setup the pygame display for use in the Engine
        pygame.init()
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
        for suit in suits:
            for value in values:
                deck.append(StandardPlayingCard(suit, value))
        if special_cards is not None:
            for card in special_cards:
                deck.append(card)
        return deck

    @staticmethod
    def shuffle(deck):
        temp = []
        shuffled = []
        for i in range(0, len(deck)):
            temp.append(deck[i])
        for i in range(0, len(deck)):
            rand = random.randrange(0, len(deck) - i)
            shuffled.append(temp.pop(rand))
        return shuffled

    # Methods below deal with transferring cards.
    @staticmethod
    def deal_cards(deck, hand, number_cards):
        if len(deck) < number_cards:
            number_cards = len(deck)
        for i in range(0, number_cards):
            hand.append(deck.pop())

    @staticmethod
    def transfer_card(card, source, destination):
        if card in source:
            source.pop(card)
            destination.append(card)

    @staticmethod
    def transfer_cards(card_list, source, destination):
        for card in card_list:
            if card in source:
                source.remove(card)
                destination.append(card)
