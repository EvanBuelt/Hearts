import pygame
from CardEngine import Hitbox
import CardEngine.Engine

UI_FONT = None

BLACK = (0, 0, 0, 255)
DARKGRAY = (64, 64, 64, 255)
GRAY = (128, 128, 128, 255)
LIGHTGRAY = (140, 140, 140, 255)
LIGHTGRAY2 = (212, 208, 200, 255)
WHITE = (255, 255, 255, 255)
TRANSPARENT = (255, 255, 255, 0)
GREEN = (24, 119, 24, 255)


def init():
    """
    Initializes the Font used in the text
    :return:
    """
    pygame.font.init()
    global UI_FONT
    UI_FONT = pygame.font.Font(pygame.font.match_font('gentiumbookbasic'), 20)


class _InheritanceError(Exception):
    """
    Inheritance Error is used to ensure certain class methods are inherited.
    """
    def __init__(self, value):
        """
        :param value: Message to be displayed when error is raised
        :return:
        """
        self.value = value

    def __str__(self):
        """

        :return: Returns message to be displayed for errors
        """
        return repr(self.value)


class UIElement(object):
    """
    Element on the screen that interacts with user.  This is the base class that should be used when creating
    new UI Elements.

    The following methods must be overridden:
    -render: Used to display the UI Element to the screen (or another pygame surface)
    -_update: Updates internal elements
    -handle_event: Function to handle pygame events from the engine.

    Variables:
    -rect: x and y location, as well as size of the image
    -z: variable used to determine order in which UI Elements are displayed and handled
    -visible: Used to determines if the UI Element is displayed and will handle events
    """
    def __init__(self, rect, z):
        """
        Initializes the UI Element for basic interaction with the engine
        :param rect:
        :param z:
        :return:
        """

        # Set location of UI Element.  Defaulted to location 0, 0, and width 60 and height 30
        if rect is None:
            (x, y) = (0, 0)
            (w, h) = (60, 30)
            self._rect = pygame.Rect((x, y), (w, h))
        else:
            self._rect = pygame.Rect(rect)

        self._z = z
        self._visible = True

        # Adds the UI Element to the Card Engine
        CardEngine.Engine.CardEngine.add_ui_element(self)

    # Functions all subclasses must override
    def render(self, surface):
        """Renders the current UI Element to the desired surface input"""
        raise _InheritanceError('Function not defined')

    def _update(self):
        """Update the internal state of the UI Element"""
        raise _InheritanceError('Function not defined')

    def handle_event(self, event):
        """
        Method to handle pygame events
        :param event: Pygame event passed in by the Engine.
        :return:
        """
        raise _InheritanceError('Function not defined')

    # Common functions for location
    def set_location(self, x, y, z=0):
        """
        Sets the top left location of a pygame rect
        :param x: x location
        :param y: y location
        :param z: z location
        :return:
        """
        self._rect.topleft = (x, y)
        self._z = z
        self._update()

    def move(self, dx, dy, dz=0):
        """
        Moves the UI Element by a given dx, dy, and a default dz of 0
        :param dx: Moves the pygame rect dx units
        :param dy: Moves the pygame rect dy units
        :param dz: Optional parameter default to 0 that moves the UI Element in the z-direction
        :return:
        """
        (x, y) = self._rect.topleft
        self._rect.topleft = (x + dx, y + dy)
        self._z += dz
        self._update()

    # Collision functions
    def collide(self, x, y):
        """
        Determines if a point collides with the UI Element
        :param x: X location
        :param y: Y location
        :return:
        """
        return self._rect.collidepoint(x, y)

    def collide_ui(self, ui_element):
        """
        Determines if two UI Elements collide
        :param ui_element: Other UI Element to check for collision
        :return:
        """
        return self._rect.colliderect(ui_element.rect)

    # Properties to access variables
    def _prop_get_rect(self):
        return self._rect
    def _prop_set_rect(self, new_rect):
        self._rect = pygame.Rect(new_rect)
        self._update()
        return

    def _prop_get_z(self):
        return self._z
    def _prop_set_z(self, new_z):
        self._z = new_z
        self._update()
        return

    def _prop_get_visible(self):
        return self._visible
    def _prop_set_visible(self, visible):
        self._visible = visible
        self._update()
        return

    rect = property(_prop_get_rect, _prop_set_rect)
    z = property(_prop_get_z, _prop_set_z)
    visible = property(_prop_get_visible, _prop_set_visible)


