from __future__ import annotations

from tkinter import *
from typing import List, Set

from cell import Cell


class Sudoku:
    cells: List[Cell] = []
    units: List[List[Cell]] = []
    solutions: List[str] = []

    def __init__(self, sudoku_str: str):
        # Init cells
        for i in range(len(sudoku_str)):
            value = sudoku_str[i]
            cell = Cell(value, i)
            self.cells.append(cell)

        # Build peers list
        for i in range(len(self.cells)):
            # row
            cell = self.cells[i]
            idx = i - i % 9
            row = set(c for c in self.cells[idx:idx + 9] if c != cell)
            cell.add_peers(row)

            # column
            cell = self.cells[i]
            base_idx = i % 9
            col = set()
            for j in range(9):
                idx = j * 9 + base_idx
                c = self.cells[idx]
                if c != cell:
                    col.add(c)
            cell.add_peers(col)

            # 3x3 block
            block = set(self.cells[idx] for idx in self.get_block_ids(i) if idx != i)
            print('For cell', i, ': adding block', ', '.join([str(cell.cell_id) for cell in block]))
            cell.add_peers(block)

    @staticmethod
    def get_block_ids(idx: int) -> Set[int]:
        """Return list of cell indexes for block"""
        block_idx = set()
        block_y = (idx % 9) - idx % 3
        line_start = int((idx - idx % 9) / 9)
        block_x = line_start - line_start % 3
        for x in range(3):
            for y in range(3):
                idx = (block_x + x) * 9 + block_y + y
                block_idx.add(idx)
        return block_idx

    def solve(self):
        """Solve Sudoku"""
        # initial propagation
        self.propagate()

        """
        # Add current state to stack
        stack: List[Tuple[List[str], Optional[Tuple[int, int]]]] = [(self.serialize(), None)]
        # Work on stack with Depth-First-Search (DFS)
        while len(stack) > 0:
            sudoku, last_guess = stack[-1]
            # TODO calculate list of possible guesses
            possible_guesses = []
            if possible_guesses[-1] == last_guess:
                # End is reached in this branch
                stack.pop()
                continue
            elif last_guess is None:
                # Try first guess
                next_guess = possible_guesses[0]
            else:
                idx = possible_guesses.index(last_guess)
                next_guess = possible_guesses[idx + 1]
            # TODO deserialize
            s = Sudoku('')

            # Do next_guess
            idx, value = next_guess
            s.cells[idx].candidates = value
            s.propagate()

            # If still solvable, push to stack, else iterate
            if s.solved():
                self.solutions.append(str(s))
                stack.pop()
            if not s.valid():
                stack.pop()
            else:
                stack.append((s.serialize(), None))
        """

    def propagate(self):
        """
        Propagate constraints:
            (1) If a cell holds a value, no other cell in unit can hold that value.
            (2) If a value can only be held by a single cell in unit, that cell can not hold another value.
        """
        h = 81 * 9
        while self.get_hash() != h:
            h = self.get_hash()
            print('Propagating with hash =', h)
            # Propagate (1)
            for cell in self.cells:
                cell.propagate_to_peers()
            # Propagate (2)
            # for unit in self.units:
            #    unit.propagate()

    def get_hash(self) -> int:
        """Calculate hash to detect changes"""
        candidates = sum([len(cell.candidates) for cell in self.cells])
        return candidates

    def valid(self) -> bool:
        """Checks if Sudoku still solvable"""
        return all([cell.valid() for cell in self.cells])

    def solved(self):
        """Checks if Sudoku is solved"""
        return all([cell.solved() for cell in self.cells])

    def serialize(self) -> List[str]:
        """Return a serialized form"""
        return [cell.candidates for cell in self.cells]

    @staticmethod
    def deserialize(candidates: List[str]) -> Sudoku:
        """Return a serialized form"""
        s = Sudoku()
        s.cells = []
        for i in range(len(candidates)):
            cell = Cell(candidates, i)
            s.cells.append(cell)
        return s

    def printable_str(self) -> str:
        """Print the Sudoku"""
        c = 0
        r = 0
        s = ''
        for cell in self.cells:
            c += 1
            s += str(cell) + ' '
            if c == 9:
                r += 1
                s += '\n'
                if r in [3, 6]:
                    s += '-' * 21 + '\n'
                c = 0
            elif c in [3, 6]:
                s += '| '
        return s

    def __str__(self) -> str:
        """Print the Sudoku"""
        return ''.join(str(c) for c in self.cells).replace(' ', '.')

    def show(self):
        """Show GUI"""
        window = Tk()
        window.geometry("480x500")
        window.title("Sudoku")
        for i in range(len(self.cells)):
            cell = self.cells[i]
            label = Label(window, text=str(cell), width=4, height=2, borderwidth=1, relief="solid",
                          font=("Helvetica", 22), fg=cell.color)
            c = i % 9
            r = int((i - i % 9) / 9)
            padx = 2 if c % 3 == 1 else 0
            pady = 2 if r % 3 == 1 else 0
            label.grid(column=c, row=r, padx=padx, pady=pady)
        window.update()
        window.lift()
        window.attributes("-topmost", True)
        window.mainloop()
