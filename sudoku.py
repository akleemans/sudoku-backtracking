from __future__ import annotations

from typing import List, Set

from cell import Cell


class Sudoku:
    cells: List[Cell]
    units: List[List[Cell]] = []

    def __init__(self, candidate_list: List[str]):
        # Init cells
        self.cells = []
        for i in range(len(candidate_list)):
            candidates = candidate_list[i]
            cell = Cell(candidates, i)
            self.cells.append(cell)

        # Build peers list
        for i in range(len(self.cells)):
            # row
            cell = self.cells[i]
            idx = i - i % 9
            row = set(c for c in self.cells[idx:idx + 9] if c != cell)

            # column
            cell = self.cells[i]
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
        for c in range(9):
            row = [cell for cell in self.cells[c * 9:(c + 1) * 9]]
            self.units.append(row)

        for r in range(9):
            col = []
            for c in range(9):
                col.append(self.cells[r + c * 9])
            self.units.append(col)

        for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]:
            block = [self.cells[idx] for idx in self.get_block_ids(i)]
            self.units.append(block)

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

    def propagate(self):
        """
        Propagate constraints:
            (1) If a cell holds a value, no other peer of cell can hold that value.
            (2) If a value can only be held by a single cell in unit, that cell can not hold another value.
        """
        h = 81 * 9
        while self.valid() and self.get_hash() != h:
            h = self.get_hash()
            # print('Propagating with total candidates =', h)
            # Propagate (1)
            for cell in self.cells:
                cell.propagate_to_peers()
            # Propagate (2)
            for unit in self.units:
                quit_flag = False
                all_candidates = ''.join([c.candidates for c in unit])
                for i in range(1, 10):
                    value = str(i)
                    # if only once in unit, remove other candidates from that cell
                    if all_candidates.count(value) == 1:
                        cell = [c for c in unit if value in c.candidates].pop()
                        if len(cell.candidates) > 1:
                            # print(cell.cell_id, 'Removing candidates:', cell.candidates, 'can only be', value)
                            cell.candidates = value
                            quit_flag = True
                            break
                if quit_flag:
                    break

    def get_hash(self) -> int:
        """Calculate hash to detect changes"""
        candidates = sum([len(cell.candidates) for cell in self.cells])
        return candidates

    def valid(self) -> bool:
        """Checks if Sudoku still solvable"""
        # Check if all cells are still valid
        if not all([cell.valid() for cell in self.cells]):
            return False

        # Check for units
        for unit in self.units:
            all_candidates = ''.join([c.candidates for c in unit])
            if not all([str(v) in all_candidates for v in range(1, 10)]):
                return False
        return True

    def solved(self):
        """Checks if Sudoku is solved"""
        return all([cell.solved() for cell in self.cells])

    def serialize(self) -> List[str]:
        """Return a serialized form"""
        return [cell.candidates for cell in self.cells]

    def __str__(self) -> str:
        """Print the Sudoku"""
        return ''.join(str(c) for c in self.cells).replace(' ', '.')
