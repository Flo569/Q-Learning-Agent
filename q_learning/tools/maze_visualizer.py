import tkinter as tk
import maze_file_reader as reader

maze = reader.load_maze("default", "maze_7")

cell_size = 40

colors = {
    0: "grey",    # empty
    1: "green",   # start
    2: "red",     # goal
    3: "black"    # wall
}

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