## Solve Every Sudoku Puzzle
##
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}

def cross(a, b):
    """
    Return the list formed by all the possible concatenations
    of a letter s in string a with a letter t in string b.
    Args:
        a, b: strings.
    Returns:
        list: All the possible concatenations of letters.
    """
    return [s+t for s in a for t in b]

digits = "123456789"
rows = "ABCDEFGHI"
cols = digits
boxes = cross(rows, cols)

# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.
row_units = [cross(r, cols) for r in rows]

# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.
column_units = [cross(rows, c) for c in cols]

# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

################ Unit Tests ################

def test():
    "A set of tests that must pass."
    assert len(boxes) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in boxes)
    assert all(len(peers[s]) == 20 for s in boxes)
    assert units['C2'] == [['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
                           
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')

################ Grid Parser ###############

def grid_values(grid):
    """
    Convert grid string into {<box>: <value>} dict with '.' value for empties.
    Args:
        grid: Sudoku grid in string form, 81 characters long.
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'.
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"

    chars = []
    for c in grid:
        if c in '0.' :
            chars.append(digits)
        elif c in digits:
            chars.append(c)

    assert len(chars) == 81
    return dict(zip(boxes, chars))

################ Constraint Propagation ################

def eliminate(values):
    """
    Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values



def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate Strategy
        values = eliminate(values)
        # Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values.
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

################ Search ################

def solve(grid): return search(grid_values(grid))

def search(values):
    """ 
    Using depth-first search and propagation, try all possible values.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier

    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    # Look for unfilled squares and choose one with the fewest possibilities
    _, box = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Recursive search to solve each one of the resulting sudokus
    for val in values[box]:
        sudoku_copy = values.copy()
        sudoku_copy[box] = val
        attempt = search(sudoku_copy)
        if attempt:
            return attempt

################ Display as 2-D grid ################

def display(values):
    """
    Display the values as a 2-D grid.
    Args: 
        The sudoku in dictionary form.
    Output: None.
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print()

################ System test ################

import time

def solve_all(grids, name=''):
    """Attempt to solve a sequence of grids. Report results."""
    times, results = zip(*[time_solve(grid.strip()) for grid in grids])
    N = len(results)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times)))
            
def time_solve(grid):
    start = time.clock()
    values = solve(grid)
    t = time.clock() - start
    return (t, solved(values))

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit):
        return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    
if __name__ == '__main__':
    test()
    solve_all(open("../data/sudoku-easy50.txt"), "easy")
    solve_all(open("../data/sudoku-top95.txt"), "hard")
    solve_all(open("../data/sudoku-hardest.txt"), "hardest")