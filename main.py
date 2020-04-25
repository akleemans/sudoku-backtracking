import csv

import time

from solver import Solver


def solve_all(filename: str):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='|', quotechar='"')
        sudoku_rows = [row for row in csv_reader]

    total_solving_time = 0
    count = 0
    for sudoku_row in sudoku_rows[:8]:
        start = time.time()
        solutions = Solver.solve(sudoku_row[0])
        end = time.time()
        if len(solutions) != 1:
            print('!!! Got multiple solutions:', solutions)
        # if solved_str == sudoku_row[1]:
        #    print('Successfully solved, solution matches!')
        # else:
        #    print('!!! Got a different solution than real solution :((')
        solving_time = end - start
        total_solving_time += solving_time
        print('Solved', count, 'in', round(solving_time, 8), 's')
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
    # if solved_str == sudoku_row[1]:
    #    print('Successfully solved, solution matches!')
    # else:
    #    print('!!! Got a different solution than real solution :((')
    print('Solved in', round(end - start, 8), 's')


if __name__ == "__main__":
    solve_all('sudokus_3x3.csv')
    # solve_single('.94...13..............76..2.8..1.....32.........2...6.....5.4.......8..7..63.4..8')
