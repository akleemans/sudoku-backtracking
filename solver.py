from __future__ import annotations

from tkinter import *
from typing import List, Tuple, Optional

from sudoku import Sudoku


class Solver:
    solutions: List[str] = []

    @staticmethod
    def solve(sudoku_str: str) -> str:
        """Build and solve Sudoku"""
        sudoku = Solver.deserialize_from_str(sudoku_str)

        # initial propagation
        sudoku.propagate()

        Solver.show(sudoku)

        # If already solved or unsolvable, return
        if sudoku.solved():
            return str(sudoku)
        if not sudoku.valid():
            raise ValueError('Unsolvable Sudoku!')

        # Add current state to stack
        stack: List[Tuple[List[str], Optional[Tuple[int, str]]]] = [(sudoku.serialize(), None)]

        # Work on stack with Depth-First-Search (DFS)
        iterations = 0
        while len(stack) > 0:
            print('Working on stack, iteration =', iterations, ', stack size:', len(stack))
            iterations += 1
            candidates, last_guess = stack[-1]
            # TODO
            # Calculate list of possible guesses.
            # Guesses look like (41, '9'): "At index 41, try value '9'"

            # Create Sudoku from "serialized form"
            sudoku = Sudoku(candidates)
            possible_guesses: List[Tuple[int, str]] = Solver.get_guesses(sudoku)

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

            # Do next_guess
            print('Do next guess:', next_guess)
            idx, value = next_guess
            sudoku.cells[idx].candidates = value
            sudoku.propagate()

            # If still solvable, push to stack, else iterate
            if sudoku.solved():
                print('Solve loop: Found solution! Adding to solutions.')
                sudoku.solutions.append(str(sudoku))
                stack.pop()
            elif not sudoku.valid():
                # Update latest guess
                print('Solve loop: Invalid Sudoku, update guess on last stack item.')
                stack[-1] = (candidates, next_guess)
            else:
                print('Solve loop: Sudoku not solved after propagation but still valid, adding to stack.')
                stack.append((sudoku.serialize(), None))

        # For now, just return single solution
        solution = sudoku.solutions[0]
        return solution

    @staticmethod
    def deserialize_from_str(sudoku_str: str):
        """Build a Sudoku from a 12..5.42. etc list"""
        all_c = '123456789'
        return Sudoku([v if v != '.' else all_c for v in sudoku_str])

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

    @staticmethod
    def get_guesses(sudoku: Sudoku) -> List[Tuple[int, str]]:
        """
        Calculate guesses based on a Sudoku.
        This should be stable, as we depend on the order to check how far we're already with guessing.
        This can be optimized for guessing small candidate lists first.
        """
        guesses = []
        for cell in sudoku.cells:
            # If no single candidate on cell, we can guess.
            if len(cell.candidates) > 1:
                for c in cell.candidates:
                    guesses.append((cell.cell_id, c))
        return guesses
