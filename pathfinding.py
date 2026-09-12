"""Breadth-first search on a rectangular, unweighted grid. No GUI dependencies."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class SearchResult:
    path: tuple[tuple[int, int], ...] | None
    visited: tuple[tuple[int, int], ...]


def shortest_path(width, height, start, end, walls=()):
    """Return a shortest path (including endpoints), or None when unreachable.

    Coordinates are (x, y), with (0, 0) at the top left. Movement is orthogonal
    and every move costs one. The input wall collection is never mutated.
    """
    if any(type(n) is not int or n <= 0 for n in (width, height)):
        raise ValueError("Grid dimensions must be positive integers.")

    def point(value):
        if not isinstance(value, (tuple, list)) or len(value) != 2:
            raise ValueError("Each coordinate must contain x and y.")
        x, y = value
        if type(x) is not int or type(y) is not int:
            raise ValueError("Coordinates must be integers.")
        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("Coordinates must be inside the grid.")
        return x, y

    start, end = point(start), point(end)
    blocked = {point(wall) for wall in walls}
    if start in blocked or end in blocked:
        raise ValueError("Start and end cannot be walls.")

    queue = deque([start])
    parents = {start: None}
    visited = []
    while queue:
        current = queue.popleft()
        visited.append(current)
        if current == end:
            path = []
            while current is not None:
                path.append(current)
                current = parents[current]
            return SearchResult(tuple(reversed(path)), tuple(visited))
        x, y = current
        for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            nx, ny = neighbor
            if (0 <= nx < width and 0 <= ny < height
                    and neighbor not in blocked and neighbor not in parents):
                parents[neighbor] = current
                queue.append(neighbor)
    return SearchResult(None, tuple(visited))
