import CardEngine.UI
import CardEngine.Engine
import CardEngine.Hitbox
import sys
import pygame
import unittest


__author__ = 'Evan'


# Tests to verify the Point class
class PointTests(unittest.TestCase):
    def test_point(self):
        # Create point at (4, 5)
        p = CardEngine.Hitbox.Point2D(4, 5)

        # Verify point was created at (4, 5)
        self.assertEqual(p.x, 4)
        self.assertEqual(p.y, 5)

        # Update point directly to (7, 9)
        p.x = 7
        p.y = 9

        # Verify point moved to (7, 9)
        self.assertEqual(p.x, 7)
        self.assertEqual(p.y, 9)

    def test_copy(self):
        # Create point at (2, 3) and copy of that point
        p = CardEngine.Hitbox.Point2D(2, 3)
        q = p.copy()

        # Verify points are in the same location
        self.assertEqual(p.x, q.x)
        self.assertEqual(p.y, q.y)

        # Move original point to (5, 6)
        p.x = 5
        p.y = 6

        # Verify points are not in the same location
        self.assertNotEqual(p.x, q.x)
        self.assertNotEqual(p.y, q.y)

    def test_translate(self):
        # Create point at (3, 3)
        p = CardEngine.Hitbox.Point2D(3, 3)

        # Move point in positive direction to (5 ,6)
        p.translate(2, 3)

        # Verify point moved to (5, 6)
        self.assertEqual(p.x, 5)
        self.assertEqual(p.y, 6)

        # Move point in negative direction to (-4, 2)
        p.translate(-9, -8)

        # Verify point moved to (-4, -2)
        self.assertEqual(p.x, -4)
        self.assertEqual(p.y, -2)

    def test_rotate_clockwise(self):
        # Create point at (3, 3)
        p = CardEngine.Hitbox.Point2D(3, 3)

        # Rotate point about (0, 0) 90 degrees to (y, -x) = (3, -3) and verify
        p.rotate_clockwise(0, 0, 1.570796327)
        self.assertAlmostEqual(p.x, -3, 7)
        self.assertAlmostEqual(p.y, 3, 7)

        # Rotate point about (0, 0) 90 degrees to (y, -x) = (-3, -3) and verify
        p.rotate_clockwise(0, 0, 1.570796327)
        self.assertAlmostEqual(p.x, -3, 7)
        self.assertAlmostEqual(p.y, -3, 7)

        # Rotate point about (0, 0) 90 degrees to (y, -x) = (-3, 3) and verify
        p.rotate_clockwise(0, 0, 1.570796327)
        self.assertAlmostEqual(p.x, 3, 7)
        self.assertAlmostEqual(p.y, -3, 7)

        # Rotate point about (0, 0) 90 degrees to (y, -x) = (3, 3) and verify
        p.rotate_clockwise(0, 0, 1.570796327)
        self.assertAlmostEqual(p.x, 3, 7)
        self.assertAlmostEqual(p.y, 3, 7)

    def test_rotate_counterclockwise(self):
        # Create point at (3, 3)
        p = CardEngine.Hitbox.Point2D(3, 3)

        # Rotate point about (0, 0) 90 degrees to (-y, x) = (-3, 3) and verify
        p.rotate_counterclockwise(0, 0, 1.5707963268)
        self.assertAlmostEqual(p.x, 3, 5)
        self.assertAlmostEqual(p.y, -3, 5)

        # Rotate point about (0, 0) 90 degrees to (-y, x) = (-3, -3) and verify
        p.rotate_counterclockwise(0, 0, 1.5707963268)
        self.assertAlmostEqual(p.x, -3, 5)
        self.assertAlmostEqual(p.y, -3, 5)

        # Rotate point about (0, 0) 90 degrees to (-y, x) = (3, -3) and verify
        p.rotate_counterclockwise(0, 0, 1.5707963268)
        self.assertAlmostEqual(p.x, -3, 5)
        self.assertAlmostEqual(p.y, 3, 5)

        # Rotate point about (0, 0) 90 degrees to (-y, x) = (3, 3) and verify
        p.rotate_counterclockwise(0, 0, 1.5707963268)
        self.assertAlmostEqual(p.x, 3, 5)
        self.assertAlmostEqual(p.y, 3, 5)

    def test_scale(self):
        # Create point at (3, 3)
        p = CardEngine.Hitbox.Point2D(3, 3)

        # Scale point to twice as big as before
        p.scale(0, 0, 2)
        self.assertAlmostEqual(p.x, 6, 5)
        self.assertAlmostEqual(p.y, 6, 5)

        # Scale point to half as big as before
        p.scale(0, 0, .5)
        self.assertAlmostEqual(p.x, 3, 5)
        self.assertAlmostEqual(p.y, 3, 5)

    def test_reflect(self):
        # Create point at (3, 3)
        p = CardEngine.Hitbox.Point2D(3, 3)
        self.addTypeEqualityFunc(type(p), p.__eq__)

        # Reflect point about x-axis
        p.reflect('x')
        self.assertEqual(p, (-3, 3))

        # Reflect point about y-axis)
        p.reflect('y')
        self.assertEqual(p, (-3, -3))

        # Reflect point about x-axis
        p.reflect('X')
        self.assertEqual(p, (3, -3))

        # Reflect point about y-axis
        p.reflect('Y')
        self.assertEqual(p, (3, 3))


