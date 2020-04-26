from __future__ import annotations

from typing import List, Optional

from cell import Cell


class Sudoku:
    cells: List[Cell] = []
    units: List[List[Cell]]

    def __init__(self, candidates: Optional[List[str]] = None):
        """Initialize Sudoku with empty structure (cells & units)"""
        self.cells = [Cell(i) for i in range(81)]

        # Build peers list
        for i in range(len(self.cells)):
            cell = self.cells[i]

            # row
            idx = i - i % 9
            row = set(c for c in self.cells[idx:idx + 9] if c != cell)

            # column
            base_idx = i % 9
            col = set()
            for j in range(9):
                idx = j * 9 + base_idx
                c = self.cells[idx]
                if c != cell:
                    col.add(c)

            # 3x3 block
            block = set(self.cells[idx] for idx in self.get_block_ids(i) if idx != i)

            # Set peers on cell
            cell.peers = row | col | block

        # Build units
        self.units = []
        for idx in range(9):
            self.units.append([c for c in self.cells[idx * 9:(idx + 1) * 9]])

        for r_idx in range(9):
            self.units.append([self.cells[r_idx + c_idx * 9] for c_idx in range(9)])

        for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
            block = [self.cells[idx] for idx in self.get_block_ids(i)]
            self.units.append(block)

        # If candidate list was provided, set it
        if candidates is not None:
            self.set_state(candidates)

    def set_state(self, candidate_list: List[str]) -> None:
        """Reset cells to a state"""
        for i in range(len(self.cells)):
            self.cells[i].candidates = candidate_list[i]

    @staticmethod
    def get_block_ids(idx: int) -> List[int]:
        """Return list of cell indexes for block"""
        block_idx = []
        block_y = (idx % 9) - idx % 3
        line_start = int((idx - idx % 9) / 9)
        block_x = line_start - line_start % 3
        for x in range(3):
            for y in range(3):
                idx = (block_x + x) * 9 + block_y + y
                block_idx.append(idx)
        return block_idx

    def propagate(self) -> None:
        """Propagate constraints:
            (1) If a cell holds a value, no other peer of cell can hold that value.
            (2) If a value can only be held by a single cell in unit, that cell can not hold another value.
        """
        total_candidates = 81 * 9
        while self.valid() and self.get_total_candidates() < total_candidates:
            total_candidates = self.get_total_candidates()
            # Propagate (1)
            for cell in self.cells:
                cell.propagate_to_peers()
            # Propagate (2)
            for unit in self.units:
                all_candidates = ''.join([c.candidates for c in unit])
                for i in range(1, 10):
                    value = str(i)
                    if all_candidates.count(value) == 1:
                        cells = [c for c in unit if value in c.candidates]
                        cell = cells.pop()
                        if len(cell.candidates) > 1:
                            cell.candidates = value
                            break

    def get_total_candidates(self) -> int:
        """Calculate hash to detect changes"""
        return sum([len(cell.candidates) for cell in self.cells])

    def valid(self) -> bool:
        """Checks if Sudoku still solvable"""
        if not all([cell.valid() for cell in self.cells]):
            return False

        # Check if units can still contain all numbers
        for unit in self.units:
            all_candidates = ''.join([c.candidates for c in unit])
            if not all([(str(v) in all_candidates) for v in range(1, 10)]):
                return False

        # Check if units contain numbers only once
        for unit in self.units:
            all_values = ''.join([c.candidates for c in unit if len(c.candidates) == 1])
            if not all([all_values.count(str(v)) <= 1 for v in range(1, 10)]):
                return False
        return True

    def solved(self) -> bool:
        """Checks if Sudoku is solved"""
        if not all([cell.solved() for cell in self.cells]):
            return False

        for unit in self.units:
            values = ''.join([c.candidates for c in unit])
            if not len(values) == 9 or not all([(v in values) for v in '123456789']):
                return False
        return True

    def serialize(self) -> List[str]:
        """Return a serialized form"""
        return [cell.candidates for cell in self.cells]

    def __str__(self) -> str:
        """Return a condensed string representation of the Sudoku"""
        return ''.join(str(c) for c in self.cells).replace(' ', '.')
