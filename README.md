# Path Finder Visualizer

An interactive maze for exploring **breadth-first search**. Place a start, an end, and walls, then watch the search visit cells and reveal a shortest route.

Originally a 2019–2020 Python/Tkinter/Pygame project. This refresh keeps the maze idea and replaces the search and interface with a small Tkinter application and an independently testable search module.

## Try it

Use **Python 3.10 or newer with Tkinter**. No third-party Python packages are required. Check Tkinter with `python3 -m tkinter`; if that fails, use a Python installation that includes Tk.

```bash
python3 "Visual Maze.py"
```

1. Select **Wall**, then click cells to add or remove obstacles.
2. Select **Start** or **End** and click a cell to move that marker.
3. Choose **Find path**. Blue cells show exploration; gold cells show the route.
4. Edit the maze or choose **Clear walls** to explore another layout.

The interface uses a 12×12 grid. The search module accepts any positive rectangular dimensions, with coordinates `(x, y)` measured from the top left. Moves are up, down, left, or right, with equal cost. This is an unweighted-grid visualizer, not a weighted routing engine.

## How it works

`pathfinding.py` uses a FIFO queue, records each cell once, and reconstructs the route through parent pointers. It returns a `SearchResult` with the route and exploration order. An unreachable target returns `path=None`; malformed coordinates and blocked endpoints raise `ValueError`.

```python
from pathfinding import shortest_path

result = shortest_path(5, 4, (0, 0), (4, 3), walls={(2, 0), (2, 1)})
print(result.path)
```

Search time and memory are O(width × height) in the worst case. Animation uses Tk callbacks so the interface can respond while exploration is displayed.

## Verify

```bash
python3 -m unittest discover -v
```

Tests cover detours, unreachable targets, coincident endpoints, invalid coordinates, and every wall configuration on a 3×3 grid, checked against an independent distance-relaxation implementation.

## Repository guide

- `pathfinding.py` — search and validation; usable without a display.
- `Visual Maze.py` — interactive editor and animation.
- `test_pathfinding.py` — algorithm tests.

The original image assets remain in the repository for historical context; the refreshed interface does not depend on them. Earlier implementations remain in git history.