# Tests to verify the Vector class
class VectorTests(unittest.TestCase):

    def test_Vector(self):
        v1 = CardEngine.Hitbox.Vector2D(2, 4)

        self.assertAlmostEqual(v1.x, 2, 5)
        self.assertAlmostEqual(v1.y, 4, 5)

        return

    def test_magnitude(self):
        v1 = CardEngine.Hitbox.Vector2D(3, 4)
        v2 = CardEngine.Hitbox.Vector2D(2, 2)
        v3 = CardEngine.Hitbox.Vector2D(-3, 2)
        v4 = CardEngine.Hitbox.Vector2D(-4, -5)
        v5 = CardEngine.Hitbox.Vector2D(2, -4)

        # Verify both magnitude and length methods for first vector
        self.assertAlmostEqual(v1.magnitude(), 5, 5)
        self.assertAlmostEqual(v1.length(), 5, 5)

        # Verify both magnitude and length methods for second vector
        self.assertAlmostEqual(v2.magnitude(), 2.8284271, 5)
        self.assertAlmostEqual(v2.length(), 2.8284271, 5)

        # Verify both magnitude and length methods for third vector
        self.assertAlmostEqual(v3.magnitude(), 3.60555127, 5)
        self.assertAlmostEqual(v3.length(), 3.60555127, 5)

        # Verify both magnitude and length methods for third vector
        self.assertAlmostEqual(v4.magnitude(), 6.4031242, 5)
        self.assertAlmostEqual(v4.length(), 6.4031242, 5)

        # Verify both magnitude and length methods for third vector
        self.assertAlmostEqual(v5.magnitude(), 4.4721359, 5)
        self.assertAlmostEqual(v5.length(), 4.4721359, 5)
        return

    def test_normalize(self):
        v1 = CardEngine.Hitbox.Vector2D(2, 2)
        v2 = v1.normalize()

        self.assertAlmostEqual(v1.x, 2, 7)
        self.assertAlmostEqual(v1.y, 2, 7)

        self.assertAlmostEqual(v2.x, .7071068, 5)
        self.assertAlmostEqual(v2.y, .7071068, 5)

    def test_angles(self):
        v1 = CardEngine.Hitbox.Vector2D(2, 2)
        v2 = CardEngine.Hitbox.Vector2D(1, 5)
        v3 = CardEngine.Hitbox.Vector2D(-3, -2)
        v4 = CardEngine.Hitbox.Vector2D(-4, 0)
        v5 = CardEngine.Hitbox.Vector2D(3, -9)

        # Verify angle for vector 1
        self.assertAlmostEqual(v1.get_degrees(), 45, 5)
        self.assertAlmostEqual(v1.get_radians(), 0.78539816, 5)

        # Verify angle for vector 2
        self.assertAlmostEqual(v2.get_degrees(), 78.69006770, 5)
        self.assertAlmostEqual(v2.get_radians(), 1.37340077, 5)

        # Verify angle for vector 3
        self.assertAlmostEqual(v3.get_degrees(), 213.69006755, 5)
        self.assertAlmostEqual(v3.get_radians(), 3.72959525, 5)

        # Verify angle for vector 4
        self.assertAlmostEqual(v4.get_degrees(), 180, 5)
        self.assertAlmostEqual(v4.get_radians(), 3.14159265, 5)

        # Verify angle for vector 5
        self.assertAlmostEqual(v5.get_degrees(), 288.4349468, 5)
        self.assertAlmostEqual(v5.get_radians(), 5.0341395, 5)
        return

    def test_add_vectors(self):

        v1 = CardEngine.Hitbox.Vector2D(2, 3)
        v2 = CardEngine.Hitbox.Vector2D(-4, -3)
        v3 = CardEngine.Hitbox.Vector2D(3, -2)

        # Add vector 2 to vector 1
        v1 += v2

        # Verify adding vector 2 to vector 1 updates vector 1 appropriately, and does not affect vector 2
        self.assertAlmostEqual(v1.x, -2, 5)
        self.assertAlmostEqual(v1.y, 0, 5)
        self.assertAlmostEqual(v2.x, -4, 5)
        self.assertAlmostEqual(v2.y, -3, 5)

        # Add vector 3 to vector 1
        v1 += v3

        # Verify adding vector 3 to vector 1 updates vector 1 appropriately, and does not affect vector 3
        self.assertAlmostEqual(v1.x, 1, 5)
        self.assertAlmostEqual(v1.y, -2, 5)
        self.assertAlmostEqual(v3.x, 3, 5)
        self.assertAlmostEqual(v3.y, -2, 5)

        # Add vector 2 to vector 3
        v3 += v2

        # Verify adding vector 2 to vector 3 updates vector 3 appropriately, and does not affect vector 2
        self.assertAlmostEqual(v2.x, -4, 5)
        self.assertAlmostEqual(v2.y, -3, 5)
        self.assertAlmostEqual(v3.x, -1, 5)
        self.assertAlmostEqual(v3.y, -5, 5)

        # Add vector 3 to vector 2
        v2 += v3

        # Verify adding vector 3 to vector 2 updates vector 2 appropriately, and does not affect vector 3
        self.assertAlmostEqual(v2.x, -5, 5)
        self.assertAlmostEqual(v2.y, -8, 5)
        self.assertAlmostEqual(v3.x, -1, 5)
        self.assertAlmostEqual(v3.y, -5, 5)

    def test_subtract_vectors(self):
        v1 = CardEngine.Hitbox.Vector2D(2, 3)
        v2 = CardEngine.Hitbox.Vector2D(-4, -3)
        v3 = CardEngine.Hitbox.Vector2D(3, -2)

        # Subtract vector 2 from vector 1
        v1 -= v2

        # Verify adding vector 2 to vector 1 updates vector 1 appropriately, and does not affect vector 2
        self.assertAlmostEqual(v1.x, 6, 5)
        self.assertAlmostEqual(v1.y, 6, 5)
        self.assertAlmostEqual(v2.x, -4, 5)
        self.assertAlmostEqual(v2.y, -3, 5)

        # Subtract vector 3 from vector 1
        v1 -= v3

        # Verify adding vector 3 to vector 1 updates vector 1 appropriately, and does not affect vector 3
        self.assertAlmostEqual(v1.x, 3, 5)
        self.assertAlmostEqual(v1.y, 8, 5)
        self.assertAlmostEqual(v3.x, 3, 5)
        self.assertAlmostEqual(v3.y, -2, 5)

        # Add vector 2 to vector 3
        v3 -= v2

        # Verify adding vector 2 to vector 3 updates vector 3 appropriately, and does not affect vector 2
        self.assertAlmostEqual(v2.x, -4, 5)
        self.assertAlmostEqual(v2.y, -3, 5)
        self.assertAlmostEqual(v3.x, 7, 5)
        self.assertAlmostEqual(v3.y, 1, 5)

        # Add vector 3 to vector 2
        v2 -= v3

        # Verify adding vector 3 to vector 2 updates vector 2 appropriately, and does not affect vector 3
        self.assertAlmostEqual(v2.x, -11, 5)
        self.assertAlmostEqual(v2.y, -4, 5)
        self.assertAlmostEqual(v3.x, 7, 5)
        self.assertAlmostEqual(v3.y, 1, 5)

    def test_multiply_vectors(self):
        return

    def test_scale(self):
        return

    def test_dot(self):
        return

    def test_angles_between_vectors(self):
        return


