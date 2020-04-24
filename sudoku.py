from __future__ import annotations

from tkinter import *
from typing import Tuple

from cell import Cell


class Sudoku:

    def __init__(self, sudoku_str: str):
        # Init cells
        self.cells = []
        for i in range(len(sudoku_str)):
            cell = Cell(sudoku_str[i], i)
            self.cells.append(cell)

        # Build peers list
        for i in range(len(self.cells)):
            # row
            cell = self.cells[i]
            idx = i - i % 9
            row = [cell for cell in self.cells[idx:idx + 9]]
            cell.add_peers(row)

            # col
            cell = self.cells[i]
            base_idx = i % 9
            col = []
            for j in range(9):
                idx = j * 9 + base_idx
                col.append(self.cells[idx])
            cell.add_peers(col)

            # TODO 3x3 block
            block_y = (i % 9) - i % 3
            block_x = (i - i % 9) % 3  # ???

            block = []
            for y in range(3):
                for x in range(3):
                    idx = (block_x + x) * 9 + block_y + y
                    block.append(self.cells[idx])
            # cell.add_peers(block)

    def solve(self):
        """Solve Sudoku"""
        # initial propagation
        self.propagate()

        # Add current state to
        # stack = [self.serialize()]
        # TODO try with backtracking

    def propagate(self):
        """Propagate"""
        h = ()
        while self.get_hash() != h:
            h = self.get_hash()
            print('Propagating with hash =', h)
            for cell in self.cells:
                cell.propagate_to_peers()
        # TODO check if still solvable

    def get_hash(self) -> Tuple[int, int]:
        """Calculate hash to detect changes"""
        filled = sum([1 for cell in self.cells if cell.value is not None])
        candidates = sum([len(cell.candidates) for cell in self.cells])
        return filled, candidates

    def solvable(self) -> bool:
        """Checks if Sudoku still solveable"""
        return all([cell.valid() for cell in self.cells])

    def __str__(self) -> str:
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
