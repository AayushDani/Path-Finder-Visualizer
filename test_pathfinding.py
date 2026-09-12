import itertools
import unittest

from pathfinding import shortest_path


class PathTests(unittest.TestCase):
    def test_open_grid_distance_and_endpoints(self):
        result = shortest_path(5, 4, (0, 0), (4, 3))
        self.assertEqual(len(result.path) - 1, 7)
        self.assertEqual(result.path[0], (0, 0))
        self.assertEqual(result.path[-1], (4, 3))

    def test_detour(self):
        walls = {(1, 0), (1, 1)}
        result = shortest_path(3, 3, (0, 0), (2, 0), walls)
        self.assertEqual(len(result.path) - 1, 6)
        self.assertFalse(set(result.path) & walls)
        self.assertEqual(walls, {(1, 0), (1, 1)})

    def test_unreachable_terminates_without_revisits(self):
        result = shortest_path(4, 4, (0, 0), (3, 3), {(2, y) for y in range(4)})
        self.assertIsNone(result.path)
        self.assertEqual(len(result.visited), 8)
        self.assertEqual(len(set(result.visited)), len(result.visited))

    def test_same_start_end(self):
        result = shortest_path(1, 1, (0, 0), (0, 0))
        self.assertEqual(result.path, ((0, 0),))

    def test_invalid_inputs(self):
        cases = [(0, 2, (0, 0), (1, 1), ()),
                 (True, 2, (0, 0), (0, 1), ()),
                 (2, 2, (-1, 0), (1, 1), ()),
                 (2, 2, (0, 0), (2, 1), ()),
                 (2, 2, (0.0, 0), (1, 1), ()),
                 (2, 2, (0, 0), (1, 1), {(0, 0)}),
                 (2, 2, (0, 0), (1, 1), {(1, 1)}),
                 (2, 2, (0, 0), (1, 1), {(3, 3)}),
                 (2, 2, (0,), (1, 1), ())]
        for args in cases:
            with self.subTest(args=args), self.assertRaises(ValueError):
                shortest_path(*args)

    def test_every_three_by_three_maze_against_distance_relaxation(self):
        # An independent distance-relaxation oracle checks all 128 wall layouts.
        points = list(itertools.product(range(3), repeat=2))
        interior = [p for p in points if p not in ((0, 0), (2, 2))]
        for mask in range(1 << len(interior)):
            walls = {p for i, p in enumerate(interior) if mask & (1 << i)}
            distance = {p: float("inf") for p in points if p not in walls}
            distance[(0, 0)] = 0
            for _ in points:
                for a in distance:
                    for b in distance:
                        if abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1:
                            distance[b] = min(distance[b], distance[a] + 1)
            result = shortest_path(3, 3, (0, 0), (2, 2), walls)
            with self.subTest(mask=mask):
                if distance[(2, 2)] == float("inf"):
                    self.assertIsNone(result.path)
                else:
                    self.assertEqual(len(result.path) - 1, distance[(2, 2)])
                    for a, b in zip(result.path, result.path[1:]):
                        self.assertEqual(abs(a[0] - b[0]) + abs(a[1] - b[1]), 1)


if __name__ == "__main__":
    unittest.main()
