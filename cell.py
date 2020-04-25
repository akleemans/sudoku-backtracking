from __future__ import annotations

from typing import List, Set, Optional


class Cell:
    peers: Set[Cell] = set()
    candidates: str = '123456789'
    initial: bool = False
    color: str = 'blue'
    cell_id: int

    def __init__(self, candidates: str, cell_id: int):
        self.cell_id = cell_id
        self.candidates = candidates
        if len(candidates) == 1:
            self.initial = True
            self.color = 'black'

    def add_peers(self, peers: Set[Cell]) -> None:
        """Convenience method to add peers"""
        self.peers = self.peers | peers
        print(self.cell_id, 'has now # of peers:', len(self.peers))

    def propagate_to_peers(self) -> None:
        """Propagate own number to peers (if set)"""
        if len(self.candidates) == 1:
            for peer in self.peers:
                peer.remove_candidate(self.candidates)

    def remove_candidate(self, value: str) -> None:
        """Remove value from candidates"""
        if value in self.candidates:
            print(self.cell_id, 'Removing', value, 'from candidates:', self.candidates)
            self.candidates = self.candidates.replace(value, '')

    def __str__(self) -> str:
        """Return printable value"""
        return self.candidates if len(self.candidates) == 1 else ' '

#    def reset(self) -> None:
#        """Reset cell to start state"""
#        if not self.initial:
#            self.candidates = '123456789'

    def valid(self) -> bool:
        """Returns if cell still valid"""
        return len(self.candidates) >= 1

    def solved(self) -> bool:
        """Returns if cell has a value"""
        return len(self.candidates) == 1