class CardUI(UIElement):
    def __init__(self, card=None, front_surface=None, back_surface=None, rect=None, x=0, y=0, z=0,
                 angle_degrees=0, callback_function=None):

        UIElement.__init__(self, rect, z)

        # Workaround for the time being.
        # UI Elements are not expected to overlap, while cards are.
        # Engine handles events with cards differently than other UI Elements as a result
        CardEngine.Engine.CardEngine.remove_ui_element(self)
        CardEngine.Engine.CardEngine.add_card_element(self)

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

        # Setup sound to playback when requested
        self._sound = None
        self._start_time = 0

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

    def play_sound(self):
        if self._sound is not None:
            print pygame.time.get_ticks()
            print self._start_time
            print self._sound.get_length() * 1000
            if (pygame.time.get_ticks() - self._start_time) > (self._sound.get_length() * 1000):
                self._sound.play()
                self._start_time = pygame.time.get_ticks()

    def load_sound_file(self, file_path):
        self._sound = pygame.mixer.Sound(file_path)
        self._sound.set_volume(0.2)

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
        self._update()
    def _prop_get_angle_radians(self):
        return self._angle * 3.1415926 / 180

    def _prop_set_angle_degrees(self, angle_degrees):
        self._angle = angle_degrees
        self._update()
    def _prop_get_angle_degrees(self):
        return self._angle

    def _prop_get_sound(self):
        return self._sound
    def _prop_set_sound(self, sound):
        self._sound = sound

    callbackFunction = property(_prop_get_callback_function, _prop_set_callback_function)
    front_view = property(_prop_get_front_view, _prop_set_front_view)
    angle_radians = property(_prop_get_angle_radians, _prop_set_angle_radians)
    angle_degrees = property(_prop_get_angle_degrees, _prop_set_angle_degrees)
    sound = property(_prop_get_sound, _prop_set_sound)
# The following classes are used as a base for common UI Elements.  The first way to handle UI Elements is to
# use a callback function, which will be triggered internally in reaction to pygame events.  The second way is to
# use inheritance to override several methods in the UI Element class.  These methods are called in the handle_event
# method that will call the overridden methods.

# As both classes share several commonalities, a base class is used.
# This base class is internal to the UI module, and does not handle events,
# so it should not be referenced outside this module.

# Standard UI Elements:
# Text (Output)
# TextBox (Input)
# CheckBox (Input)
# Button (Input)


class _BaseText(UIElement):
    def __init__(self, rect=None, z=0, text='',
                 background_color=TRANSPARENT, text_color=BLACK, font=None):

        UIElement.__init__(self, rect, z)

        # Set color of background and text color
        self._bgColor = background_color
        self._textColor = text_color

        if text is '':
            self._text = 'Text'
        else:
            self._text = text

        if font is None:
            self._font = UI_FONT
        else:
            self._font = font

        # Create standard surface for text
        self._surfaceNormal = pygame.Surface(self._rect.size).convert_alpha()
        self._update()

    def render(self, surface):
        if self._visible:
            surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        # Make syntax pretty
        w = self.rect.width
        h = self.rect.height

        # Update surface to fit size of rect
        self._surfaceNormal = pygame.Surface(self._rect.size).convert_alpha()
        self._surfaceNormal.fill(self._bgColor)

        # Draw text on surface
        text_surf = self.font.render(self._text, True, self._textColor)
        text_rect = text_surf.get_rect()
        text_rect.center = int(w / 2), int(h / 2)
        self._surfaceNormal.blit(text_surf, text_rect)

    def handle_event(self, event):
        return

    def _prop_get_text(self):
        return self._text
    def _prop_set_text(self, new_text):
        self._text = new_text
        self._update()
        return

    def _prop_get_font(self):
        return self._font
    def _prop_set_font(self, new_font):
        self._font = new_font
        self._update()
        return

    def _prop_get_background_color(self):
        return self._bgColor
    def _prop_set_background_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()
        return

    def _prop_get_text_color(self):
        return self._textColor
    def _prop_set_text_color(self, new_text_color):
        self._textColor = new_text_color
        self._update()
        return

    text = property(_prop_get_text, _prop_set_text)
    text_color = property(_prop_get_text_color, _prop_set_text_color)
    font = property(_prop_get_font, _prop_set_font)
    background_color = property(_prop_get_background_color, _prop_set_background_color)


