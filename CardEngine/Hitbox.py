import math


class SquareHitbox(object):
    def __init__(self, x, y, width, height, angle):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.angle = math.radians(angle)

        self.points = []
        self.rotatedPoints = []

        self._get_points()
        self._get_rotated_points()

    def collide(self, x, y):
        # Assuming points a, b, c, and d, and a point m with coordinates (x, y).
        # Check the vector from point a to point m against the vectors from a to b and a to d.
        # Vector math to check if a point is inside the hitbox.  Allows hitbox to be rotated to any angle
        vector_am = Vector(self.rotatedPoints[0].x - x,
                           self.rotatedPoints[0].y - y)
        vector_ab = Vector(self.rotatedPoints[0].x - self.rotatedPoints[1].x,
                           self.rotatedPoints[0].y - self.rotatedPoints[1].y)
        vector_ad = Vector(self.rotatedPoints[0].x - self.rotatedPoints[3].x,
                           self.rotatedPoints[0].y - self.rotatedPoints[3].y)
        if 0 <= vector_am * vector_ab < vector_ab * vector_ab and 0 <= vector_am * vector_ad < vector_ad * vector_ad:
            return True
        else:
            return False

    def update(self, x=None, y=None, width=None, height=None, angle=None):

        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
        if angle is not None:
            self.angle = math.radians(angle)

        self._get_points()
        self._get_rotated_points()

    def _get_points(self):
        self.points = []
        self.points.append(Point(self.x, self.y))
        self.points.append(Point(self.x + self.width, self.y))
        self.points.append(Point(self.x + self.width, self.y + self.height))
        self.points.append(Point(self.x, self.y + self.height))

    def _get_rotated_points(self):
        # Use Point 0 as reference for rotating every point
        x, y = self.points[0].x, self.points[0].y

        self.rotatedPoints = []
        for point in self.points:
            self.rotatedPoints.append(point.copy())

        for point in self.rotatedPoints:
            point.rotate_counterclockwise(x, y, self.angle)

    def _prop_get_x(self):
        return self._x
    def _prop_set_x(self, x):
        self._x = x

    def _prop_get_y(self):
        return self._y
    def _prop_set_y(self, y):
        self._y = y

    def _prop_get_topleft(self):
        return
    def _prop_set_topleft(self, (x, y)):
        return

    def _prop_get_top(self):
        return
    def _prop_set_top(self, top):
        return

    def _prop_get_topright(self):
        return
    def _prop_set_topright(self, (x, y)):
        return

    def _prop_get_left(self):
        return
    def _prop_set_left(self, left):
        return

    def _prop_get_center(self):
        return
    def _prop_set_center(self, (x, y)):
        return

    def _prop_get_center_x(self):
        return
    def _prop_set_center_x(self, center_x):
        return

    def _prop_get_center_y(self):
        return
    def _prop_set_center_y(self, center_y):
        return

    def _prop_get_right(self):
        return
    def _prop_set_right(self, right):
        return

    def _prop_get_bottomleft(self):
        return
    def _prop_set_bottomleft(self, (x, y)):
        return

    def _prop_get_bottom(self):
        return
    def _prop_set_bottom(self, bottom):
        return

    def _prop_get_bottomright(self):
        return
    def _prop_set_bottomright(self, (x, y)):
        return

    def _prop_get_midtop(self):
        return
    def _prop_set_midtop(self, (x, y)):
        return

    def _prop_get_midleft(self):
        return
    def _prop_set_midleft(self, (x, y)):
        return

    def _prop_get_midbottom(self):
        return
    def _prop_set_midbottom(self, (x, y)):
        return

    def _prop_get_midright(self):
        return
    def _prop_set_midright(self, (x, y)):
        return

    def _prop_get_size(self):
        return
    def _prop_set_size(self, (width, height)):
        return

    def _prop_get_width(self):
        return self._width
    def _prop_set_width(self, width):
        self._width = width

    def _prop_get_height(self):
        return self._height
    def _prop_set_height(self, height):
        self._height = height

    def _prop_get_w(self):
        return
    def _prop_set_w(self, w):
        return

    def _prop_get_h(self):
        return
    def _prop_set_h(self, h):
        return

    x = property(_prop_get_x, _prop_set_x)
    y = property(_prop_get_y, _prop_set_y)

    topleft = property(_prop_get_topleft, _prop_set_topleft)
    topright = property(_prop_get_topright, _prop_set_topright)
    bottomleft = property(_prop_get_bottomleft, _prop_set_bottomleft)
    bottomright = property(_prop_get_bottomright, _prop_set_bottomright)

    left = property(_prop_get_left, _prop_set_left)
    top = property(_prop_get_top, _prop_set_top)
    right = property(_prop_get_right, _prop_set_right)
    bottom = property(_prop_get_bottom, _prop_set_bottom)

    midleft = property(_prop_get_midleft, _prop_set_midleft)
    midtop = property(_prop_get_midtop, _prop_set_midtop)
    midright = property(_prop_get_midright, _prop_set_midright)
    midbottom = property(_prop_get_midbottom, _prop_set_midbottom)

    size = property(_prop_get_size, _prop_set_size)
    width = property(_prop_get_width, _prop_set_width)
    height = property(_prop_get_height, _prop_set_height)
    w = property(_prop_get_w, _prop_set_w)
    h = property(_prop_get_h, _prop_set_h)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Point(self.x, self.y)

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate_clockwise(self, x, y, angle_radians):
        # Rotate about the point (x, y) clockwise by a given angle in radians

        nx = math.cos(angle_radians) * (self.x - x) - math.sin(angle_radians) * (self.y - y) + x
        ny = math.sin(angle_radians) * (self.x - x) + math.cos(angle_radians) * (self.y - y) + y

        self.x = nx
        self.y = ny

    def rotate_counterclockwise(self, x, y, angle_radians):
        # Rotate about the point (x, y) counter clockwise by a given angle in radians
        self.rotate_clockwise(x, y, -1 * angle_radians)

    def scale(self, x, y, scalar):
        # Scales about the point (x, y) by a constant scalar
        self.x = math.fabs(self.x - x) * scalar + x
        self.y = math.fabs(self.y - y) * scalar + y

    def reflect(self, axis):
        if axis is 'x' or axis is 'X':
            self.x *= -1
        elif axis is 'y' or axis is 'Y':
            self.y *= -1


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_magnitude(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))

    def get_radians(self):
        return math.acos(self.x / self.get_magnitude())

    def get_degrees(self):
        return math.degrees(self.get_radians())

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __imul__(self, num):
        self.x *= num
        self.y *= num

    def __idiv__(self, num):
        self.x /= num
        self.y /= num

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y
