"""Minesweeper - Game engine.

STORY-005: Implement cell interaction mechanics (reveal, flag, game over).
STORY-006: Implement flood fill for empty cells (0 adjacent mines).
STORY-007: First-click safety (mine placement after first click).
STORY-008: Win/loss detection.
STORY-009: Timer (starts on first click, stops on game end, MM:SS format).

Orchestrates game state, mine placement, and win/loss detection.
"""

from __future__ import annotations

import random
import time
from collections import deque
from typing import Deque, List, Optional, Set, Tuple

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
        first_click_done: Whether the first click has occurred (mines placed).
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
        self.first_click_done: bool = False
        # STORY-009: Timer state
        self.timer_running: bool = False
        self.elapsed_time: int = 0
        self._start_time: float = 0.0
        self._game_over_mines: Set[Tuple[int, int]] = set()
        # STORY-008: Track correct and incorrect flags on game over
        self.correct_flags: Set[Tuple[int, int]] = set()
        self.incorrect_flags: Set[Tuple[int, int]] = set()

    # STORY-009: Maximum timer value (999 seconds = 16:39)
    MAX_TIME: int = 999

    # STORY-009: Timer Methods

    def _start_timer(self) -> None:
        """Start the game timer.

        STORY-009: Timer starts on first click.
        """
        if not self.timer_running:
            self.timer_running = True
            self._start_time = time.time()

    def _stop_timer(self) -> None:
        """Stop the game timer and calculate final elapsed time.

        STORY-009: Timer stops when game ends (win or loss).
        """
        if self.timer_running:
            # Calculate elapsed time since start
            elapsed = int(time.time() - self._start_time)
            self.elapsed_time = min(elapsed, self.MAX_TIME)
            self.timer_running = False

    def _update_timer(self) -> int:
        """Update and return the current elapsed time.

        STORY-009: Updates timer at least once per second.
        Returns the current elapsed time in seconds, capped at MAX_TIME.

        Returns:
            Current elapsed time in seconds (0 if timer not running).
        """
        if self.timer_running:
            elapsed = int(time.time() - self._start_time)
            self.elapsed_time = min(elapsed, self.MAX_TIME)
        return self.elapsed_time

    def get_formatted_time(self) -> str:
        """Format the elapsed time as MM:SS.

        STORY-009: Format time as MM:SS (e.g., 01:23, 16:39).
        Maximum value is 999 seconds (16:39).

        Returns:
            Formatted time string in MM:SS format.
        """
        current_time = self._update_timer()
        minutes = current_time // 60
        seconds = current_time % 60
        return f"{minutes:02d}:{seconds:02d}"

    def get_elapsed_time(self) -> int:
        """Get the current elapsed time in seconds.

        STORY-009: Returns current elapsed time, updating if timer is running.

        Returns:
            Elapsed time in seconds (capped at 999).
        """
        return self._update_timer()

    def reset(self) -> None:
        """Reset the game to its initial state.

        STORY-005: Reset clears game state so a new game can start.
        STORY-009: Also resets the timer.
        """
        self.grid.reset()
        self.flags_placed = 0
        self.game_over = False
        self.game_won = False
        self.first_click_done = False
        # STORY-009: Reset timer
        self.timer_running = False
        self.elapsed_time = 0
        self._start_time = 0.0
        self._game_over_mines = set()
        # STORY-008: Clear flag tracking
        self.correct_flags = set()
        self.incorrect_flags = set()

    def place_mines(self, exclude_row: int, exclude_col: int) -> None:
        """Place mines on the grid, excluding the first-click position and its neighbors.

        Mines are placed randomly, avoiding the cell at (exclude_row, exclude_col)
        and all of its 8 neighbors to ensure the first click is always safe.

        Args:
            exclude_row: Row index to exclude from mine placement.
            exclude_col: Column index to exclude from mine placement.
        """
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

        STORY-005-T1: Left-click event handler for revealing cells.
        - Left-click on a hidden cell reveals it.
        - Left-click on a revealed cell does nothing.
        - Left-click on a flagged cell does nothing.
        - If the cell is a mine, triggers game over.
        - First click triggers mine placement (first-click safety).

        Args:
            row: Row index of the cell to reveal.
            col: Column index of the cell to reveal.

        Returns:
            The new state of the cell after revealing, or None if invalid.
        """
        # Check if game is already over
        if self.game_over:
            return None

        cell = self.grid.get_cell(row, col)
        if cell is None:
            return None

        # Left-click on a revealed cell does nothing (AC2)
        if cell.state == CellState.REVEALED:
            return cell.state

        # Flagged cells cannot be revealed by left-clicking (AC5)
        if cell.state == CellState.FLAGGED:
            return None

        # First click safety: generate mines after first click (AC8, STORY-007)
        if not self.first_click_done:
            self.place_mines(row, col)
            self.first_click_done = True
            # STORY-009: Start timer on first click
            self._start_timer()

        # Cell must be hidden to reveal it
        if cell.state != CellState.HIDDEN:
            return None

        # Reveal the cell
        cell.state = CellState.REVEALED

        # Check if the revealed cell is a mine (AC3, AC7)
        if cell.is_mine:
            self.game_over = True
            self._reveal_all_mines()
            # STORY-009: Stop timer on game over (loss)
            self._stop_timer()
            return cell.state

        # STORY-006: Flood fill for cells with 0 adjacent mines
        if cell.adjacent_mines == 0:
            self._flood_fill(row, col)

        return cell.state

    def toggle_flag(self, row: int, col: int) -> bool:
        """Toggle the flag state of a cell.

        STORY-005-T2: Right-click event handler for toggling flags.
        - Right-click on a hidden cell → Flagged
        - Right-click on a flagged cell → Hidden
        - Revealed cells cannot be flagged

        Args:
            row: Row index of the cell.
            col: Column index of the cell.

        Returns:
            True if the flag was toggled successfully, False otherwise.
        """
        # Cannot toggle flags if game is over
        if self.game_over:
            return False

        cell = self.grid.get_cell(row, col)
        if cell is None:
            return False

        # Only hidden cells can be flagged
        if cell.state == CellState.HIDDEN:
            cell.state = CellState.FLAGGED
            self.flags_placed += 1
            return True
        elif cell.state == CellState.FLAGGED:
            cell.state = CellState.HIDDEN
            self.flags_placed -= 1
            return True

        # Revealed cells cannot be flagged
        return False

    def check_win_condition(self) -> bool:
        """Check if the player has won the game.

        STORY-005/STORY-008: Win condition check.
        The player wins when all non-mine cells are revealed.

        Returns:
            True if all non-mine cells are revealed, False otherwise.
        """
        if self.game_over:
            return False

        revealed_count = 0
        total_cells = self.grid.rows * self.grid.cols
        non_mine_cells = total_cells - self.total_mines

        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell = self.grid.cells[r][c]
                if cell.state == CellState.REVEALED and not cell.is_mine:
                    revealed_count += 1

        if revealed_count == non_mine_cells:
            self.game_won = True
            self.game_over = True
            # STORY-009: Stop timer on win
            self._stop_timer()
            return True

        return False

    def get_flag_feedback(self, row: int, col: int) -> Optional[str]:
        """Get the visual feedback for a flagged cell on game over.

        STORY-008: Determines if a flagged cell is correct or incorrect.

        Args:
            row: Row index of the cell.
            col: Column index of the cell.

        Returns:
            "correct" if the cell is a correctly flagged mine,
            "incorrect" if the cell is incorrectly flagged,
            None if the cell is not flagged.
        """
        if (row, col) in self.correct_flags:
            return "correct"
        elif (row, col) in self.incorrect_flags:
            return "incorrect"
        return None

    def get_game_over_mines(self) -> Set[Tuple[int, int]]:
        """Get the set of mine positions revealed on game over.

        STORY-005-T3: Mine detection on click (game over condition).
        Returns the positions of all mines that should be revealed.

        Returns:
            Set of (row, col) tuples for all mine positions.
        """
        return self._game_over_mines

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
                self.grid.cells[r][c].adjacent_mines = self._count_adjacent_mines(r, c)

    def _count_adjacent_mines(self, row: int, col: int) -> int:
        """Count the number of mines adjacent to the cell at (row, col).

        Args:
            row: Row index of the cell.
            col: Column index of the cell.

        Returns:
            The count of mines in the 8 neighboring cells.
        """
        count = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                cell = self.grid.get_cell(nr, nc)
                if cell is not None and cell.is_mine:
                    count += 1
        return count

    def chord(self, row: int, col: int) -> bool:
        """Chord on a revealed numbered cell.

        STORY-013: When a numbered cell has the correct number of flags around it,
        clicking it reveals all remaining unflagged neighbors.

        - Right-click on a revealed numbered cell triggers chording
        - Chording only activates when the number of adjacent flags matches the cell's mine count
        - All unflagged neighbors are revealed when chording activates
        - If chording triggers a mine, the game ends (loss)
        - If chording triggers flood fill (0 adjacent mines), flood fill is applied
        - Chording does nothing if the flag count doesn't match the cell's mine count
        - Chording is disabled during game over states

        Args:
            row: Row index of the cell to chord.
            col: Column index of the cell to chord.

        Returns:
            True if chording was performed, False otherwise.
        """
        # Chording is disabled during game over states
        if self.game_over:
            return False

        cell = self.grid.get_cell(row, col)
        if cell is None:
            return False

        # Only revealed numbered cells can be chored
        if cell.state != CellState.REVEALED or cell.adjacent_mines == 0:
            return False

        # Count adjacent flags
        adjacent_flags = self._count_adjacent_flags(row, col)

        # Chording does nothing if the flag count doesn't match the cell's mine count
        if adjacent_flags != cell.adjacent_mines:
            return False

        # Reveal all unflagged neighbors
        neighbors_revealed = False
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                neighbor = self.grid.get_cell(nr, nc)
                if neighbor is not None and neighbor.state == CellState.HIDDEN:
                    # Reveal the neighbor
                    if neighbor.is_mine:
                        # If chording triggers a mine, the game ends (loss)
                        neighbor.state = CellState.REVEALED
                        self.game_over = True
                        self._reveal_all_mines()
                        # STORY-009: Stop timer on game over (loss)
                        self._stop_timer()
                        return True
                    else:
                        neighbor.state = CellState.REVEALED
                        neighbors_revealed = True
                        # If chording triggers flood fill (0 adjacent mines), flood fill is applied
                        if neighbor.adjacent_mines == 0:
                            self._flood_fill(nr, nc)

        return neighbors_revealed

    def _count_adjacent_flags(self, row: int, col: int) -> int:
        """Count the number of flags adjacent to the cell at (row, col).

        Args:
            row: Row index of the cell.
            col: Column index of the cell.

        Returns:
            The count of flagged neighboring cells.
        """
        count = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                neighbor = self.grid.get_cell(nr, nc)
                if neighbor is not None and neighbor.state == CellState.FLAGGED:
                    count += 1
        return count

    def _reveal_all_mines(self) -> None:
        """Reveal all mines on the board for game over display.

        STORY-005-T3: Clicking a mine reveals all mines on the board.
        Mines that are not flagged are revealed as mines.
        STORY-008: Track correct and incorrect flags for visual feedback.
        """
        self._game_over_mines = set()
        self.correct_flags = set()
        self.incorrect_flags = set()
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell = self.grid.cells[r][c]
                if cell.is_mine:
                    self._game_over_mines.add((r, c))
                    if cell.state != CellState.FLAGGED:
                        cell.state = CellState.REVEALED
                # STORY-008: Track incorrectly flagged cells (flags on non-mines)
                elif cell.state == CellState.FLAGGED:
                    self.incorrect_flags.add((r, c))

        # STORY-008: Mark correctly flagged mines
        for mine_r, mine_c in self._game_over_mines:
            cell = self.grid.get_cell(mine_r, mine_c)
            if cell is not None and cell.state == CellState.FLAGGED:
                self.correct_flags.add((mine_r, mine_c))

    # STORY-006: Flood Fill Implementation

    def _flood_fill(self, start_row: int, start_col: int) -> None:
        """Iterative flood fill to reveal empty cells and their boundaries.

        Uses a BFS (Breadth-First Search) approach with a deque to avoid
        stack overflow on large grids.

        When a cell with 0 adjacent mines is revealed, all adjacent cells
        are recursively revealed. This process continues until cells with
        non-zero mine counts are reached.

        Flood fill:
        - Only reveals hidden cells (not flagged cells)
        - Stops at grid boundaries
        - Stops at cells with non-zero adjacent mine counts (they are revealed
          but not expanded further)
        - Does not run during game over

        Args:
            start_row: Row index of the starting cell (must have 0 adjacent mines).
            start_col: Column index of the starting cell.
        """
        # Don't flood fill during game over
        if self.game_over:
            return

        # Use a deque for iterative BFS to avoid stack overflow
        queue: Deque[Tuple[int, int]] = deque()
        queue.append((start_row, start_col))

        # Track visited cells to avoid infinite loops
        visited: Set[Tuple[int, int]] = set()

        while queue:
            row, col = queue.popleft()

            # Skip if already visited
            if (row, col) in visited:
                continue
            visited.add((row, col))

            cell = self.grid.get_cell(row, col)
            if cell is None:
                continue

            # Skip flagged cells (AC5: Flood fill does not reveal flagged cells)
            if cell.state == CellState.FLAGGED:
                continue

            # Reveal the cell (only if it's hidden)
            if cell.state == CellState.HIDDEN:
                cell.state = CellState.REVEALED

            # If this cell has 0 adjacent mines, continue flood fill to neighbors
            if cell.adjacent_mines == 0:
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc
                        if (nr, nc) not in visited:
                            neighbor = self.grid.get_cell(nr, nc)
                            if (
                                neighbor is not None
                                and neighbor.state == CellState.HIDDEN
                            ):
                                queue.append((nr, nc))