class _BaseTextBox(UIElement):
    def __init__(self, rect=None, z=0, background_text=None, background_color=WHITE,
                 input_text_color=BLACK, background_text_color=LIGHTGRAY, font=None):

        UIElement.__init__(self, rect, z)

        # Set values for surface display
        self._bgColor = background_color
        self._inputTextColor = input_text_color
        self._bgTextColor = background_text_color

        # Input text uses a list that is converted to a string (which is immutable)
        self._inputText = ''
        self._listInputText = []

        # Background text
        if background_text is None:
            self._bgText = 'Input'
        else:
            self._bgText = background_text

        # If no font is given, use gentium book, font size 12
        if font is None:
            self._font = UI_FONT
        else:
            self._font = font

        # Track mouse click events and keyboard inputs
        self._isSelected = False
        self._lastMouseDownOverTextBox = False
        self._keydown = False

        # Create Surface
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceInput = pygame.Surface(self._rect.size)

        self._update()

    def render(self, surface):
        if self._visible:
            if self._inputText is not '':
                surface.blit(self._surfaceInput, self._rect)
            else:
                surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        # Syntactic sugar for height and width for text
        w = self._rect.width
        h = self._rect.height

        # Start with a clean slate for the surfaces with background color
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceInput = pygame.Surface(self._rect.size)

        self._surfaceNormal.fill(self._bgColor)
        self._surfaceInput.fill(self._bgColor)

        # Create background text
        bg_text_surf = self._font.render(self._bgText, True, self._bgTextColor, self._bgColor)
        bg_text_rect = bg_text_surf.get_rect()
        bg_text_rect.left = 5
        bg_text_rect.centery = int(h / 2)
        self._surfaceNormal.blit(bg_text_surf, bg_text_rect)

        # Create input text
        self._listInputText = [y for y in self._listInputText if y != '']
        self._inputText = str(''.join(self._listInputText))
        input_text_surf = self._font.render(self._inputText, True, self._inputTextColor, self._bgColor)
        input_text_rect = input_text_surf.get_rect()
        input_text_rect.left = 5
        input_text_rect.centery = int(h / 2)
        self._surfaceInput.blit(input_text_surf, input_text_rect)

        # Update normal surface used not selected and no input
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.line(self._surfaceNormal, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceNormal, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, GRAY, (1, h - 2), (w - 2, h - 2))
        pygame.draw.line(self._surfaceNormal, GRAY, (w - 2, 1), (w - 2, h - 2))

        # Update input surface used for when selected or there is input
        pygame.draw.rect(self._surfaceInput, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.line(self._surfaceInput, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceInput, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surfaceInput, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceInput, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, GRAY, (1, h - 2), (w - 2, h - 2))
        pygame.draw.line(self._surfaceNormal, GRAY, (w - 2, 1), (w - 2, h - 2))

    def _prop_get_background_text(self):
        return self._bgText
    def _prop_set_background_text(self, new_background_text):
        self._bgText = new_background_text
        self._update()

    def _prop_get_background_color(self):
        return self._bgColor
    def _prop_set_background_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()

    def _prop_get_input_text(self):
        return self._inputText
    def _prop_set_input_text(self, new_input_text):
        self._listInputText = []
        for char in new_input_text:
            self._listInputText.append(char)

    def _prop_get_input_text_color(self):
        return self._inputTextColor
    def _prop_set_input_text_color(self, new_input_text_color):
        self._inputTextColor = new_input_text_color
        self._update()

    def _prop_get_background_text_color(self):
        return self._bgTextColor
    def _prop_set_background_text_color(self, new_background_text_color):
        self._bgTextColor = new_background_text_color
        self._update()

    def _prop_get_font(self):
        return self._font
    def _prop_set_font(self, new_font):
        self._font = new_font
        self._update()

    backgroundText = property(_prop_get_background_text, _prop_set_background_text)
    backgroundTextColor = property(_prop_get_background_text_color, _prop_set_background_text_color)
    backgroundColor = property(_prop_get_background_color, _prop_set_background_color)
    inputText = property(_prop_get_input_text, _prop_set_input_text)
    inputTextColor = property(_prop_get_input_text_color, _prop_set_input_text_color)
    font = property(_prop_get_font, _prop_set_font)


class _BaseCheckBox(UIElement):
    def __init__(self, rect=None, z=0, background_color=WHITE):
        # Set position of element

        UIElement.__init__(self, rect, z)

        self._bgColor = background_color

        # Variables to track internal state in reaction to events
        self._isChecked = False
        self._lastMouseDownOverCheckBox = False

        # Images to be displayed on screen
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceChecked = pygame.Surface(self._rect.size)

        self._update()

    def render(self, surface):
        if self._visible:
            if self._isChecked:
                surface.blit(self._surfaceChecked, self._rect)
            else:
                surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        # Create blank surfaces to be drawn upon
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceChecked = pygame.Surface(self._rect.size)

        # Syntactic sugar
        w = self._rect.width
        h = self._rect.height

        # Create unchecked surface
        self._surfaceNormal.fill(self._bgColor)
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((1, 1, w - 2, h - 2)), 1)

        # Create checked surface
        self._surfaceChecked.fill(self._bgColor)
        pygame.draw.rect(self._surfaceChecked, BLACK, pygame.Rect((0, 0, w, h)), 1)
        pygame.draw.rect(self._surfaceChecked, BLACK, pygame.Rect((1, 1, w - 2, h - 2)), 1)
        pygame.draw.line(self._surfaceChecked, GREEN, (3, int(h / 2)), (int(w / 2), h - 5), 3)
        pygame.draw.line(self._surfaceChecked, GREEN, (int(w / 2), h - 5), (w - 5, 4), 3)

    def _prop_get_background_color(self):
        return self._bgColor
    def _prop_set_background_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()

    def _prop_get_is_checked(self):
        return self._isChecked
    def _prop_set_is_checked(self, is_checked):
        self._isChecked = is_checked
        self._update()

    backgroundColor = property(_prop_get_background_color, _prop_set_background_color)
    checked = property(_prop_get_is_checked, _prop_set_is_checked)


