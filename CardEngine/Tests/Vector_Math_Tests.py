import unittest
import CardEngine.VectorMath
__author__ = 'Evan'


# Tests to verify the Point class
class PointTests(unittest.TestCase):
    def test_point(self):
        # Create point at (4, 5)
        p = CardEngine.VectorMath.Point2D(4, 5)

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
        p = CardEngine.VectorMath.Point2D(2, 3)
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
        p = CardEngine.VectorMath.Point2D(3, 3)

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

        p1 = CardEngine.VectorMath.Point2D(3, 3)
        p2 = CardEngine.VectorMath.Point2D(5, 5)

        # Rotate point 1 about (0, 0) 90 degrees to (-y, x) = (-3, 3) and verify
        p1.rotate_clockwise(0, 0, 1.570796327)
        self.assertAlmostEqual(p1.x, -3, 7)
        self.assertAlmostEqual(p1.y, 3, 7)

        # Rotate point 1 about (0, 0) 90 degrees to (-y, x) = (-3, -3) and verify
        p1.rotate_clockwise(0, 0, 1.570796327)
        self.assertAlmostEqual(p1.x, -3, 7)
        self.assertAlmostEqual(p1.y, -3, 7)

        # Rotate point 1 about (0, 0) 90 degrees to (-y, x) = (3, -3) and verify
        p1.rotate_clockwise(0, 0, 1.570796327)
        self.assertAlmostEqual(p1.x, 3, 7)
        self.assertAlmostEqual(p1.y, -3, 7)

        # Rotate point 1 about (0, 0) 90 degrees to (-y, x) = (3, 3) and verify
        p1.rotate_clockwise(0, 0, 1.570796327)
        self.assertAlmostEqual(p1.x, 3, 7)
        self.assertAlmostEqual(p1.y, 3, 7)

        # Rotate point 2 about (2, 2) 90 degrees to (-y + 4, x) = (-1, 5)
        p2.rotate_clockwise(2, 2, 1.570796327)
        self.assertAlmostEqual(p2.x, -1, 7)
        self.assertAlmostEqual(p2.y, 5, 7)

        # Rotate point 2 about (2, 2) 90 degrees to (-y + 4, x) = (-1, -1)
        p2.rotate_clockwise(2, 2, 1.570796327)
        self.assertAlmostEqual(p2.x, -1, 7)
        self.assertAlmostEqual(p2.y, -1, 7)

        # Rotate point 2 about (2, 2) 90 degrees to (-y + 4, x) = (5, -1)
        p2.rotate_clockwise(2, 2, 1.570796327)
        self.assertAlmostEqual(p2.x, 5, 7)
        self.assertAlmostEqual(p2.y, -1, 7)

        # Rotate point 2 about (2, 2) 90 degrees to (-y + 4, x) = (5, 5)
        p2.rotate_clockwise(2, 2, 1.570796327)
        self.assertAlmostEqual(p2.x, 5, 7)
        self.assertAlmostEqual(p2.y, 5, 7)

    def test_rotate_counterclockwise(self):

        p1 = CardEngine.VectorMath.Point2D(3, 3)
        p2 = CardEngine.VectorMath.Point2D(5, 5)

        # Rotate point about (0, 0) 90 degrees to (-y, x) = (3, -3) and verify
        p1.rotate_counterclockwise(0, 0, 1.5707963268)
        self.assertAlmostEqual(p1.x, 3, 5)
        self.assertAlmostEqual(p1.y, -3, 5)

        # Rotate point about (0, 0) 90 degrees to (-y, x) = (-3, -3) and verify
        p1.rotate_counterclockwise(0, 0, 1.5707963268)
        self.assertAlmostEqual(p1.x, -3, 5)
        self.assertAlmostEqual(p1.y, -3, 5)

        # Rotate point about (0, 0) 90 degrees to (-y, x) = (-3, 3) and verify
        p1.rotate_counterclockwise(0, 0, 1.5707963268)
        self.assertAlmostEqual(p1.x, -3, 5)
        self.assertAlmostEqual(p1.y, 3, 5)

        # Rotate point about (0, 0) 90 degrees to (-y, x) = (3, 3) and verify
        p1.rotate_counterclockwise(0, 0, 1.5707963268)
        self.assertAlmostEqual(p1.x, 3, 5)
        self.assertAlmostEqual(p1.y, 3, 5)

        # Rotate point 2 about (2, 2) 90 degrees to (-y + 4, x) = (5, -1)
        p2.rotate_counterclockwise(2, 2, 1.570796327)
        self.assertAlmostEqual(p2.x, 5, 7)
        self.assertAlmostEqual(p2.y, -1, 7)

        # Rotate point 2 about (2, 2) 90 degrees to (-y + 4, x) = (-1, -1)
        p2.rotate_counterclockwise(2, 2, 1.570796327)
        self.assertAlmostEqual(p2.x, -1, 7)
        self.assertAlmostEqual(p2.y, -1, 7)

        # Rotate point 2 about (2, 2) 90 degrees to (-y + 4, x) = (-1, 5)
        p2.rotate_counterclockwise(2, 2, 1.570796327)
        self.assertAlmostEqual(p2.x, -1, 7)
        self.assertAlmostEqual(p2.y, 5, 7)

        # Rotate point 2 about (2, 2) 90 degrees to (-y + 4, x) = (5, 5)
        p2.rotate_counterclockwise(2, 2, 1.570796327)
        self.assertAlmostEqual(p2.x, 5, 7)
        self.assertAlmostEqual(p2.y, 5, 7)

    def test_scale(self):

        p1 = CardEngine.VectorMath.Point2D(3, 3)
        p2 = CardEngine.VectorMath.Point2D(4, 5)

        # Scale point 1 to twice as big as before, about point (0, 0)
        p1.scale(0, 0, 2)
        self.assertAlmostEqual(p1.x, 6, 5)
        self.assertAlmostEqual(p1.y, 6, 5)

        # Scale point 1 to half as big as before, about point (0, 0)
        p1.scale(0, 0, .5)
        self.assertAlmostEqual(p1.x, 3, 5)
        self.assertAlmostEqual(p1.y, 3, 5)

        # Scale point 2 about point (1, 2) by a factor of 3
        p2.scale(1, 2, 3)
        self.assertAlmostEqual(p2.x, 10, 5)
        self.assertAlmostEqual(p2.y, 11, 5)

        # Scale point 2 about point (1, 2) by a factor of 3
        p2.scale(1, 2, 0.5)
        self.assertAlmostEqual(p2.x, 5.5, 5)
        self.assertAlmostEqual(p2.y, 6.5, 5)

    def test_reflect(self):
        # Create point at (3, 3)
        p = CardEngine.VectorMath.Point2D(3, 3)
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

    # Tests __init__()
    def test_Vector(self):
        v1 = CardEngine.VectorMath.Vector2D(2, 4)

        self.assertAlmostEqual(v1.x, 2, 5)
        self.assertAlmostEqual(v1.y, 4, 5)

        return

    def test_copy(self):
        v1 = CardEngine.VectorMath.Vector2D(-2, 4)
        v2 = v1.copy()

        # Verify copy equals the original
        self.assertEqual(v1.x, v2.x)
        self.assertEqual(v1.y, v2.y)

        # Change second vector
        v2.x = 5
        v2.y = 6

        # Verify copy does not equal the original
        self.assertNotEqual(v1.x, v2.x)
        self.assertNotEqual(v1.y, v2.y)

    # Tests Vector2D.magnitude() and Vector2D.length()
    def test_magnitude(self):
        v1 = CardEngine.VectorMath.Vector2D(3, 4)
        v2 = CardEngine.VectorMath.Vector2D(2, 2)
        v3 = CardEngine.VectorMath.Vector2D(-3, 2)
        v4 = CardEngine.VectorMath.Vector2D(-4, -5)
        v5 = CardEngine.VectorMath.Vector2D(2, -4)

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

    # Tests Vector2D.normalize()
    def test_normalize(self):
        v1 = CardEngine.VectorMath.Vector2D(2, 2)
        v2 = v1.normalize()

        self.assertAlmostEqual(v1.x, 2, 7)
        self.assertAlmostEqual(v1.y, 2, 7)

        self.assertAlmostEqual(v2.x, .7071068, 5)
        self.assertAlmostEqual(v2.y, .7071068, 5)

    # Tests Vector2D.scale()
    def test_scale(self):
        v1 = CardEngine.VectorMath.Vector2D(1, 4)
        v2 = CardEngine.VectorMath.Vector2D(-2, -3)
        v3 = CardEngine.VectorMath.Vector2D(-1, 2)

        # Scale v1 by 2
        v1.scale(2)
        v2.scale(3)
        v3.scale(0.5)

        # Verify v1 equals (2, 5)
        self.assertEqual(v1.x, 2)
        self.assertEqual(v1.y, 8)

        # Verify v2 equals (-2, -11)
        self.assertEqual(v2.x, -6)
        self.assertEqual(v2.y, -9)

        # Verify v3 equals (-0.5, 1)
        self.assertAlmostEqual(v3.x, -0.5, 5)
        self.assertAlmostEqual(v3.y, 1, 5)

    # Tests Vector2D.dot()
    def test_dot_using_vectors(self):
        v1 = CardEngine.VectorMath.Vector2D(3, 4)
        v2 = CardEngine.VectorMath.Vector2D(-2, -1)
        v3 = CardEngine.VectorMath.Vector2D(-3, 1)
        v4 = CardEngine.VectorMath.Vector2D(1, -4)

        self.assertEqual(v1.dot(v1), 25)
        self.assertEqual(v1.dot(v2), -10)
        self.assertEqual(v1.dot(v3), -5)
        self.assertEqual(v1.dot(v4), -13)

        self.assertEqual(v2.dot(v1), -10)
        self.assertEqual(v2.dot(v2), 5)
        self.assertEqual(v2.dot(v3), 5)
        self.assertEqual(v2.dot(v4), 2)

        self.assertEqual(v3.dot(v1), -5)
        self.assertEqual(v3.dot(v2), 5)
        self.assertEqual(v3.dot(v3), 10)
        self.assertEqual(v3.dot(v4), -7)

        self.assertEqual(v4.dot(v1), -13)
        self.assertEqual(v4.dot(v2), 2)
        self.assertEqual(v4.dot(v3), -7)
        self.assertEqual(v4.dot(v4), 17)

    # Tests Vector2D.dot()
    def test_dot_using_tuples(self):
        v1 = CardEngine.VectorMath.Vector2D(3, 4)
        v2 = CardEngine.VectorMath.Vector2D(-2, -1)

        self.assertEqual(v1.dot((2, -2)), -2)
        self.assertEqual(v2.dot((-3, 4)), 2)

    # Tests Vector2D.get_angle_between_vectors()
    def test_angles_between_vectors(self):
        v1 = CardEngine.VectorMath.Vector2D(0, 4)
        v2 = CardEngine.VectorMath.Vector2D(4, 0)

        # Verify angle is 90 degrees (pi/2 radians) between two vectors
        self.assertAlmostEqual(v1.get_angle_between_vectors(v2), 1.5707963, 5)
        self.assertAlmostEqual(v2.get_angle_between_vectors(v1), 1.5707963, 5)

        # Verify angle is 0 degrees between same vector and itself
        self.assertAlmostEqual(v1.get_angle_between_vectors(v1), 0, 5)
        self.assertAlmostEqual(v2.get_angle_between_vectors(v2), 0, 5)

        return

    # Tests Vector2D.degrees() and Vector2D.radians()
    def test_angles(self):
        v1 = CardEngine.VectorMath.Vector2D(2, 2)
        v2 = CardEngine.VectorMath.Vector2D(1, 5)
        v3 = CardEngine.VectorMath.Vector2D(-3, -2)
        v4 = CardEngine.VectorMath.Vector2D(-4, 0)
        v5 = CardEngine.VectorMath.Vector2D(3, -9)

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

    # Tests Vector2D.__iadd__() (+=)
    def test_add_vectors_using_vectors(self):

        v1 = CardEngine.VectorMath.Vector2D(2, 3)
        v2 = CardEngine.VectorMath.Vector2D(-4, -3)
        v3 = CardEngine.VectorMath.Vector2D(3, -2)

        # Add vectors together
        v1 += v2
        v2 += v3

        # Verify Vector 1 is (2 + -4, 3 + -3) = (-2, 0)
        self.assertAlmostEqual(v1.x, -2, 5)
        self.assertAlmostEqual(v1.y, 0, 5)

        # Verify Vector 2 is (-4 + 3, -3 + -2) = (-1, -5)
        self.assertAlmostEqual(v2.x, -1, 5)
        self.assertAlmostEqual(v2.y, -5, 5)

        # Verify Vector 3 is (3, -2)
        self.assertAlmostEqual(v3.x, 3, 5)
        self.assertAlmostEqual(v3.y, -2, 5)

    # Tests Vector2D.__iadd__() (+=)
    def test_add_vectors_using_tuples(self):

        v1 = CardEngine.VectorMath.Vector2D(4, 5)
        v2 = CardEngine.VectorMath.Vector2D(3, 3)

        # Add tuples to vectors
        v1 += (-2, -1)
        v2 += (-2.5, 4.1)

        # Verify v1 is (4 + -2, 5 + -1) = (2, 4)
        self.assertAlmostEqual(v1.x, 2, 5)
        self.assertAlmostEqual(v1.y, 4, 5)

        # Verify v2 is (3 + -2.5, 3 + 4.1) = (0.5, 7.1)
        self.assertAlmostEqual(v2.x, 0.5, 5)
        self.assertAlmostEqual(v2.y, 7.1, 5)

    # Tests Vector2D.__isub__() (-=)
    def test_subtract_vectors_using_vectors(self):
        v1 = CardEngine.VectorMath.Vector2D(2, 3)
        v2 = CardEngine.VectorMath.Vector2D(-4, -3)
        v3 = CardEngine.VectorMath.Vector2D(3, -2)

        # Subtract vectors together
        v1 -= v2
        v2 -= v3

        # Verify Vector 1 is (2 - -4, 3 - -3) = (6, 6)
        self.assertAlmostEqual(v1.x, 6, 5)
        self.assertAlmostEqual(v1.y, 6, 5)

        # Verify Vector 2 is (-4 - 3, -3 - -2) = (-7, -1)
        self.assertAlmostEqual(v2.x, -7, 5)
        self.assertAlmostEqual(v2.y, -1, 5)

        # Verify Vector 3 is (3, -2)
        self.assertAlmostEqual(v3.x, 3, 5)
        self.assertAlmostEqual(v3.y, -2, 5)

    # Tests Vector2D.__isub__() (-=)
    def test_subtract_vectors_using_tuples(self):
        v1 = CardEngine.VectorMath.Vector2D(1, 3)
        v2 = CardEngine.VectorMath.Vector2D(-4, -2)

        # Subtract tuples from vectors
        v1 -= (-1, -2)
        v2 -= (-5, -6)

        # Verify Vector 1 is (1 - -1, 3 - -2) = (2, 5)
        self.assertAlmostEqual(v1.x, 2, 5)
        self.assertAlmostEqual(v1.y, 5, 5)

        # Verify Vector 2 is (-4 - -5, -2 - -6) = (1, 4)
        self.assertAlmostEqual(v2.x, 1, 5)
        self.assertAlmostEqual(v2.y, 4, 5)

    # Tests Vector2D.__imul__() (*=)
    def test_multiply_scalar(self):
        v1 = CardEngine.VectorMath.Vector2D(4, 3)
        v2 = CardEngine.VectorMath.Vector2D(-1, 5)

        v1 *= 3
        v2 *= .75

        # Verify v1 is (4 * 3, 3 * 3) = (12, 9)
        self.assertEqual(v1.x, 12)
        self.assertEqual(v1.y, 9)

        # Verify v2 is (-1 * .75, 5 * .75) = (-.75, 3.75)
        self.assertAlmostEqual(v2.x, -.75, 5)
        self.assertAlmostEqual(v2.y, 3.75, 5)

    # Tests Vector2D.__idiv__() (/=)
    def test_divide_scalar(self):
        v1 = CardEngine.VectorMath.Vector2D(-8, -6)
        v2 = CardEngine.VectorMath.Vector2D(4, -3)

        v1 /= 2
        v2 /= .6666666667

        # Verify v1 is (-8 / 2, -6 / 2) = (-4, -3)
        self.assertAlmostEqual(v1.x, -4, 5)
        self.assertAlmostEqual(v1.y, -3, 5)

        # Verify v2 is (4 / (2/3), -3 / (2/3)) = (6, -4.5)
        self.assertAlmostEqual(v2.x, 6, 5)
        self.assertAlmostEqual(v2.y, -4.5, 5)

    # Tests Vector2D.__mul__() (*)
    def test_multiply_vectors(self):
        v1 = CardEngine.VectorMath.Vector2D(-2, 2)
        v2 = CardEngine.VectorMath.Vector2D(4, 3)
        v3 = CardEngine.VectorMath.Vector2D(9, -5)
        v4 = CardEngine.VectorMath.Vector2D(-2, -3)

        self.assertEqual(v1 * v1, 8)
        self.assertEqual(v1 * v2, -2)
        self.assertEqual(v1 * v3, -28)
        self.assertEqual(v1 * v4, -2)

        self.assertEqual(v2 * v1, -2)
        self.assertEqual(v2 * v2, 25)
        self.assertEqual(v2 * v3, 21)
        self.assertEqual(v2 * v4, -17)

        self.assertEqual(v3 * v1, -28)
        self.assertEqual(v3 * v2, 21)
        self.assertEqual(v3 * v3, 106)
        self.assertEqual(v3 * v4, -3)

        self.assertEqual(v4 * v1, -2)
        self.assertEqual(v4 * v2, -17)
        self.assertEqual(v4 * v3, -3)
        self.assertEqual(v4 * v4, 13)


