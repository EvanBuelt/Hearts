import math


class Triangle(object):
    def __init__(self, point_a, point_b, point_c):
        self._points = [point_a, point_b, point_c]

    def collidepoint(self, *args):
        """
        The collide point takes in two different arguments.  One is a tuple, and the other is a Point.
        :param args: Either (x, y) or Point
        :return: Returns True if point is inside the triangle
        """
        # Length of 2 implies the input is a tuple
        if len(args) is 2:
            x = args[0]
            y = args[1]
        # Length of 1 implies input is a point
        elif len(args) is 1:
                x = args[0].x
                y = args[0].y

        else:
            raise ValueError("Improper values passed in")

        point_a = self._points[0]
        point_b = self._points[1]
        point_c = self._points[2]

        # Compute vectors
        v0 = Vector(point_c.x - point_a.x, point_c.y - point_a.y)
        v1 = Vector(point_b.x - point_a.x, point_b.y - point_b.y)
        v2 = Vector(x - point_a.x, y - point_b.y)

        # Compute dot products
        dot00 = v0 * v0
        dot01 = v0 * v1
        dot02 = v0 * v2
        dot11 = v1 * v1
        dot12 = v1 * v2

        # Compute barycentric coordinates
        denominator = 1 / (dot00 * dot11 - dot01 * dot01)
        u = (dot11 * dot02 - dot01 * dot12) * denominator
        v = (dot00 * dot12 - dot01 * dot02) * denominator

        # Check if point is in triangle
        return (u >= 0) and (v >= 0) and (u + v < 1)

    def collidetriangle(self, triangle):
        """
        Takes another Triangle class and returns whether either triangle collides with each other
        :param triangle: Triangle class
        :return: Returns true if either Triangle intersect the other
        """
        for point in triangle._points:
            if self.collidepoint(point):
                return True
        for point in self._points:
            if triangle.collidepoint(point):
                return True
        return False

    def _prop_getpointa(self):
        return self._points[0]
    def _prop_setpointa(self, pointa):
        self._points[0] = pointa

    def _prop_getpointb(self):
        return self._points[1]
    def _prop_setpointb(self, pointb):
        self._points[1] = pointb

    def _prop_getpointc(self):
        return self._points[2]
    def _prop_setpointc(self, pointc):
        self._points[2] = pointc

    pointa = property(_prop_getpointa, _prop_setpointa)
    pointb = property(_prop_getpointb, _prop_setpointb)
    pointc = property(_prop_getpointc, _prop_setpointc)


class Hitbox(object):
    def __init__(self, points=None):
        if points is None:
            self.points = []
        else:
            self.points = points
        self.points = []


class SquareHitbox(object):
    def __init__(self, x, y, width, height, angle):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._angle = math.radians(angle)

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

    def update(self, **kwargs):

        if 'x' in kwargs:
            self._x = kwargs['x']
        if 'y' in kwargs:
            self._y = kwargs['y']
        if 'width' in kwargs:
            self._width = kwargs['width']
        if 'height' in kwargs:
            self._height = kwargs['height']
        if 'degrees' in kwargs:
            self._angle = math.radians(kwargs['degrees'])
        elif 'radians' in kwargs:
            self._angle = kwargs['radians']

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
            point.rotate_counterclockwise(x, y, self._angle)

    def _prop_get_x(self):
        return self._x
    def _prop_set_x(self, x):
        self._x = x
        self.update()

    def _prop_get_y(self):
        return self._y
    def _prop_set_y(self, y):
        self._y = y
        self.update()

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
        return (self._width, self._height)
    def _prop_set_size(self, (width, height)):
        self._width = width
        self._height = height
        self.update()

    def _prop_get_width(self):
        return self._width
    def _prop_set_width(self, width):
        self._width = width
        self.update()

    def _prop_get_height(self):
        return self._height
    def _prop_set_height(self, height):
        self._height = height
        self.update()

    def _prop_get_w(self):
        return self._width
    def _prop_set_w(self, w):
        self._width = w
        self.update()

    def _prop_get_h(self):
        return self._height
    def _prop_set_h(self, h):
        self._height = h
        self.update()

    def _prop_get_radians(self):
        return self._angle
    def _prop_set_radians(self, angle):
        self._angle = angle
        self.update()

    def _prop_get_degrees(self):
        return math.degrees(self._angle)
    def _prop_set_degrees(self, degrees):
        self._angle = math.radians(degrees)
        self.update()

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
        self.x = float(x)
        self.y = float(y)

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

    def __eq__(self, *args):
        if len(args) is 1:
            other = args[0]
            if isinstance(other, type(self)):
                return (self.x == other.x) and (self.y == other.y)
            elif isinstance(other, type((1, 0))) or isinstance(other, type((1., 2.))):
                return (self.x == other[0]) and (self.y == other[1])

        raise ValueError('Invalid Values For Comparison')

    def __ne__(self, *args):
        if len(args) is 1:
            other = args[0]
            if isinstance(other, type(self)):
                return (self.x != other.x) or (self.y != other.y)
            elif isinstance(other, type((1, 0))) or isinstance(other, type((1., 2.))):
                return (self.x != other[0]) or (self.y != other[1])

        raise ValueError('Invalid Values For Comparison')


class Vector:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def magnitude(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))

    def length(self):
        return self.magnitude()

    def normalize(self):
        return Vector(self.x/self.length(), self.y/self.length())

    def scale(self, scalar):
        self.x *= scalar
        self.y *= scalar

    def dot(self, other):
        return self.x*other.x + self.y*other.y

    def get_angle_between_vectors(self, other):
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))

    def get_radians(self):
        result = math.atan2(self.y, self.x)
        if result < 0:
            result += 2 * math.pi
        return result

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
        return self.x*other.x + self.y*other.y

    def __eq__(self, *args):
        if len(args) is 1:
            other = args[0]
            if isinstance(other, type(self)):
                return (self.x == other.x) and (self.y == other.y)
            elif isinstance(other, type((1, 0))) or isinstance(other, type((1., 2.))):
                return (self.x == other[0]) and (self.y == other[1])

        raise ValueError('Invalid Values For Comparison')

    def __ne__(self, *args):
        if len(args) is 1:
            other = args[0]
            if isinstance(other, type(self)):
                return (self.x != other.x) or (self.y != other.y)
            elif isinstance(other, type((1, 0))) or isinstance(other, type((1., 2.))):
                return (self.x != other[0]) or (self.y != other[1])

        raise ValueError('Invalid Values For Comparison')
