import pygame
import CardEngine.Engine

__author__ = 'Evan'


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
        :param rect: Pygame Rect
        :param z: number
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
        :param event: Pygame event
        :return:
        """
        raise _InheritanceError('Function not defined')

    # Common functions for location
    def set_location(self, x, y, z=0):
        """
        Sets the top left location of a pygame rect
        :param x: num
        :param y: num
        :param z: num
        :return:
        """
        self._rect.topleft = (x, y)
        self._z = z
        self._update()

    def move(self, dx, dy, dz=0):
        """
        Moves the UI Element by a given dx, dy, and a default dz of 0
        :param dx: num
        :param dy: num
        :param dz: Optional parameter default to 0.  num
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
