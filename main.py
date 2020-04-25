import csv

import time

from solver import Solver


def solve_all(filename: str, puzzles_only=False):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        sudoku_rows = [row for row in csv_reader]

    total_solving_time = 0
    count = 0
    for sudoku_row in sudoku_rows:
        if puzzles_only:
            puzzle = sudoku_row[0]
        else:
            puzzle, expected_solution, difficulty, nr = sudoku_row

        start = time.time()
        solutions = Solver.solve(puzzle)
        end = time.time()
        if len(solutions) != 1:
            print('!!! Got multiple solutions:', solutions)
        if not puzzles_only and solutions.pop() != expected_solution:
            print('!!! Got a different solution than real solution :((')
        solving_time = end - start
        total_solving_time += solving_time
        print('Solved', count, ('/diff:' + str(difficulty) if not puzzles_only else ''), 'in', round(solving_time, 8),
              's')
        # print('Solved', count, 'with difficulty', difficulty, 'in', round(solving_time, 8), 's')
        count += 1
    print('Solved all in', round(total_solving_time, 8), 's')


def solve_single(sudoku_str: str):
    start = time.time()
    solutions = Solver.solve(sudoku_str)
    if len(solutions) == 0:
        print('!!! Got no solution :(((')
    elif len(solutions) > 1:
        print('!!! Got multiple solutions:', solutions)

    solved_str = solutions.pop()
    end = time.time()
    Solver.show(Solver.deserialize_from_str(solved_str))
    print('Solved in', round(end - start, 8), 's')


if __name__ == "__main__":
    # solve_all('hard-magictour95.csv', True)
    # solve_all('sudokus2.csv')
    # solve_single('.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8')

    # first of Norvigs "hard" puzzles
    solve_single('4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......')