class _BaseButton(UIElement):
    def __init__(self, rect=None, z=0, text='',
                 background_color=LIGHTGRAY, foreground_color=BLACK, font=None):

        UIElement.__init__(self, rect, z)

        # set text and color to be applied to blank surfaces
        self._text = text
        self._bgColor = background_color
        self._fgColor = foreground_color

        # set font for text
        if font is None:
            self._font = UI_FONT
        else:
            self._font = font

        # create blank surfaces to be created in update
        pygame.Surface((200, 300))
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceDown = pygame.Surface(self._rect.size)
        self._surfaceHighlight = pygame.Surface(self._rect.size)

        # tracks the state of the button
        self._buttonDown = False  # is the button currently pushed down?
        self._mouseOverButton = False  # is the mouse currently hovering over the button?
        self._lastMouseDownOverButton = False  # was the last mouse down event over the mouse button? (Tracks clicks.)

        # update graphics for the button
        self._update()

    def render(self, surface):
        if self._visible:
            if self._buttonDown:
                surface.blit(self._surfaceDown, self._rect)
            elif self._mouseOverButton:
                surface.blit(self._surfaceHighlight, self._rect)
            else:
                surface.blit(self._surfaceNormal, self._rect)

    def _update(self):
        self._surfaceNormal = pygame.Surface(self._rect.size)
        self._surfaceDown = pygame.Surface(self._rect.size)
        self._surfaceHighlight = pygame.Surface(self._rect.size)

        # syntactic sugar
        w = self._rect.width
        h = self._rect.height

        # fill background color for all buttons
        self._surfaceNormal.fill(self._bgColor)
        self._surfaceDown.fill(self._bgColor)
        self._surfaceHighlight.fill(self._bgColor)

        # draw caption text for all buttons
        caption_surf = self._font.render(self._text, True, self._fgColor, self._bgColor)
        caption_rect = caption_surf.get_rect()
        caption_rect.center = int(w / 2), int(h / 2)
        self._surfaceNormal.blit(caption_surf, caption_rect)
        self._surfaceDown.blit(caption_surf, caption_rect)

        # draw border for normal button
        pygame.draw.rect(self._surfaceNormal, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self._surfaceNormal, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceNormal, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surfaceNormal, DARKGRAY, (1, h - 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, DARKGRAY, (w - 1, 1), (w - 1, h - 1))
        pygame.draw.line(self._surfaceNormal, GRAY, (2, h - 2), (w - 2, h - 2))
        pygame.draw.line(self._surfaceNormal, GRAY, (w - 2, 2), (w - 2, h - 2))

        # draw border for down button
        pygame.draw.rect(self._surfaceDown, BLACK, pygame.Rect((0, 0, w, h)), 1)  # black border around everything
        pygame.draw.line(self._surfaceDown, WHITE, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceDown, WHITE, (1, 1), (1, h - 2))
        pygame.draw.line(self._surfaceDown, DARKGRAY, (1, h - 2), (1, 1))
        pygame.draw.line(self._surfaceDown, DARKGRAY, (1, 1), (w - 2, 1))
        pygame.draw.line(self._surfaceDown, GRAY, (2, h - 3), (2, 2))
        pygame.draw.line(self._surfaceDown, GRAY, (2, 2), (w - 3, 2))

        # draw border for highlight button
        self._surfaceHighlight = self._surfaceNormal

    def _prop_get_background_color(self):
        return self._bgColor
    def _prop_set_background_color(self, new_background_color):
        self._bgColor = new_background_color
        self._update()

    def _prop_get_foreground_color(self):
        return self._fgColor
    def _prop_set_foreground_color(self, new_foreground_color):
        self._fgColor = new_foreground_color
        self._update()

    def _prop_get_font(self):
        return self._font
    def _prop_set_font(self, new_font):
        self._visible = new_font
        self._update()

    def _prop_get_text(self):
        return self._text
    def _prop_set_text(self, new_text):
        self._text = new_text
        self._update()

    foregroundColor = property(_prop_get_foreground_color, _prop_set_foreground_color)
    backgroundColor = property(_prop_get_background_color, _prop_set_background_color)
    font = property(_prop_get_font, _prop_set_font)
    text = property(_prop_get_text, _prop_set_text)


# The following UI Elements use a callback function
class Text(_BaseText):
    def __init__(self, rect=None, z=0, text='',
                 background_color=TRANSPARENT, text_color=BLACK, font=None):
        # Let base handle most of initialization.  Base class should call _update.
        _BaseText.__init__(self, rect, z, text,
                           background_color, text_color, font)


class TextBox(_BaseTextBox):
    def __init__(self, rect=None, z=0, background_text=None, background_color=WHITE,
                 input_text_color=BLACK, background_text_color=LIGHTGRAY,
                 font=None, callback_function=None):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseTextBox.__init__(self, rect, z, background_text, background_color,
                              input_text_color, background_text_color, font)

        # Set callback function.
        self._callbackFunction = callback_function

    def handle_event(self, event):
        # Track only mouse presses and key presses
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
            if self._rect.collidepoint(event.pos):
                # clicking and releasing inside textbox selects textbox
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._lastMouseDownOverTextBox = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._lastMouseDownOverTextBox:
                        self._isSelected = True
                    self._lastMouseDownOverTextBox = False
            else:
                # releasing mouse outside textbox deselects textbox
                self._lastMouseDownOverTextBox = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self._isSelected = False

        if event.type is pygame.KEYDOWN and self._isSelected:
            if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                if len(self._listInputText) > 0:
                    self._listInputText.pop()

            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                pass  # Future update.  Allow user to move cursor location

            elif event.key in (pygame.K_TAB, pygame.K_ESCAPE):
                pass  # Events to ignore

            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                if self._callbackFunction is not None:
                    self._callbackFunction(self)

            else:
                self._listInputText.append(event.unicode)

        self._update()

    def _prop_get_callback_function(self):
        return self._callbackFunction
    def _prop_set_callback_function(self, new_callback_function):
        self._callbackFunction = new_callback_function
        self._update()

    callbackFunction = property(_prop_get_callback_function, _prop_set_callback_function)


class CheckBox(_BaseCheckBox):
    def __init__(self, rect=None, z=0, background_color=WHITE, callback_function=None):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseCheckBox.__init__(self, rect, z, background_color)

        # Set function to be called when checked or unchecked
        self._callbackFunction = callback_function

    def handle_event(self, event):
        # Track only mouse presses and key presses
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN) or not self._visible:
            return

        if self._rect.collidepoint(event.pos):
            # clicking and releasing inside checkbox toggles check
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._lastMouseDownOverCheckBox = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self._lastMouseDownOverCheckBox and self._isChecked:
                    self._isChecked = False
                    if self._callbackFunction is not None:
                        self._callbackFunction(self)
                elif self._lastMouseDownOverCheckBox and not self._isChecked:
                    self._isChecked = True
                    if self._callbackFunction is not None:
                        self._callbackFunction(self)
                self._lastMouseDownOverCheckBox = False
        else:
            self._lastMouseDownOverCheckBox = False

        self._update()

    def _prop_get_callback_function(self):
        return self._callbackFunction
    def _prop_set_callback_function(self, new_callback_function):
        self._callbackFunction = new_callback_function
        self._update()

    callbackFunction = property(_prop_get_callback_function, _prop_set_callback_function)


