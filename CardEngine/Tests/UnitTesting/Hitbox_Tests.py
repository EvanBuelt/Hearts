import unittest
import CardEngine.Hitbox
from CardEngine.VectorMath import Point2D
from CardEngine.VectorMath import Triangle2D
__author__ = 'Evan'


class HitboxTests(unittest.TestCase):

    def test_Hitbox(self):
        blank_hitbox = CardEngine.Hitbox.Hitbox2D()
        hitbox_one_point = CardEngine.Hitbox.Hitbox2D([Point2D(1, 1)])
        hitbox_two_points = CardEngine.Hitbox.Hitbox2D([Point2D(2, 3),
                                                        Point2D(3, 6)])
        hitbox_three_points = CardEngine.Hitbox.Hitbox2D([Point2D(4, 10),
                                                          Point2D(5, 14),
                                                          Point2D(6, 19)])
        hitbox_four_points = CardEngine.Hitbox.Hitbox2D([Point2D(7, 25),
                                                         Point2D(8, 33),
                                                         Point2D(9, 42),
                                                         Point2D(10, 52)])

        # Verify blank hitbox defaults to (0, 0)
        self.assertEqual(blank_hitbox.x, 0)
        self.assertEqual(blank_hitbox.y, 0)
        self.assertEqual(blank_hitbox.hitbox_points, [])
        self.assertEqual(blank_hitbox.triangles, [])

        # Verify second hitbox uses a single point with no triangles
        self.assertEqual(hitbox_one_point.x, 1)
        self.assertEqual(hitbox_one_point.y, 1)
        self.assertEqual(hitbox_one_point.hitbox_points, [Point2D(1, 1)])
        self.assertEqual(hitbox_one_point.triangles, [])

        # Verify third hitbox uses two points with no triangles
        self.assertEqual(hitbox_two_points.x, 2)
        self.assertEqual(hitbox_two_points.y, 3)
        self.assertEqual(hitbox_two_points.hitbox_points, [Point2D(2, 3),
                                                          Point2D(3, 6)])
        self.assertEqual(hitbox_one_point.triangles, [])

        # Verify fourth hitbox uses two points with one triangles
        self.assertEqual(hitbox_three_points.x, 4)
        self.assertEqual(hitbox_three_points.y, 10)
        self.assertEqual(hitbox_three_points.hitbox_points, [Point2D(4, 10),
                                                             Point2D(5, 14),
                                                             Point2D(6, 19)])
        self.assertEqual(hitbox_three_points.triangles, [Triangle2D((4, 10), (5, 14), (6, 19))])

        # Verify fourth hitbox uses two points with one triangles
        self.assertEqual(hitbox_four_points.x, 7)
        self.assertEqual(hitbox_four_points.y, 25)
        self.assertEqual(hitbox_four_points.hitbox_points, [Point2D(7, 25),
                                                            Point2D(8, 33),
                                                            Point2D(9, 42),
                                                            Point2D(10, 52)])

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