# Tests to verify the Triangle class.
class TriangleTests(unittest.TestCase):
    def test_Triangle(self):
        # Initialize triangle to test initial setup
        triangle = CardEngine.VectorMath.Triangle2D(CardEngine.VectorMath.Point2D(0, 0),
                                              CardEngine.VectorMath.Point2D(3, 0),
                                              CardEngine.VectorMath.Point2D(0, 4))

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
        triangle = CardEngine.VectorMath.Triangle2D(CardEngine.VectorMath.Point2D(0, 0),
                                              CardEngine.VectorMath.Point2D(4, 0),
                                              CardEngine.VectorMath.Point2D(0, 4))

        # Initialize points for test
        point_inside_triangle_1 = CardEngine.VectorMath.Point2D(1.8, 1.8)
        point_inside_triangle_2 = CardEngine.VectorMath.Point2D(0.1, 3.8)
        point_inside_triangle_3 = CardEngine.VectorMath.Point2D(3.8, 0.1)
        point_outside_triangle_1 = CardEngine.VectorMath.Point2D(-0.5, 2)
        point_outside_triangle_2 = CardEngine.VectorMath.Point2D(2, -0.5)
        point_outside_triangle_3 = CardEngine.VectorMath.Point2D(2.1, 2.1)

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
        triangle_1 = CardEngine.VectorMath.Triangle2D(CardEngine.VectorMath.Point2D(1, 1),
                                                CardEngine.VectorMath.Point2D(4, 0),
                                                CardEngine.VectorMath.Point2D(0, 4))
        # Triangle 2 encompasses Triangle 1
        triangle_2 = CardEngine.VectorMath.Triangle2D(CardEngine.VectorMath.Point2D(-1, -1),
                                                CardEngine.VectorMath.Point2D(5, 0),
                                                CardEngine.VectorMath.Point2D(0, 5))

        # Triangle 3 partially within Triangle 2, but does not collide with Triangle 1
        triangle_3 = CardEngine.VectorMath.Triangle2D(CardEngine.VectorMath.Point2D(-1, -2),
                                                CardEngine.VectorMath.Point2D(0, 0),
                                                CardEngine.VectorMath.Point2D(0, -3))

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
        pointa = CardEngine.VectorMath.Point2D(4, 5)
        pointb = CardEngine.VectorMath.Point2D(4, 0)
        pointc = CardEngine.VectorMath.Point2D(0, 0)

        triangle = CardEngine.VectorMath.Triangle2D(pointa, pointb, pointc)

        return
