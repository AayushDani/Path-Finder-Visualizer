"""Interactive maze editor. Run with: python3 'Visual Maze.py'."""

import tkinter as tk
from tkinter import ttk

from pathfinding import shortest_path

SIZE, CELL = 12, 40
COLORS = {"empty": "#ffffff", "wall": "#334155", "visited": "#dbeafe",
          "path": "#fbbf24", "start": "#16a34a", "end": "#dc2626"}


class MazeApp:
    def __init__(self, root):
        self.root = root
        root.title("Path Finder | Breadth-first search")
        root.resizable(False, False)
        self.start, self.end = (0, 0), (SIZE - 1, SIZE - 1)
        self.walls, self.visited, self.path = set(), set(), set()
        self.pending = None
        self.mode = tk.StringVar(value="wall")
        self.status = tk.StringVar(value="Click cells to draw walls, then find a path.")

        frame = ttk.Frame(root, padding=20)
        frame.pack()
        ttk.Label(frame, text="Path Finder", font=("Helvetica", 22, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Explore shortest paths on an unweighted grid.").pack(anchor="w", pady=(4, 14))
        modes = ttk.Frame(frame)
        modes.pack(anchor="w", pady=(0, 12))
        for label, value in (("Wall", "wall"), ("Start", "start"), ("End", "end")):
            ttk.Radiobutton(modes, text=label, variable=self.mode, value=value).pack(side="left", padx=(0, 16))
        self.canvas = tk.Canvas(frame, width=SIZE * CELL, height=SIZE * CELL,
                                highlightthickness=1, highlightbackground="#cbd5e1")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.edit)
        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=12)
        ttk.Button(buttons, text="Find path", command=self.search).pack(side="left")
        ttk.Button(buttons, text="Clear walls", command=self.clear).pack(side="left", padx=8)
        ttk.Label(frame, textvariable=self.status, wraplength=SIZE * CELL).pack(anchor="w")
        ttk.Label(frame, text="Green: start   Red: end   Blue: explored   Gold: path").pack(anchor="w", pady=(8, 0))
        self.draw()

    def reset_search(self):
        if self.pending is not None:
            self.root.after_cancel(self.pending)
            self.pending = None
        self.visited.clear()
        self.path.clear()

    def edit(self, event):
        point = event.x // CELL, event.y // CELL
        if not all(0 <= n < SIZE for n in point):
            return
        self.reset_search()
        mode = self.mode.get()
        if mode == "wall" and point not in (self.start, self.end):
            if point in self.walls:
                self.walls.remove(point)
            else:
                self.walls.add(point)
        elif mode == "start":
            self.start = point
            self.walls.discard(point)
        elif mode == "end":
            self.end = point
            self.walls.discard(point)
        self.status.set("Maze updated. Select Find path to explore it.")
        self.draw()

    def clear(self):
        self.reset_search()
        self.walls.clear()
        self.status.set("Walls cleared.")
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for y in range(SIZE):
            for x in range(SIZE):
                point = x, y
                kind = ("start" if point == self.start else "end" if point == self.end
                        else "wall" if point in self.walls else "path" if point in self.path
                        else "visited" if point in self.visited else "empty")
                self.canvas.create_rectangle(x * CELL, y * CELL, (x + 1) * CELL,
                                             (y + 1) * CELL, fill=COLORS[kind], outline="#cbd5e1")
                label = "S/E" if point == self.start == self.end else "S" if point == self.start else "E" if point == self.end else ""
                if label:
                    self.canvas.create_text((x + .5) * CELL, (y + .5) * CELL,
                                            text=label, fill="white", font=("Helvetica", 12, "bold"))

    def search(self):
        self.reset_search()
        result = shortest_path(SIZE, SIZE, self.start, self.end, self.walls)
        self.status.set("Exploring cells in breadth-first order...")
        steps = iter(result.visited)

        def animate():
            self.pending = None
            point = next(steps, None)
            if point is not None:
                self.visited.add(point)
                self.draw()
                self.pending = self.root.after(18, animate)
                return
            if result.path is None:
                self.status.set(f"No route. Explored {len(result.visited)} reachable cells.")
            else:
                self.path.update(result.path)
                self.status.set(f"Shortest route: {len(result.path) - 1} moves. Explored {len(result.visited)} cells.")
            self.draw()

        animate()


if __name__ == "__main__":
    root = tk.Tk()
    MazeApp(root)
    root.mainloop()
