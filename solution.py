"""
 Python program to solve sudoku puzzles.
 Author: Aravind Raghunathan.
 The program attempts to solve a standard 9x9 Sudoku puzzle by using AI constrain propagation & search
 techniques ( Specifically,  Naked Twins, Elimination, Only-Choice & Search).
 Code developed as part of th requirement for Udacity AI degree program.
"""
assignments = []

# Defining identities for rows and columns in a 9x9 sudoku board
rows = 'ABCDEFGHI'
cols = '123456789'
rowsreverse = 'IHGFEDCBA'


# Function to return the cross product of input arguments
def cross(A, B):
    return [s + t for s in A for t in B]

# Creating identities for each sudoku grid
boxes = cross(rows, cols)

# Creating multiple entities for manipulation of data.
# Obtained from the file utils.py provided by Udacity.
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
#units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
units = dict()
for s in boxes:
    units[s] = []
    for u in unitlist:
        if s in u:
            units[s] = units[s] + [u]
#print(units)



#peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
peers = dict()
for s in boxes:
    peers[s] = []
    for u in unitlist:
        if s in u:
            peers[s] = peers[s] + u
            peers[s].remove(s)

#print(peers)
squarepeers = dict((s, [u for u in square_units if s in u]) for s in boxes)

# Creating left, right diagonal units and combine with unitlist
left_diag_unit = []
for index in range(0,9):
    left_diag_unit.append(rows[index]+cols[index])


right_diag_unit = []
for index in range(0,9):
    right_diag_unit.append(rowsreverse[index]+cols[index])

diag_units = [left_diag_unit,right_diag_unit]

unitlist = unitlist + diag_units



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    Just a check
    """
    values[box] = value
    #if len(value) == 1:
    assignments.append(values.copy())
    return values

def naked_twins(values):
    """
        Eliminate values using the naked twins strategy.
        Args:
            values(dict): a dictionary of the form {'box_name': '123456789', ...}

        Returns:
            the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of boxes with 2 values in it
    twinBoxes = []
    for boxID in values.keys():
        if len(values[boxID]) == 2:
            twinBoxes.append(boxID)

    # Get values from boxes with 2 numbers
    for entries in twinBoxes:
        twinvalues = values[entries]
        # print(twinvalues)
        # Search in peers for a box with the same value
        for peerentries in peers[entries]:
            if values[peerentries] == twinvalues:
                # print('found')
                for unitentries in units[entries]:
                    # print(unitentries)
                        # Find in units
                        if peerentries in unitentries:
                            for entries2 in unitentries:
                                # Find non twin boxes
                                if entries2 not in [entries, peerentries]:
                                    # Replace twin entries by null
                                    for nums in twinvalues:
                                        # print('nums =',nums)
                                        values[entries2] = values[entries2].replace(nums,'')
                                        assign_value(values,entries2,values[entries2])
    return values




def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    modifiedGrid = []
    for entries in grid:
        if entries in cols:
            modifiedGrid.append(entries)
        if entries == '.':
            modifiedGrid.append(cols)

    zippedGrid = zip(boxes, modifiedGrid)
    dictValues = dict(zippedGrid)
    return dictValues

def display(values):
    """
        Function to display the values of the sudoky puzzle as a 2-D grid.
        Args:
            values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """
        Function to eliminate values from peers of each box with a single value.
        Function loops through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.

        Args:
            Sudoku puzzle in dictionary form.
        Returns:
            Sudoku puzzle in dictionary form after eliminating values.
    """
    # Get solved boxes from the puzzle
    solvedBoxes = []
    for boxID in values.keys():
        if len(values[boxID]) == 1:
            solvedBoxes.append(boxID)

    # Check the values of the solved box peers for solved box value and replace with null
    for entries in solvedBoxes:
        solvedBoxEntry = values[entries]
        for solvedBoxPeer in peers[entries]:
            values[solvedBoxPeer] = values[solvedBoxPeer].replace(solvedBoxEntry,'')
            assign_value(values,solvedBoxPeer,values[solvedBoxPeer])
    return values


def only_choice(values):
    """
        Fucntion to finalize all values that are the only choice for a unit.
        Fuction goes through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

    Args:
        Sudoku puzzle in dictionary form.
    Returns:
        Sudoku puzzle in dictionary form after filling in only choices.
    """

    for entries in unitlist:
        for num in cols:
            boxwithvalues = []
            for boxentries in entries:
                if num in values[boxentries]:
                    boxwithvalues.append(boxentries)
            if len(boxwithvalues) == 1:
                values[boxwithvalues[0]] = num
                assign_value(values,boxwithvalues[0],values[boxwithvalues[0]])
    return values


def reduce_puzzle(values):
    """
        Reduces the puzzle by repeatedly calling the functions eliminate and only_choice
        until the program converges to a solution or no other changes are possible.

    Args:
        Sudoku puzzle in dictionary form.
    Returns:
        Sudoku puzzle in dictionary form after the program converges or no possible changes.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Calling eliminate function
        values = eliminate(values)
        # Calling the only_choice function
        values = only_choice(values)
        # Check how many boxes have a determined value after going through eliminate & only_choice, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
        Function identifies boxes with less number of entries and uses depth first search to branch out and try
        to solve the puzzle recursively.

    Args:
        Sudoku puzzle in dictionary form.
    Returns:
        Sudoku puzzle in dictionary form after the program converges.
    """

    # Reduce the puzzle by going through elimination and only_choice functions
    values = reduce_puzzle(values)

    if values is False:
        return False
    if all(len(values[s]) == 1 for s in boxes):
        return values

    # Find unsolved candidate boxes to search with that have more than 1 values
    minlength, minboxes = min((len(values[entries]), entries) for entries in boxes if len(values[entries]) > 1)

    # Select unsolved box entry to try out and search recursively
    for unsolvedboxentries in values[minboxes]:
        modifiedpuzzle = values.copy()
        modifiedpuzzle[minboxes] = unsolvedboxentries
        assign_value(values,minboxes,modifiedpuzzle[minboxes])
        modifiedpuzzle2 = search(modifiedpuzzle)
        if modifiedpuzzle2:
            return modifiedpuzzle2


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'.
    Returns:
        The dictionary representation of the final sudoku grid.
    """

    # First reduce the puzzle and run through depth first search to arrive at a possible solution
    reducedpuzzle = reduce_puzzle(grid_values(grid))
    searchedpuzzle = search(reducedpuzzle)
    return searchedpuzzle


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
