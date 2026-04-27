"""Minesweeper - Cell model.

STORY-001-T2: Initialize Python project with __init__.py files and base modules.
Represents a single cell on the Minesweeper board.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional


class CellState(Enum):
    """Enumerates the possible states of a cell."""

    HIDDEN = "hidden"
    REVEALED = "revealed"
    FLAGGED = "flagged"
    QUESTION = "question"


class Cell:
    """Represents a single cell on the Minesweeper board.

    Attributes:
        row: The row index of this cell (0-based).
        col: The column index of this cell (0-based).
        is_mine: Whether this cell contains a mine.
        state: The current display state of the cell.
        adjacent_mines: The count of mines in the 8 neighboring cells.
    """

    def __init__(self, row: int, col: int) -> None:
        """Initialize a Cell.

        Args:
            row: The row index of this cell (0-based).
            col: The column index of this cell (0-based).
        """
        self.row: int = row
        self.col: int = col
        self.is_mine: bool = False
        self.state: CellState = CellState.HIDDEN
        self.adjacent_mines: int = 0

    def reset(self) -> None:
        """Reset the cell to its default hidden state.

        STORY-001-T2: Stub implementation for Cell.reset().
        """
        self.state = CellState.HIDDEN
        self.is_mine = False
        self.adjacent_mines = 0

    def __repr__(self) -> str:
        """Return a string representation of the Cell.

        Returns:
            A string like 'Cell(0,0) mine=False state=HIDDEN'.
        """
        return (
            f"Cell({self.row},{self.col}) "
            f"mine={self.is_mine} state={self.state.value}"
        )
