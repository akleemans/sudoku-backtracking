import csv

import time

from solver import Solver

with open('sudokus.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|', quotechar='"')
    sudokus = [row for row in csv_reader]

sudoku_row = sudokus[0]

print('Solving', sudoku_row[0], 'with difficulty "' + sudoku_row[2] + '"')
start = time.time()
solutions = Solver.solve(sudoku_row[0])
if len(solutions) != 1:
    print('!!! Got multiple solutions:', solutions)

solved_str = solutions.pop()
end = time.time()
Solver.show(Solver.deserialize_from_str(solved_str))

if solved_str == sudoku_row[1]:
    print('Successfully solved, solution matches!')
else:
    print('!!! Got a different solution than real solution :((')

print('Solved in', round(end - start, 8), 's')