class Button(_BaseButton):
    def __init__(self, rect=None, z=0, text='',
                 background_color=LIGHTGRAY, foreground_color=BLACK, font=None,
                 callback_function=None):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseButton.__init__(self, rect, z, text,
                             background_color, foreground_color, font)

        # Set callback if provided
        self._callbackFunction = callback_function

    def handle_event(self, event):
        if event.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN) or not self._visible:
            # The button only cares bout mouse-related events (or no events, if it is invisible)
            return

        if not self._mouseOverButton and self._rect.collidepoint(event.pos):
            # if mouse has entered the button:
            self._mouseOverButton = True
        elif self._mouseOverButton and not self._rect.collidepoint(event.pos):
            # if mouse has exited the button:
            self._mouseOverButton = False

        if self._rect.collidepoint(event.pos):
            # if mouse event happened over the button:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._buttonDown = True
                self._lastMouseDownOverButton = True
        else:
            if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                # if an up/down happens off the button, then the next up won't cause mouseClick()
                self._lastMouseDownOverButton = False

        # mouse up is handled whether or not it was over the button
        do_mouse_click = False
        if event.type == pygame.MOUSEBUTTONUP:
            if self._lastMouseDownOverButton:
                do_mouse_click = True
                self._lastMouseDownOverButton = False

            if self._buttonDown:
                self._buttonDown = False

            if do_mouse_click:
                self._buttonDown = False
                if self._callbackFunction is not None:
                    self._callbackFunction(self)

        self._update()

    def _prop_get_callback_function(self):
        return self._callbackFunction
    def _prop_set_callback_function(self, new_callback_function):
        self._callbackFunction = new_callback_function
        self._update()

    callbackFunction = property(_prop_get_callback_function, _prop_set_callback_function)


