from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, List, Dict

# ---------------------------------------------------------------------------
# Type alias
# ---------------------------------------------------------------------------
Cell = Tuple[int, int]   # (row, col)


# ---------------------------------------------------------------------------
# StepLogger
# ---------------------------------------------------------------------------
@dataclass
class LogEvent:
    action: str   # "assign" | "backtrack" | "prune"
    cell:   Cell
    value:  int


class StepLogger:
    """Records every assign / backtrack / prune event for animation."""

    def __init__(self):
        self.events: List[LogEvent] = []

    def log(self, action: str, cell: Cell, value: int):
        self.events.append(LogEvent(action=action, cell=cell, value=value))


# ---------------------------------------------------------------------------
# NonogramCSP
# ---------------------------------------------------------------------------
class NonogramCSP:
    """
    Represents a Nonogram puzzle as a CSP.

    Attributes
    ----------
    N : int
        Number of rows.
    M : int
        Number of columns.
    row_clues : list[tuple[int, ...]]
        row_clues[i] is the clue sequence for row i.
    col_clues : list[tuple[int, ...]]
        col_clues[j] is the clue sequence for column j.
    variables : list[Cell]
        All cells in row-major order: (0,0), (0,1), ..., (N-1, M-1).
    neighbors : dict[Cell, list[Cell]]
        All cells sharing a row or column with the key cell (excluding itself).
    """

    def __init__(
        self,
        N: int,
        M: int,
        row_clues: List[Tuple[int, ...]],
        col_clues: List[Tuple[int, ...]],
    ):
        self.N = N
        self.M = M
        self.row_clues = [tuple(c) for c in row_clues]
        self.col_clues = [tuple(c) for c in col_clues]

        # Variables in row-major order
        self.variables: List[Cell] = [
            (i, j) for i in range(N) for j in range(M)
        ]

        # Neighbour map: cells sharing the same row OR column
        self.neighbors: Dict[Cell, List[Cell]] = {}
        for cell in self.variables:
            r, c = cell
            nbrs = set()
            for j in range(M):
                if j != c:
                    nbrs.add((r, j))
            for i in range(N):
                if i != r:
                    nbrs.add((i, c))
            self.neighbors[cell] = list(nbrs)
