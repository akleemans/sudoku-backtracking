from __future__ import annotations

from typing import Set


class Cell:
    peers: Set[Cell]
    candidates: str
    cell_id: int

    def __init__(self, cell_id: int):
        """Initialize Cell with cell_id (for debugging)"""
        self.cell_id = cell_id

    def propagate_to_peers(self) -> None:
        """Propagate own number to peers (if set)"""
        if len(self.candidates) == 1:
            for peer in self.peers:
                peer.remove_candidate(self.candidates)

    def remove_candidate(self, value: str) -> None:
        """Remove value from candidates"""
        if value in self.candidates:
            self.candidates = self.candidates.replace(value, '')

    def __str__(self) -> str:
        """Return printable value"""
        return self.candidates if len(self.candidates) == 1 else ' '

    def valid(self) -> bool:
        """Returns if cell still valid"""
        return len(self.candidates) >= 1

    def solved(self) -> bool:
        """Returns if cell has a value"""
        return len(self.candidates) == 1
