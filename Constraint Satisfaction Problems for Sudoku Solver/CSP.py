import copy
import time

domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

def solve_sudoku(board):

    if select(board) == False:
        return board
    else:
        row = select(board)[0]
        col = select(board)[1]

        for value in domain:
            if isPossible(board, row, col, value) == True:
                board[row][col] = value
                solution = solve_sudoku(board)

                if solution != False:
                    return solution
                board[row][col] = 0

        return False


def select(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return [row, col]
    return False


def isPossible(board, row, col, value):
    for i in range(0, 9):
        if i != row and board[i][col] == value:
            return False

    for j in range(0, 9):
        if j != col and board[row][j] == value:
            return False

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(0, 3):
        for j in range(3):
            if i != row and j != col and board[start_row + i][start_col + j] == value:
                return False
    return True


def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                if isPossible(board, row, col, board[row][col]):
                    return True
    return False


if __name__ == '__main__':
    sudoku1 = [
        [6, 0, 8, 7, 0, 2, 1, 0, 0],
        [4, 0, 0, 0, 1, 0, 0, 0, 2],
        [0, 2, 5, 4, 0, 0, 0, 0, 0],
        [7, 0, 1, 0, 8, 0, 4, 0, 5],
        [0, 8, 0, 0, 0, 0, 0, 7, 0],
        [5, 0, 9, 0, 6, 0, 3, 0, 1],
        [0, 0, 0, 0, 0, 6, 7, 5, 0],
        [2, 0, 0, 0, 9, 0, 0, 0, 8],
        [0, 0, 6, 8, 0, 5, 2, 0, 3]
    ]
    sudoku2 = [
        [0, 7, 0, 0, 4, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 6, 1, 0],
        [3, 9, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 4, 0, 0, 9],
        [0, 0, 3, 0, 0, 0, 7, 0, 0],
        [5, 0, 0, 1, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 7, 6],
        [0, 5, 4, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 1, 0, 0, 5, 0]
    ]

    start1 = time.time()
    print("Original Puzzle:\t\t\t\t\t\t Solution:")

    puzzle = copy.deepcopy(sudoku1)

    if not solve(puzzle):
        solution = False
    else:
        solution = solve_sudoku(puzzle)

    if solution == False:
        print("FAILED")
    else:
        for i in range(9):
            print(sudoku1[i], "\t\t\t", solution[i])

    stop1 = time.time()
    print("Execution Time:", round(stop1 - start1, 2), "s")
    print("-----------------------------------------------------------------------")

    start2 = time.time()
    print("Original Puzzle:\t\t\t\t\t\t Solution:")

    puzzle = copy.deepcopy(sudoku2)

    if not solve(puzzle):
        solution = False
    else:
        solution = solve_sudoku(puzzle)

    if solution == False:
        print("FAILED")
    else:
        for i in range(9):
            print(sudoku2[i], "\t\t\t", solution[i])

    stop2 = time.time()
    print("Execution Time:", round(stop2 - start2, 2), "s")

