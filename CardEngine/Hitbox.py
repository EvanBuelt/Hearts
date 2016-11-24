import math
import CardEngine.VectorMath


class Hitbox2D(object):
    def __init__(self, points=None):
        # If no points were passed in, then initialize an empty array.  Otherwise,
        if points is None:
            self.original_points = []
            self._x = 0
            self._y = 0
        else:
            self.original_points = [point for point in points]
            self._x = self.original_points[0].x
            self._y = self.original_points[0].y
        # Points used to create triangles.  Need copy of original points as overlapping hitboxes
        # will add or remove points.
        self.hitbox_points = [point for point in self.original_points]

        # Triangles will be created to detect a mouse collision
        self.triangles = []

    def _update(self):
        self._create_triangles()

    def _create_triangles(self):
        self.triangles = []
        if len(self.hitbox_points) >= 3:
            for i in range(0, len(self.original_points) - 2):
                point_1 = self.original_points[0]
                point_2 = self.original_points[i + 1]
                point_3 = self.original_points[i + 2]

                self.triangles.append(CardEngine.VectorMath.Triangle2D(point_1, point_2, point_3))

    def collidepoint(self, x, y):
        collide_result = False
        for triangle in self.triangles:
            collide_result |= triangle.collidepoint(x, y)
        return collide_result

    def colliderect(self, rect):
        (x, y) = rect.topleft
        width = rect.width
        height = rect.height

        collide_result = self.collidepoint(x, y) or self.collidepoint(x + width, y) or \
                         self.collidepoint(x + width, y + height) or self.collidepoint(x, y + height)

        for point in self.original_points:
            collide_result |= rect.collide(point.x, point.y)

        return collide_result

    def collidehitbox(self, hitbox):
        collide_result = False

        for point in hitbox.original_points:
            collide_result |= self.collidepoint(point.x, point.y)

        for point in self.original_points:
            collide_result |= hitbox.collidepoint(point.x, point.y)

        return collide_result

    def _prop_get_x(self):
        return self._x
    def _prop_set_x(self, x):
        self._x = x
        self._update()

    def _prop_get_y(self):
        return self._y
    def _prop_set_y(self, y):
        self._y = y
        self._update()

    x = property(_prop_get_x, _prop_set_x)
    y = property(_prop_get_y, _prop_set_y)


class SquareHitbox2D(Hitbox2D):
    def __init__(self, x, y, width, height, angle):
        Hitbox2D.__init__(self, [CardEngine.VectorMath.Point2D(x, y),
                                 CardEngine.VectorMath.Point2D(x + width, y),
                                 CardEngine.VectorMath.Point2D(x + width, y + height),
                                 CardEngine.VectorMath.Point2D(x, y + height)])

        self._width = width
        self._height = height
        self._angle = math.radians(angle)

        self._update_original_points()
        self._get_rotated_points()

    def collide(self, x, y):
        # Assuming points a, b, c, and d, and a point m with coordinates (x, y).
        # Check the vector from point a to point m against the vectors from a to b and a to d.
        # Vector math to check if a point is inside the hitbox.  Allows hitbox to be rotated to any angle
        vector_am = CardEngine.VectorMath.Vector2D(self.rotatedPoints[0].x - x,
                                                   self.rotatedPoints[0].y - y)
        vector_ab = CardEngine.VectorMath.Vector2D(self.rotatedPoints[0].x - self.rotatedPoints[1].x,
                                                   self.rotatedPoints[0].y - self.rotatedPoints[1].y)
        vector_ad = CardEngine.VectorMath.Vector2D(self.rotatedPoints[0].x - self.rotatedPoints[3].x,
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

        self._update_original_points()
        self._get_rotated_points()

    def _update(self):
        Hitbox2D._update(self)

    def _update_original_points(self):
        self.original_points[0].x = self.x
        self.original_points[0].y = self.y

        self.original_points[1].x = self.x + self.width
        self.original_points[1].y = self.y

        self.original_points[2].x = self.x + self.width
        self.original_points[2].y = self.y + self.height

        self.original_points[3].x = self.x
        self.original_points[3].y = self.y + self.height

    def _get_rotated_points(self):
        # Use Point 0 as reference for rotating every point
        x, y = self.original_points[0].x, self.original_points[0].y

        self.rotatedPoints = [point.copy() for point in self.original_points]

        for point in self.rotatedPoints:
            point.rotate_counterclockwise(x, y, self._angle)

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
