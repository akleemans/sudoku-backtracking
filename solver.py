from __future__ import annotations

from tkinter import *
from typing import List, Tuple, Optional, Set

from sudoku import Sudoku

debug: bool = False


class Solver:
    solutions: List[str] = []

    @staticmethod
    def solve(sudoku_str: str, solve_all=False) -> Set[str]:
        """Build and solve a Sudoku"""
        sudoku = Solver.deserialize_from_str(sudoku_str)

        # initial propagation
        sudoku.propagate()
        # print('Sudoku after first propagation:')
        # Solver.show(sudoku)

        # If already solved or unsolvable, return
        if sudoku.solved():
            return {str(sudoku)}
        if not sudoku.valid():
            raise ValueError('Unsolvable Sudoku!')

        # Add current state to stack:
        # 1. current Sudoku as List of candidates,
        # 2. The guess next up for next layer in format (41, '9'): "At index 41, try value '9'"
        # Note that current_guess means next guess to try on the current layer, and the tried guess on an earlier layer.
        next_guess = Solver.calculate_guesses(sudoku)[0]
        stack: List[Tuple[List[str], Optional[Tuple[int, str]]]] = [(sudoku.serialize(), next_guess)]

        # Work on stack with Depth-First-Search (DFS)
        iterations = 0
        solutions = set()
        while len(stack) > 0:
            if iterations % 100 == 0:
                print('>> Iteration ' + str(iterations) + ' /stack:' + str(len(stack)) + '/sol: ' + str(len(solutions)))
            Solver.log('>> Iteration ' + str(iterations) + ' / stack size:' + str(len(stack)) + '/ solutions: ' + str(
                len(solutions)) + ' path: ' + str([i[1] for i in stack]))
            iterations += 1
            candidates, current_guess = stack[-1]

            # Create Sudoku from "serialized" form
            sudoku.set_state(candidates)

            if current_guess is None:
                # If no more guess, pop element and iterate on next upper layer
                stack.pop()
                possible_guesses = Solver.calculate_guesses(sudoku)
                next_guess = possible_guesses[0]
                stack[-1] = (stack[-1][0], next_guess)
                continue

            # possible_guesses: List[Tuple[int, str]] = Solver.calculate_guesses(sudoku)
            # if possible_guesses[-1] == current_guess:
            #    # End is reached in this branch
            #    stack.pop()
            #    continue
            # elif current_guess is None:
            #    # Try first guess
            #    next_guess = possible_guesses[0]
            # else:
            #    idx = possible_guesses.index(current_guess)
            #    next_guess = possible_guesses[idx + 1]

            # Do next_guess
            Solver.log('Do proposed guess: ' + str(current_guess))
            idx, value = current_guess
            sudoku.cells[idx].candidates = value
            sudoku.propagate()

            if debug:
                # Solver.show(sudoku)
                Solver.show_console(sudoku)

            # If still solvable, push to stack, else iterate
            if sudoku.solved():
                Solver.log('Solve loop: Found solution! Adding to solutions.')
                return {str(sudoku)}
            # TODO rework for multiple / all solutions
#                if not solve_all:
#                    return {str(sudoku)}
#                else:
#                    solutions.add(str(sudoku))
#                    stack[-1] = (candidates, next_guess)
            elif not sudoku.valid():
                # Update latest guess
                Solver.log('Solve loop: Invalid Sudoku, move on to next guess on last stack item.')
                sudoku.set_state(candidates)
                possible_guesses = Solver.calculate_guesses(sudoku)
                idx = possible_guesses.index(current_guess) + 1
                if idx == len(possible_guesses):
                    # We already worked on last guess, mark stack to go back
                    stack[-1] = (candidates, None)
                else:
                    # Try next possibility on state
                    next_guess = possible_guesses[idx]
                    stack[-1] = (candidates, next_guess)
            else:
                # Proceed to next layer
                Solver.log('Solve loop: Sudoku not solved after propagation but still valid, adding to stack.')
                stack[-1] = (candidates, next_guess)
                possible_guesses = Solver.calculate_guesses(sudoku)
                next_guess = possible_guesses[0]
                stack.append((sudoku.serialize(), next_guess))

        # For now, just return single solution
        Solver.log('Finished checking, found solutions:' + str(solutions))
        return solutions

    @staticmethod
    def log(s: str) -> None:
        """Print to console if debug mode is on"""
        if debug:
            print(s)

    @staticmethod
    def deserialize_from_str(sudoku_str: str):
        """Build a Sudoku from a 12..5.42. etc list"""
        sudoku = Sudoku()
        sudoku.set_state([v if v != '.' else '123456789' for v in sudoku_str])
        return sudoku

    @staticmethod
    def show(sudoku: Sudoku):
        """Show GUI"""
        window = Tk()
        window.geometry("480x500")
        window.title("Sudoku")
        for i in range(len(sudoku.cells)):
            cell = sudoku.cells[i]
            value = str(cell)
            if value == ' ':
                # value = '1 2 3\n4 5 6\n7 8 9'
                value = '\n'.join(
                    [' '.join([(str(i) if str(i) in cell.candidates else ' ') for i in range(j * 3 + 1, j * 3 + 3 + 1)])
                     for j in range(3)])
                label = Label(window, text=value, width=6, height=3, borderwidth=1, relief="solid",
                              font=("Helvetica", 14), fg='black')
            else:
                label = Label(window, text=value, width=4, height=2, borderwidth=1, relief="solid",
                              font=("Helvetica", 22), fg='black')
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
        input()

    @staticmethod
    def calculate_guesses(sudoku: Sudoku) -> List[Tuple[int, str]]:
        """
        Calculate a list of guesses based on a partially filled Sudoku.
        This should be stable, as we depend on the order to check how far we're already with guessing.
        The order of guesses is optimized for small candidate lists first (minimum remaining values).
        """
        guesses = []
        for cell in sudoku.cells:
            # If no single candidate on cell, we can guess.
            if len(cell.candidates) > 1:
                for c in cell.candidates:
                    guesses.append((cell.cell_id, c, len(cell.candidates)))
        sorted_guesses = sorted(guesses, key=lambda x: x[2])
        return [(g[0], g[1]) for g in sorted_guesses]
