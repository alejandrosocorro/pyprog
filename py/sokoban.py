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


def transform_grid(grid):
    new_grid = []
    for row in grid:
        line = row.replace("0", " ")
        line = line.replace("1", "X")
        line = line.replace("2", ".")
        line = line.replace("3", "*")
        line = line.replace("4", "@")
        line = line.replace("5", "&")
        line = line.replace("6", "$")
        new_grid.append(line)
    return new_grid


def find_locations(grid):
    box, hole, person, wall, box_on_whole, person_on_whole = (
        "*",
        ".",
        "@",
        "X",
        "&",
        "$",
    )
    boxes = []
    holes = []
    walls = []
    player = ()
    for i, row in enumerate(grid):
        for j, column in enumerate(row):
            if column == box:
                boxes.append((i, j))
            elif column == hole:
                holes.append((i, j))
            elif column == person:
                player = (i, j)
            elif column == wall:
                walls.append((i, j))
            elif column == box_on_whole:
                boxes.append((i, j))
            elif column == person_on_whole:
                player = (i, j)
    return boxes, holes, player, walls


def choose_box_to_push(grid):
    boxes, holes, player, walls = find_locations(grid)
    paths = []
    for box in boxes:
        paths.append(bfs(grid, box, player))
    return min(paths)


def get_grid_X_and_Y(grid):
    width = max([len(r) for r in grid])
    height = len(grid)
    return width, height


def move_player_trough_route(player, route, grid):
    x, y = route[0]
    neighbors = find_neighbors(x, y)
    pos = [i for i in neighbors if i in route][0]
    temp = list(grid[pos[0]])
    temp[pos[1]] = "@"
    grid[pos[0]] = "".join(temp)

    temp = list(grid[player[0]])
    replace_char = " "
    if player[1] == "$":
        replace_char = "."
    temp[player[1]] = replace_char
    grid[player[0]] = "".join(temp)
    return grid


def find_neighbors(x, y):
    return ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))


def bfs(grid, start, goal):
    width, height = get_grid_X_and_Y(grid)
    wall = "X"
    box = "*"
    box_on_whole = "&"
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if (x, y) == goal:
            return path

        for row, col in find_neighbors(x, y):
            if (
                0 <= col < width
                and 0 <= row < height
                and grid[row][col] != wall
                and grid[row][col] != box
                and grid[row][col] != box_on_whole
                and (row, col) not in seen
            ):
                queue.append(path + [(row, col)])
                seen.add((row, col))


def read_sokobans(filename):
    with open(filename, "r") as f:
        lines = f.readlines()

    all_grids = []
    for line in lines:
        if line.strip():
            line = line.split(",")[1].strip()
            height = int(line[0:2])
            width = int(line[2:4])
            maze = textwrap.wrap(line[4:], width)
            all_grids.append(transform_grid(maze))
    return all_grids


def display_sokoban(grid):
    for row in grid:
        print(row)


def reduce_sokoban(grid):
    stalled = False
    while not stalled:



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
    solve_all(parse_sokobans("sokoban_evels.txt"))
