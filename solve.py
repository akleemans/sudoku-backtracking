import csv
import time

from sudoku import Sudoku

with open('sudokus.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|', quotechar='"')
    sudokus = [row for row in csv_reader]

sudoku = sudokus[0]

s = Sudoku(sudoku[0])
print('Solving with difficulty "' + sudoku[2] + '"')
s.show()
start = time.time()
s.solve()
end = time.time()
s.show()
print('Solved in', round(end - start, 8), 's')
