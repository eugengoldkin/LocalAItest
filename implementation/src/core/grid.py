"""Minesweeper - Grid model.

STORY-001-T2: Initialize Python project with __init__.py files and base modules.
Manages the 2D grid of cells for the Minesweeper game.
"""

from __future__ import annotations

from typing import List, Optional

from src.core.cell import Cell, CellState


class Grid:
    """Manages the 2D grid of cells for Minesweeper.

    Attributes:
        rows: The number of rows in the grid.
        cols: The number of columns in the grid.
        cells: A 2D list of Cell objects.
    """

    def __init__(self, rows: int, cols: int) -> None:
        """Initialize a Grid with the given dimensions.

        Args:
            rows: Number of rows in the grid.
            cols: Number of columns in the grid.
        """
        self.rows: int = rows
        self.cols: int = cols
        self.cells: List[List[Cell]] = self._create_empty_grid()

    def _create_empty_grid(self) -> List[List[Cell]]:
        """Create an empty 2D list of Cell objects.

        Returns:
            A 2D list where each element is a Cell in HIDDEN state.
        """
        return [[Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]

    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """Retrieve a cell by its row and column indices.

        Args:
            row: The row index.
            col: The column index.

        Returns:
            The Cell at the given position, or None if out of bounds.
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def reset(self) -> None:
        """Reset all cells to their default state.

        STORY-001-T2: Stub implementation for Grid.reset().
        """
        for r in range(self.rows):
            for c in range(self.cols):
                self.cells[r][c].reset()

    def __repr__(self) -> str:
        """Return a string representation of the Grid.

        Returns:
            A string like 'Grid(9x9)'.
        """
        return f"Grid({self.rows}x{self.cols})"