# UI Elements below, denoted with a prefix of Py-, are intended to be inherited.
# Several methods have been set up, but not defined.  These methods are to be handled by the programmer.

# The following methods are to be overwritten as necessary:
#   -mouse_click: called when mouse clicked.
#   -mouse_enter: called when mouse entered UI Element
#   -mouse_exit: called when mouse no longer over UI Element
#   -mouse_down: called when mouse pressed
#   -mouse_up: called when mouse released
#   -keyboard_down: called when key pressed
#   -keyboard_up: called when key released


class PyText(_BaseText):
    def __init__(self, rect=None, z=0, text='',
                 background_color=TRANSPARENT, text_color=BLACK, font=None):
        # Let base handle most of initialization.  Base class should call _update.
        _BaseText.__init__(self, rect, z, text,
                           background_color, text_color, font)

        self._mouseOverText = False
        self._lastMouseDownOverText = False
        self._isSelected = False

    def handle_event(self, event):
        # Track only mouse presses and key presses, if visible
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        has_exited = False
        do_mouse_click = False

        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if not self._mouseOverText and self.rect.collidepoint(event.pos):
                # if mouse has entered the button:
                self._mouseOverText = True
                self.mouse_enter(event)
            elif self._mouseOverText and not self.rect.collidepoint(event.pos):
                # if mouse has exited the button:
                self._mouseOverText = False
                has_exited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

            if self._rect.collidepoint(event.pos):
                # if mouse event happened over the check box:
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_move(event)

                # clicking and releasing inside textbox selects it
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._lastMouseDownOverText = True
                    self.mouse_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._lastMouseDownOverText:
                        self._isSelected = True
                        do_mouse_click = True
                    self._lastMouseDownOverText = False
                    self.mouse_up(event)
            else:
                # releasing mouse click outside textbox deselects it
                self._lastMouseDownOverText = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self._isSelected = False

            if do_mouse_click:
                self.mouse_click(event)

            if has_exited:
                self.mouse_exit(event)

        elif event.type is pygame.KEYUP:
            self.keyboard_up(event)

        else:
            self.keyboard_down(event)

        self._update()

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def keyboard_down(self, event):
        pass

    def keyboard_up(self, event):
        pass


