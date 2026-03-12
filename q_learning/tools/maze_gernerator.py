import random

directory: str = "test"
filename: str = "test_4"

# odd numbers only -> works better
SIZE = 11


def generate_maze(size):
    # Start mit Wänden
    maze = [[3 for _ in range(size)] for _ in range(size)]
    visited = [[False for _ in range(size)] for _ in range(size)]

    # Hilfsfunktionen
    def neighbors(y, x):
        nbs = []
        for dy, dx in [(-2,0),(2,0),(0,-2),(0,2)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < size and 0 <= nx < size and not visited[ny][nx]:
                nbs.append((ny, nx))
        return nbs

    # Prim-artige Erzeugung
    start_y, start_x = random.randrange(1, size, 2), random.randrange(1, size, 2)
    maze[start_y][start_x] = 0
    visited[start_y][start_x] = True
    walls = []

    for ny, nx in neighbors(start_y, start_x):
        walls.append((start_y, start_x, ny, nx))

    while walls:
        idx = random.randrange(len(walls))
        y, x, ny, nx = walls.pop(idx)
        if not visited[ny][nx]:
            maze[(y+ny)//2][(x+nx)//2] = 0
            maze[ny][nx] = 0
            visited[ny][nx] = True
            for nny, nnx in neighbors(ny, nx):
                walls.append((ny, nx, nny, nnx))

    # Start und Ziel setzen
    maze[1][1] = 1
    maze[size-2][size-2] = 2

    return maze

def save_maze(filename, maze):
    with open(filename, "w") as f:
        for row in maze:
            line = "[" + ",".join(str(x) for x in row) + "],"
            f.write(line + "\n")



def main():
    maze = generate_maze(SIZE)
    save_maze(f"mazes/{directory}/{filename}.txt", maze)


if __name__ == "__main__":
    main()