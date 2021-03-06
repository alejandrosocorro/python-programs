import time
from collections import deque


class Reader:
    def __init__(self, filename):
        self.filename = filename

    def transform_grid(self, grid):
        new_grid = []
        for row in grid:
            line = row.replace("0", " ")
            line = line.replace("1", "#")
            line = line.replace("2", ".")
            line = line.replace("3", "$")
            line = line.replace("4", "@")
            line = line.replace("5", "*")
            line = line.replace("6", "+")
            new_grid.append(line)
        return new_grid

    def read_sokobans(self):
        with open(self.filename, "r") as f:
            lines = f.readlines()

        all_grids = []
        for line in lines:
            if line.strip():
                line = line.split(",")[1].strip()
                height = int(line[0:2])
                width = int(line[2:4])
                line = line[4:]
                maze = [line[i : i + width] for i in range(0, len(line), width)]
                all_grids.append(self.transform_grid(maze))
        return all_grids


class Sokoban:
    def __init__(self, board):
        self.data = board
        self.nrows = max(len(r) for r in self.data)
        self.px = 0
        self.py = 0
        self.sdata = ""
        self.ddata = ""
        self.directions = (
            (0, -1, "u", "U"),
            (1, 0, "r", "R"),
            (0, 1, "d", "D"),
            (-1, 0, "l", "L"),
        )
        self.maps = {
            " ": " ",
            ".": ".",
            "@": " ",
            "#": "#",
            "$": " ",
            "*": ".",
            "+": ".",
        }
        self.mapd = {
            " ": " ",
            ".": " ",
            "@": "@",
            "#": " ",
            "$": "*",
            "*": "*",
            "+": "@",
        }

        for r, row in enumerate(self.data):
            for c, ch in enumerate(row):
                self.sdata += self.maps[ch]
                self.ddata += self.mapd[ch]
                if ch == "@":
                    self.px, self.py = c, r

    def solved_grid(self, m1, m2):
        """ Print to stdout solved Sokoban board"""
        m1 = [m1[i : i + self.nrows] for i in range(0, len(m1), self.nrows)]
        m2 = [m2[i : i + self.nrows] for i in range(0, len(m2), self.nrows)]

        rows = []
        for i in range(0, len(m2)):
            row = list(m2[i])
            for j in range(0, len(m1[i]) - 1):
                if m1[i][j] == "@":
                    row[j] = "@"
                elif m1[i][j] == "*":
                    row[j] = "*"
            rows.append("".join(row))
        return rows

    def push(self, x, y, dx, dy, data):
        """ Possible push-moves for box and update player """
        if (
            self.sdata[(y + 2 * dy) * self.nrows + x + 2 * dx] == "#"
            or data[(y + 2 * dy) * self.nrows + x + 2 * dx] != " "
        ):
            return None

        row = list(data)
        row[y * self.nrows + x] = " "
        row[(y + dy) * self.nrows + x + dx] = "@"
        row[(y + 2 * dy) * self.nrows + x + 2 * dx] = "*"
        return "".join(row)

    def is_solved(self, temp):
        """ Helper function to check if the Sokoban is solved """
        for i in range(len(temp)):
            if (self.sdata[i] == ".") != (temp[i] == "*"):
                return False
        return True

    def solve(self):
        """ Search solution """
        grid = None
        queue = deque([(self.ddata, "", self.px, self.py)])
        visited = set([self.ddata])
        while queue:
            current, csol, x, y = queue.popleft()

            for di in self.directions:
                temp = current
                dx, dy = di[0], di[1]
                if temp[(y + dy) * self.nrows + x + dx] == "*":
                    temp = self.push(x, y, dx, dy, temp)
                    if temp and temp not in visited:

                        if self.is_solved(temp):
                            grid = self.solved_grid(temp, self.sdata)
                            return grid, csol + di[3]

                        queue.append((temp, csol + di[3], x + dx, y + dy))
                        visited.add(temp)
                else:

                    if (
                        self.sdata[(y + dy) * self.nrows + x + dx] == "#"
                        or temp[(y + dy) * self.nrows + x + dx] != " "
                    ):
                        continue

                    row = list(temp)
                    row[y * self.nrows + x] = " "
                    row[(y + dy) * self.nrows + x + dx] = "@"
                    temp = "".join(row)

                    if temp not in visited:

                        if self.is_solved(temp):
                            grid = self.solved_grid(temp, self.sdata)
                            return grid, csol + di[2]

                        queue.append((temp, csol + di[2], x + dx, y + dy))
                        visited.add(temp)

        return grid, None


def solve_all(grids):
    """ Try to solve a sequence of sokoban grids """
    sokobans = [Sokoban(grid) for grid in grids]
    for i, sokoban in enumerate(sokobans):
        time, result = time_solve(sokoban)
        print(f"Solving Sokoban #{i}\n")
        if result:
            for row in result[0]:
                print(row)

            print()
            print(f"# of Steps: {len(result[1])}")
            print(f"Time: {time}\n\n")
        else:
            print(f"Couldn't solve Sokoban #{i}...")


def time_solve(sokoban):
    """ Time how long it takes to solve a Sokoban game """
    t0 = time.time()
    result = sokoban.solve()
    return (time.time() - t0, result)


if __name__ == "__main__":
    reader = Reader("levels.txt")
    all_grids = reader.read_sokobans()
    solve_all(all_grids)
