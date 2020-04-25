import csv

import time

from solver import Solver

with open('sudokus.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|', quotechar='"')
    sudokus = [row for row in csv_reader]

sudoku = sudokus[0]

print('Solving with difficulty "' + sudoku[2] + '"')
start = time.time()
solved_str = Solver.solve(sudoku[0])
end = time.time()
Solver.show(Solver.deserialize_from_str(solved_str))
print('Solved in', round(end - start, 8), 's')
