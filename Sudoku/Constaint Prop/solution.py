from collections import defaultdict

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
left_diag  = [ rows[i] + cols[i] for i in range(len(rows))]
right_diag = [ rows[i] + cols[len(cols) - i - 1] for i in range(len(rows))]
diag = [left_diag] + [right_diag]
unitlist = row_units + column_units + square_units + diag
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """    

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers


    #print('Before:',display(values))

    for unit in unitlist:
        val_boxes = defaultdict(list)    	
        for box in unit:
            if len(values[box]) == 2:    			
                val_boxes[values[box]].append(box)

        for val,box_list in val_boxes.items():	    	
            if len(box_list) == 2:
                #print (unit,box_list)
                other_boxes = set(unit) - set(box_list)
                for oth_box in other_boxes:
                    for v in val:
                        if v in values[oth_box]:
                            assign_value(values, oth_box, values[oth_box].replace(v, ''))
                            #values[oth_box] = values[oth_box].replace(v, '')

    #print('After:',display(values))
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
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
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

    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:   
            assign_value(values, peer, values[peer].replace(digit,''))         
            #values[peer] = values[peer].replace(digit,'')
    return values
     

def only_choice(values):

    new_values = values.copy()  # note: do not modify original values
    # TODO: Implement only choice strategy here
    
    for unit in unitlist:
        dig_loc = defaultdict(list)
        for box in unit:
            for char in values[box]:
                dig_loc[char].append(box)
        
        for k,v in dig_loc.items():
            if len(v) == 1:
                new_values[v[0]] = k
                
    return new_values    

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values    

def search(values):    
    values = reduce_puzzle(values)
    if values != False:

        if isSolved(values):                        
            return values
        else:

            min_len = 99
            min_bx = ''
            for k,v in values.items():
                if len(v) < min_len and len(v) > 1:
                    min_len = len(v)
                    min_bx = k
            
            for dig in values[min_bx]:
                new_vals = values.copy()
                new_vals[min_bx] = dig
                x = search(new_vals)
                if x!= None:
                    return x    

def isSolved(values):
    
    for k,v in values.items():
        if len(v) != 1:
            return False
    
    return True

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)    
    return search(values)        

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
