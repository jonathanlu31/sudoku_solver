board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 0],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]

def solve(bd):
    empty = find_empty(bd)
    if not empty:
        return bd

    for i in range(1, 10):
        y, x = empty
        bd[y][x] = i

        if valid(bd, i, empty):
            solved = solve(bd)
            if solved:
                return solved
        
        bd[y][x] = 0

    return None    

def valid(bd, num, pos):
    y, x = pos

    # Check row
    for i in range(len(bd[y])):
        if bd[y][i] == num and i != x:
            return False
    
    # Check column
    for i in range(len(bd)):
        if bd[i][x] == num and i != y:
            return False

    # Check box
    box_y, box_x = (y // 3, x // 3)
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bd[i][j] == num and i != y and j != x:
                return False
    
    return True

def print_board(bd):
    for i in range(len(bd)):
        for j in range(len(bd[0])):
            print(bd[i][j], end = ' ')

            if j % 3 == 2 and j != 8:
                print('|', end=' ')
        print()
        if i % 3 == 2 and i != 8:
            print("-"*21)

def find_empty(bd):
    for i in range(len(bd)):
        for j in range(len(bd[0])):
            if bd[i][j] == 0:
                return i, j
