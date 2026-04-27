"""Minesweeper - Game engine.

STORY-001-T2: Initialize Python project with __init__.py files and base modules.
Orchestrates game state, mine placement, and win/loss detection.
"""

from __future__ import annotations

from typing import Optional, Tuple

from src.core.cell import CellState
from src.core.grid import Grid


class GameEngine:
    """Orchestrates the Minesweeper game logic.

    Attributes:
        grid: The game grid containing all cells.
        total_mines: The total number of mines on the board.
        flags_placed: The current number of flags placed by the player.
        game_over: Whether the game has ended.
        game_won: Whether the player has won the game.
    """

    def __init__(self, rows: int, cols: int, total_mines: int) -> None:
        """Initialize the GameEngine.

        Args:
            rows: Number of rows in the grid.
            cols: Number of columns in the grid.
            total_mines: Total number of mines to place.
        """
        self.grid: Grid = Grid(rows, cols)
        self.total_mines: int = total_mines
        self.flags_placed: int = 0
        self.game_over: bool = False
        self.game_won: bool = False

    def reset(self) -> None:
        """Reset the game to its initial state.

        STORY-001-T2: Stub implementation for GameEngine.reset().
        """
        self.grid.reset()
        self.flags_placed = 0
        self.game_over = False
        self.game_won = False

    def place_mines(self, exclude_row: int, exclude_col: int) -> None:
        """Place mines on the grid, excluding the first-click position and its neighbors.

        Mines are placed randomly, avoiding the cell at (exclude_row, exclude_col)
        and all of its 8 neighbors to ensure the first click is always safe.

        Args:
            exclude_row: Row index to exclude from mine placement.
            exclude_col: Column index to exclude from mine placement.
        """
        import random

        # Build the set of excluded positions (first click + neighbors)
        excluded = set()
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = exclude_row + dr, exclude_col + dc
                if 0 <= nr < self.grid.rows and 0 <= nc < self.grid.cols:
                    excluded.add((nr, nc))

        # Collect all valid positions for mine placement
        valid_positions = []
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                if (r, c) not in excluded:
                    valid_positions.append((r, c))

        # Ensure we don't try to place more mines than available positions
        num_mines = min(self.total_mines, len(valid_positions))

        # Randomly select positions for mines
        selected_positions = random.sample(valid_positions, num_mines)
        for r, c in selected_positions:
            self.grid.cells[r][c].is_mine = True

        # Calculate adjacent mine counts for all cells
        self._calculate_adjacent_mine_counts()
    def reveal_cell(self, row: int, col: int) -> Optional[CellState]:
        """Reveal a cell at the given position.

        Args:
            row: Row index of the cell to reveal.
            col: Column index of the cell to reveal.

        Returns:
            The new state of the cell after revealing, or None if invalid.

        STORY-001-T2: Stub implementation for GameEngine.reveal_cell().
        """
        # TODO: Implement cell reveal logic (STORY-005)
        return None

    def toggle_flag(self, row: int, col: int) -> bool:
        """Toggle the flag state of a cell.

        Args:
            row: Row index of the cell.
            col: Column index of the cell.

        Returns:
            True if the flag was toggled successfully, False otherwise.

        STORY-001-T2: Stub implementation for GameEngine.toggle_flag().
        """
        # TODO: Implement flag toggling (STORY-005)
        return False

    def check_win_condition(self) -> bool:
        """Check if the player has won the game.

        Returns:
            True if all non-mine cells are revealed, False otherwise.

        STORY-001-T2: Stub implementation for GameEngine.check_win_condition().
        """
        # TODO: Implement win condition check (STORY-008)
        return False

    def get_adjacent_mine_count(self, row: int, col: int) -> int:
        """Get the number of adjacent mines for a cell.

        Args:
            row: Row index of the cell.
            col: Column index of the cell.

        Returns:
            The count of mines in the 8 neighboring cells, or 0 if out of bounds.
        """
        cell = self.grid.get_cell(row, col)
        if cell is None:
            return 0
        return cell.adjacent_mines

    def _calculate_adjacent_mine_counts(self) -> None:
        """Calculate adjacent mine counts for all cells on the grid."""
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                self.grid.cells[r][c].adjacent_mines = self.get_adjacent_mine_count(r, c)

