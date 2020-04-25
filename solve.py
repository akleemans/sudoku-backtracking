import csv

import time

from solver import Solver

with open('sudokus.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|', quotechar='"')
    sudokus = [row for row in csv_reader]

sudoku_row = sudokus[1]

print('Solving with difficulty "' + sudoku_row[2] + '"')
start = time.time()
solved_str = Solver.solve(sudoku_row[0])
end = time.time()
Solver.show(Solver.deserialize_from_str(solved_str))

if solved_str == sudoku_row[1]:
    print('Successfully solved, solution matches!')
else:
    print('Got a different solution than real solution :((')

print('Solved in', round(end - start, 8), 's')
