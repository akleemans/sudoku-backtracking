from __future__ import annotations

from typing import List, Set, Optional


class Cell:
    peers: Set[Cell] = set()
    value: Optional[str] = None
    candidates: str = ''
    initial: bool = False
    color: str = 'blue'
    id: int

    def __init__(self, value, id: int):
        self.id = id
        if value != '.':
            self.value = value
            self.initial = True
            self.color = 'black'
        else:
            self.candidates = '123456789'

    def add_peers(self, peers: List[Cell]) -> None:
        """Convenience method to add peers"""
        self.peers = self.peers | set(peers)
        print(self.id, 'has now peers:', len(self.peers))

    def propagate_to_peers(self) -> None:
        """Propagate own number to peers (if set)"""
        if self.value is not None:
            for peer in self.peers:
                peer.remove_candidate(self.value)

    def remove_candidate(self, value: str) -> None:
        """Remove candidate"""
        if value in self.candidates:
            print(self.id, 'Removing', value, 'from candidates:', self.candidates)
            self.candidates = self.candidates.replace(value, '')
            if len(self.candidates) == 1:
                # Has to be the solution
                self.value = self.candidates
                self.candidates = ''

    def __str__(self) -> str:
        """Return printable value"""
        return self.value if self.value is not None else ' '

    def reset(self) -> None:
        """Reset cell to start state"""
        if not self.initial:
            self.value = None
            self.candidates = '123456789'

    def valid(self) -> bool:
        """Returns if cell still valid"""
        if self.value is not None:
            return True
        else:
            # Check if any candidates are left
            return len(self.candidates) >= 1