# Tests to verify the Triangle class.
class TriangleTests(unittest.TestCase):
    def test_Triangle(self):
        # Initialize triangle to test initial setup
        triangle = CardEngine.Hitbox.Triangle(CardEngine.Hitbox.Point2D(0, 0),
                                              CardEngine.Hitbox.Point2D(3, 0),
                                              CardEngine.Hitbox.Point2D(0, 4))

        # Syntactic sugar
        point_a = triangle._points[0]
        point_b = triangle._points[1]
        point_c = triangle._points[2]

        # Ensure points were setup correctly
        self.addTypeEqualityFunc(type(point_a), point_a.__eq__)
        self.assertEqual(point_a, (0, 0))
        self.assertEqual(point_b, (3, 0))
        self.assertEqual(point_c, (0, 4))
        self.assertNotEqual(point_a, point_b)
        self.assertNotEqual(point_b, point_c)
        self.assertNotEqual(point_a, point_c)

    def test_CollidePoint(self):
        # Initialize triangle to test collide point works with both points and tupples
        triangle = CardEngine.Hitbox.Triangle(CardEngine.Hitbox.Point2D(0, 0),
                                              CardEngine.Hitbox.Point2D(4, 0),
                                              CardEngine.Hitbox.Point2D(0, 4))

        # Initialize points for test
        point_inside_triangle_1 = CardEngine.Hitbox.Point2D(1.8, 1.8)
        point_inside_triangle_2 = CardEngine.Hitbox.Point2D(0.1, 3.8)
        point_inside_triangle_3 = CardEngine.Hitbox.Point2D(3.8, 0.1)
        point_outside_triangle_1 = CardEngine.Hitbox.Point2D(-0.5, 2)
        point_outside_triangle_2 = CardEngine.Hitbox.Point2D(2, -0.5)
        point_outside_triangle_3 = CardEngine.Hitbox.Point2D(2.1, 2.1)

        # Verify that a given point is inside the triangle
        self.assertTrue(triangle.collidepoint(point_inside_triangle_1))
        self.assertTrue(triangle.collidepoint(point_inside_triangle_2))
        self.assertTrue(triangle.collidepoint(point_inside_triangle_3))

        # Verify that a given point is outside the triangle
        self.assertFalse(triangle.collidepoint(point_outside_triangle_1))
        self.assertFalse(triangle.collidepoint(point_outside_triangle_2))
        self.assertFalse(triangle.collidepoint(point_outside_triangle_3))

        # Verify tuples can work as well
        self.assertTrue(triangle.collidepoint(1.8, 1.8))
        self.assertFalse(triangle.collidepoint(2.1, 2.1))
        self.assertFalse(triangle.collidepoint(-0.5, 2))
        self.assertFalse(triangle.collidepoint(2, -0.5))

    def test_CollideTriangle(self):
        # Initialize triangles
        triangle_1 = CardEngine.Hitbox.Triangle(CardEngine.Hitbox.Point2D(1, 1),
                                                CardEngine.Hitbox.Point2D(4, 0),
                                                CardEngine.Hitbox.Point2D(0, 4))
        # Triangle 2 encompasses Triangle 1
        triangle_2 = CardEngine.Hitbox.Triangle(CardEngine.Hitbox.Point2D(-1, -1),
                                                CardEngine.Hitbox.Point2D(5, 0),
                                                CardEngine.Hitbox.Point2D(0, 5))

        # Triangle 3 partially within Triangle 2, but does not collide with Triangle 1
        triangle_3 = CardEngine.Hitbox.Triangle(CardEngine.Hitbox.Point2D(-1, -2),
                                                CardEngine.Hitbox.Point2D(0, 0),
                                                CardEngine.Hitbox.Point2D(0, -3))

        # Verify Triangle 1 and 2 intersect
        self.assertTrue(triangle_1.collidetriangle(triangle_2))
        self.assertTrue(triangle_2.collidetriangle(triangle_1))

        # Verify Triangle 1 and 3 do not intersect
        self.assertFalse(triangle_1.collidetriangle(triangle_3))
        self.assertFalse(triangle_3.collidetriangle(triangle_1))

        # Verify Triangle 2 and 3 intersect
        self.assertTrue(triangle_2.collidetriangle(triangle_3))
        self.assertTrue(triangle_3.collidetriangle(triangle_2))
        return

    def test_Properties(self):
        pointa = CardEngine.Hitbox.Point2D(4, 5)
        pointb = CardEngine.Hitbox.Point2D(4, 0)
        pointc = CardEngine.Hitbox.Point2D(0, 0)

        triangle = CardEngine.Hitbox.Triangle(pointa, pointb, pointc)

        return


class HitboxTests(unittest.TestCase):

    def test_Hitbox(self):
        return

    def test_Magnitude(self):
        return

    def test_angle(self):
        return

    def test_multiply(self):
        return

    def test_divide(self):
        return

    def test_add(self):
        return

    def test_subtract(self):
        return


class SquareHitbox(unittest.TestCase):

    def test_SquareHitbox(self):
        return

if __name__ == '__main__':
    unittest.main()