class PyTextBox(_BaseTextBox):
    def __init__(self, rect=None, z=0, background_text=None, background_color=WHITE,
                 input_text_color=BLACK, background_text_color=LIGHTGRAY, font=None):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseTextBox.__init__(self, rect, z, background_text, background_color,
                              input_text_color, background_text_color, font)

        self._mouseOverTextBox = False

    def handle_event(self, event):
        # Track only mouse presses and key presses, if visible
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        has_exited = False
        do_mouse_click = False

        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if not self._mouseOverTextBox and self.rect.collidepoint(event.pos):
                # if mouse has entered the button:
                self._mouseOverTextBox = True
                self.mouse_enter(event)
            elif self._mouseOverTextBox and not self.rect.collidepoint(event.pos):
                # if mouse has exited the button:
                self._mouseOverTextBox = False
                has_exited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

            if self._rect.collidepoint(event.pos):
                # if mouse event happened over the check box:
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_move(event)

                # clicking and releasing inside textbox selects it
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._lastMouseDownOverTextBox = True
                    self.mouse_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._lastMouseDownOverTextBox:
                        self._isSelected = True
                        do_mouse_click = True
                    self._lastMouseDownOverTextBox = False
                    self.mouse_up(event)
            else:
                # releasing mouse click outside textbox deselects it
                self._lastMouseDownOverTextBox = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self._isSelected = False

            if do_mouse_click:
                self.mouse_click(event)

            if has_exited:
                self.mouse_exit(event)

        elif event.type is pygame.KEYUP:
            self.keyboard_up(event)

        else:
            self.keyboard_down(event)

        self._update()

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def keyboard_down(self, event):
        pass

    def keyboard_up(self, event):
        pass


