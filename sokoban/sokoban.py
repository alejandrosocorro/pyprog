"""
Empty = 0,
Wall = 1,
Whole = 2,
Box = 3,
Player = 4,
BoxOnWhole = 5,
PlayerOnWhole = 6
"""
import time
import collections
import ipdb
import textwrap


def find_locations(grid):
    box, hole, person = "*", ".", "@"
    boxes = []
    holes = []
    player = ()
    for i, row in enumerate(grid):
        for j, column in enumerate(row):
            if column == box:
                boxes.append((i, j))
            elif column == hole:
                holes.append((i, j))
            elif column == person:
                player = (i, j)
    return boxes, holes, player


def choose_route(grid):
    boxes, holes, player = find_locations(grid)
    paths = []
    for box in boxes:
        paths.append(bfs(grid, box, player))
    return min(paths)


def get_grid_X_and_Y(grid):
    width = max([len(r) for r in grid])
    height = len(grid)
    return width, height


def find_neighbors(cell, grid):
    width, height = get_grid_X_and_Y(grid)
    neighbors = lambda x, y: [
        (x2, y2)
        for x2 in range(x - 1, x + 2)
        for y2 in range(y - 1, y + 2)
        if (
            -1 < x <= width
            and -1 < y <= height
            and (x != x2 or y != y2)
            and (0 <= x2 <= width)
            and (0 <= y2 <= height)
        )
    ]
    return filter_neighbors(neighbors(cell[0], cell[1]), grid)


def filter_neighbors(neighbors, grid):
    return list(filter(lambda cell: grid[cell[0]][cell[1]] == "X", neighbors))


def bfs(grid, start, goal):
    width, height = get_grid_X_and_Y(grid)
    wall = "X"
    box = "*"
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == goal:
            return path

        for row, col in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (
                0 <= col < width
                and 0 <= row < height
                and grid[row][col] != wall
                and grid[row][col] != box
                and (row, col) not in seen
            ):
                queue.append(path + [(row, col)])
                seen.add((row, col))


def read_sokobans(filename):
    with open(filename, "r"):
        lines = f.readlines()

    all_grids = []
    for line in lines:
        if line.strip():
            line = line.split(",")[1].strip()
            height = int(line[0:2])
            width = int(line[2:4])
            maze = textwrap.wrap(line[4:], width)
            all_grids.append(maze)

    return all_grids


def parse_sokobans(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    start = 0
    line_count = 0
    all_grids = []
    while line_count < len(lines):
        maze_grid = []
        maze_number = lines[start + 1]
        size_x = int(lines[start + 2].split(":")[1].strip())
        size_y = int(lines[start + 3].split(":")[1].strip())
        for i, line in enumerate(lines[start + 5 : start + 5 + size_y]):
            while len(line) < size_x:
                line += " "
            maze_grid.append(line.replace("\n", ""))
        all_grids.append(maze_grid)
        start += size_y + 6
        line_count += start
    return all_grids


def reduce_puzzle(grid):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1]
        )

        # Eliminate Strategy
        values = eliminate(values)
        # Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1]
        )

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values.
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(grid):
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(grid)
    if values is False:
        return False  ## Failed earlier

    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!

    # Look for unfilled squares and choose one with the fewest possibilities
    _, box = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Recursive search to solve each one of the resulting sudokus
    for val in values[box]:
        sudoku_copy = values.copy()
        sudoku_copy[box] = val
        attempt = search(sudoku_copy)
        if attempt:
            return attempt


def solve(grid):
    return search(grid)


def solve_all(grids, name=""):
    """Attempt to solve a sequence of grids. Report results."""
    times, results = zip(*[time_solve(grid) for grid in grids])
    if len(results):
        print(results[0])


def time_solve(grid):
    start = time.time()
    result = solve(grid)
    t = time.time() - start
    return (t, solved(result), result)


def solved(grid):
    for _, row in grid.items():
        if "." in row:
            return False
    return True


if __name__ == "__main__":
    solve_all(parse_sokobans("levels.txt"))
