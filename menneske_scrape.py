import csv
import random

import requests
import time


def parse(content: str) -> str:
    s = ''
    for row in content.split('<tr class="grid">'):
        for cell in row.split('<td class="')[1:]:
            cell_content = cell.split('>')[1].split('<')[0].replace('&nbsp;', '')
            s += cell_content if len(cell_content) == 1 else '.'
    return s


base_url = 'http://www.menneske.no/sudoku/eng/random.html?diff='
solution_url = 'http://www.menneske.no/sudoku/eng/solution.html?number='

sudokus = []
for difficulty in range(1, 10):
    url = base_url + str(difficulty)
    for i in range(10):
        print('Getting Sudoku', i, 'for difficulty', difficulty)
        content = requests.get(url).text
        nr = content.split('<a href="solution.html?number=')[1].split('"')[0]
        puzzle = parse(content)
        content = requests.get(solution_url + nr).text
        solution = parse(content)
        sudokus.append([puzzle, solution, difficulty, nr])
        time.sleep(1 + random.random())

with open('menneske_random.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerows(sudokus)
