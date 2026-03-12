import tkinter as tk
import maze_file_reader as reader

maze = reader.load_maze("default", "maze_0.txt")

cell_size = 40

colors = {
    0: "grey",    # empty
    1: "green",   # start
    2: "red",     # goal
    3: "black",   # wall
    4: "yellow"   # bonus
}

# 0 = empty square
# 1 = start (only one)
# 2 = goal  (only one)
# 3 = wall  (auto built a border around the grid)
# 4 = bonus item

root = tk.Tk()
root.title("Maze Viewer")

canvas = tk.Canvas(root,
                   width=len(maze[0]) * cell_size,
                   height=len(maze) * cell_size)
canvas.pack()

for y, row in enumerate(maze):
    for x, cell in enumerate(row):
        color = colors[cell]

        canvas.create_rectangle(
            x * cell_size,
            y * cell_size,
            (x + 1) * cell_size,
            (y + 1) * cell_size,
            fill=color,
            outline="gray20"
        )

root.mainloop()