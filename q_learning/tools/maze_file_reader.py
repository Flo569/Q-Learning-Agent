
# reads the content of a file and puts it into a list

def load_maze(directory: str, filename: str):
    maze = []

    filename = f"mazes/{directory}/{filename}"

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            # remove [ ]
            line = line.replace("[", "").replace("]", "")

            # split values
            row = [int(x) for x in line.split(",") if x.strip() != ""]

            maze.append(row)

    return maze