class PyCheckBox(_BaseCheckBox):
    def __init__(self, rect=None, z=0, background_color=WHITE):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseCheckBox.__init__(self, rect, z, background_color)

        # Variables to be used in handling events
        self._mouseOverCheckBox = False

    def handle_event(self, event):
        # Track only mouse presses and key presses, if visible
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        has_exited = False
        do_mouse_click = False

        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if not self._mouseOverCheckBox and self.rect.collidepoint(event.pos):
                # if mouse has entered the button:
                self._mouseOverCheckBox = True
                self.mouse_enter(event)
            elif self._mouseOverCheckBox and not self.rect.collidepoint(event.pos):
                # if mouse has exited the button:
                self._mouseOverCheckBox = False
                has_exited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

            if self._rect.collidepoint(event.pos):
                # if mouse event happened over the check box:
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_move(event)

                # clicking and releasing inside checkbox toggles check
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._lastMouseDownOverCheckBox = True
                    self.mouse_down(event)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self._lastMouseDownOverCheckBox and self._isChecked:
                        self._isChecked = False
                        do_mouse_click = True
                    elif self._lastMouseDownOverCheckBox and not self._isChecked:
                        self._isChecked = True
                        do_mouse_click = True
                    self._lastMouseDownOverCheckBox = False
                    self.mouse_up(event)
            else:
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    self._lastMouseDownOverCheckBox = False

            if do_mouse_click:
                self.mouse_click(event)

            if has_exited:
                self.mouse_exit(event)

        elif event.type is pygame.KEYUP:
            self.keyboard_up(event)

        else:
            self.keyboard_down(event)

        self._update()

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def keyboard_down(self, event):
        pass

    def keyboard_up(self, event):
        pass


class PyButton(_BaseButton):
    def __init__(self, rect=None, z=0, text='',
                 background_color=LIGHTGRAY, foreground_color=BLACK, font=None):

        # Let base handle most of initialization.  Base class should call _update.
        _BaseButton.__init__(self, rect, z, text,
                             background_color, foreground_color, font)

    def handle_event(self, event):
        # Track only mouse presses and key presses, if visible
        if event.type not in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION,
                              pygame.KEYUP, pygame.KEYDOWN) or not self._visible:
            return

        has_exited = False
        if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION):
            if not self._mouseOverButton and self.rect.collidepoint(event.pos):
                # if mouse has entered the button:
                self._mouseOverButton = True
                self.mouse_enter(event)
            elif self._mouseOverButton and not self.rect.collidepoint(event.pos):
                # if mouse has exited the button:
                self._mouseOverButton = False
                has_exited = True  # call mouseExit() later, since we want mouseMove() to be handled before mouseExit()

            if self.rect.collidepoint(event.pos):
                # if mouse event happened over the button:
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_move(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._buttonDown = True
                    self._lastMouseDownOverButton = True
                    self.mouse_down(event)
            else:
                if event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN):
                    # if an up/down happens off the button, then the next up won't cause mouseClick()
                    self._lastMouseDownOverButton = False

            # mouse up is handled whether or not it was over the button
            do_mouse_click = False
            if event.type == pygame.MOUSEBUTTONUP:
                if self._lastMouseDownOverButton:
                    do_mouse_click = True
                self._lastMouseDownOverButton = False

                if self._buttonDown:
                    self._buttonDown = False
                    self.mouse_up(event)

                if do_mouse_click:
                    self._buttonDown = False
                    self.mouse_click(event)

            if has_exited:
                self.mouse_exit(event)
        elif event.type is pygame.KEYUP:
            self.keyboard_up(event)

        else:
            self.keyboard_down(event)

        self._update()

    def mouse_click(self, event):
        pass

    def mouse_enter(self, event):
        pass

    def mouse_move(self, event):
        pass

    def mouse_exit(self, event):
        pass

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def keyboard_down(self, event):
        pass

    def keyboard_up(self, event):
        pass
