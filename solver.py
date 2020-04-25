from __future__ import annotations

from tkinter import *
from typing import List

from sudoku import Sudoku


class Solver:
    solutions: List[str] = []

    @staticmethod
    def solve(sudoku_str: str) -> str:
        """Build and solve Sudoku"""
        sudoku = Solver.deserialize_from_str(sudoku_str)

        # initial propagation
        sudoku.propagate()

        # If already solved or unsolvable, return
        if sudoku.solved():
            return str(sudoku)
        if not sudoku.valid():
            raise ValueError('Unsolvable Sudoku!')

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
            s = Sudoku()

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
        # For now, just return single solution
        solution = sudoku.solutions[0]
        return solution

    @staticmethod
    def deserialize_from_str(sudoku_str: str):
        """Build a Sudoku from a 12..5.42. etc list"""
        all_c = '123456789'
        return Sudoku([v if v != '.' else all_c for v in sudoku_str])

    @staticmethod
    def deserialize(candidates: List[str]) -> Sudoku:
        """Build a sudoku from candidate list"""
        return Sudoku(candidates)

    @staticmethod
    def show(sudoku: Sudoku):
        """Show GUI"""
        window = Tk()
        window.geometry("480x500")
        window.title("Sudoku")
        for i in range(len(sudoku.cells)):
            cell = sudoku.cells[i]
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

    @staticmethod
    def show_console(sudoku: Sudoku) -> None:
        """Print the Sudoku to console"""
        c = 0
        r = 0
        s = ''
        for cell in sudoku.cells:
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
        print(s)
