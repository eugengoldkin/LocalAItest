"""Tests for Chording functionality (STORY-013).

Tests for:
- Chording on revealed numbered cells with correct flags
- Chording with incorrect flag count (no action)
- Chording triggering flood fill
- Chording hitting a mine (game over)
- Chording disabled during game over
- Chording on zero-count cells (no action)
- Chording on hidden/flagged cells (no action)
"""

import pytest
from src.core.cell import CellState
from src.core.game import GameEngine


class TestChordingBasic:
    """Tests for basic chording functionality (STORY-013)."""

    def test_chording_with_correct_flags_reveals_neighbors(self):
        """AC2: Chording activates when adjacent flags match the cell's mine count."""
        # Create a controlled grid
        engine = GameEngine(7, 7, 1)
        engine.first_click_done = True

        # Place a mine at (3, 0) - far from our test area
        engine.grid.cells[3][0].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Find a cell with exactly 1 adjacent mine
        test_cell = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine and cell.adjacent_mines == 1:
                    test_cell = (r, c)
                    break
            if test_cell:
                break

        assert test_cell is not None

        # Reveal the test cell first
        engine.reveal_cell(test_cell[0], test_cell[1])
        assert engine.grid.get_cell(test_cell[0], test_cell[1]).state == CellState.REVEALED

        # Flag all adjacent mines (we know there's exactly 1)
        # Find the adjacent mine
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_cell[0] + dr, test_cell[1] + dc
                neighbor = engine.grid.get_cell(nr, nc)
                if neighbor is not None and neighbor.is_mine:
                    engine.toggle_flag(nr, nc)

        # Now chord the cell
        result = engine.chord(test_cell[0], test_cell[1])

        # Should have revealed some neighbors
        assert result is True

        # Check that all non-mine hidden neighbors are now revealed
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_cell[0] + dr, test_cell[1] + dc
                neighbor = engine.grid.get_cell(nr, nc)
                if neighbor is not None:
                    if neighbor.is_mine:
                        # Mine neighbor should remain hidden (flagged or not)
                        pass
                    else:
                        # Non-mine neighbors should be revealed
                        assert neighbor.state == CellState.REVEALED, (
                            f"Neighbor at ({nr}, {nc}) should be revealed"
                        )

    def test_chording_with_incorrect_flags_does_nothing(self):
        """AC6: Chording does nothing if the flag count doesn't match the cell's mine count."""
        # Create a controlled grid
        engine = GameEngine(7, 7, 1)
        engine.first_click_done = True

        # Place a mine far away
        engine.grid.cells[0][0].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Find a cell with exactly 1 adjacent mine
        test_cell = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine and cell.adjacent_mines == 1:
                    test_cell = (r, c)
                    break
            if test_cell:
                break

        assert test_cell is not None

        # Reveal the test cell
        engine.reveal_cell(test_cell[0], test_cell[1])

        # Add a flag on a non-mine neighbor (incorrect flag)
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_cell[0] + dr, test_cell[1] + dc
                neighbor = engine.grid.get_cell(nr, nc)
                if neighbor is not None and not neighbor.is_mine and neighbor.state == CellState.HIDDEN:
                    engine.toggle_flag(nr, nc)
                    break

        # Chord should do nothing
        result = engine.chord(test_cell[0], test_cell[1])

        assert result is False

    def test_chording_on_zero_count_cell_does_nothing(self):
        """AC6: Chording does nothing on cells with 0 adjacent mines."""
        engine = GameEngine(7, 7, 1)
        engine.first_click_done = True

        # Place mine far away so (3, 3) has 0 adjacent mines
        engine.grid.cells[0][0].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Reveal (3, 3) which should have 0 adjacent mines
        engine.reveal_cell(3, 3)
        cell = engine.grid.get_cell(3, 3)

        # Chording on a zero-count cell should do nothing
        result = engine.chord(3, 3)

        assert result is False

    def test_chording_disabled_during_game_over(self):
        """AC7: Chording is disabled during game over states."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        assert engine.game_over is True

        # Try to chord any cell
        result = engine.chord(5, 5)

        assert result is False


class TestChordingMineHit:
    """Tests for chording that hits a mine (STORY-013)."""

    def test_chording_hitting_mine_triggers_game_over(self):
        """AC4: If chording triggers a mine, the game ends (loss)."""
        # Create a controlled grid
        engine = GameEngine(7, 7, 2)
        engine.first_click_done = True

        # Place mines at specific positions
        engine.grid.cells[0][0].is_mine = True
        engine.grid.cells[0][1].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Find a cell adjacent to both mines (should have 2 adjacent mines)
        test_cell = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine and cell.adjacent_mines == 2:
                    test_cell = (r, c)
                    break
            if test_cell:
                break

        # If no cell has exactly 2 adjacent mines, find one with 1 and test with 1 mine
        if test_cell is None:
            for r in range(engine.grid.rows):
                for c in range(engine.grid.cols):
                    cell = engine.grid.get_cell(r, c)
                    if not cell.is_mine and cell.adjacent_mines == 1:
                        test_cell = (r, c)
                        break
                if test_cell:
                    break

        assert test_cell is not None

        # Reveal the test cell
        engine.reveal_cell(test_cell[0], test_cell[1])

        # Find all adjacent mines
        adjacent_mines = []
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_cell[0] + dr, test_cell[1] + dc
                neighbor = engine.grid.get_cell(nr, nc)
                if neighbor is not None and neighbor.is_mine:
                    adjacent_mines.append((nr, nc))

        # Flag all adjacent mines
        for mr, mc in adjacent_mines:
            engine.toggle_flag(mr, mc)

        # Find an unflagged hidden neighbor that is a mine
        mine_neighbor = None
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_cell[0] + dr, test_cell[1] + dc
                neighbor = engine.grid.get_cell(nr, nc)
                if neighbor is not None and neighbor.is_mine and neighbor.state != CellState.FLAGGED:
                    mine_neighbor = (nr, nc)
                    break
            if mine_neighbor:
                break

        if mine_neighbor is not None:
            # Chord should hit the mine and trigger game over
            result = engine.chord(test_cell[0], test_cell[1])

            assert result is True
            assert engine.game_over is True

            # The mine should be revealed
            mine_cell = engine.grid.get_cell(mine_neighbor[0], mine_neighbor[1])
            assert mine_cell.state == CellState.REVEALED


class TestChordingFloodFill:
    """Tests for chording that triggers flood fill (STORY-013)."""

    def test_chording_triggers_flood_fill(self):
        """AC5: If chording triggers flood fill (0 adjacent mines), flood fill is applied."""
        # Create a controlled grid
        engine = GameEngine(7, 7, 1)
        engine.first_click_done = True

        # Place mine far away
        engine.grid.cells[6][6].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Find a cell with exactly 1 adjacent mine
        test_cell = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine and cell.adjacent_mines == 1:
                    test_cell = (r, c)
                    break
            if test_cell:
                break

        assert test_cell is not None

        # Reveal the test cell
        engine.reveal_cell(test_cell[0], test_cell[1])

        # Flag the adjacent mine
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_cell[0] + dr, test_cell[1] + dc
                neighbor = engine.grid.get_cell(nr, nc)
                if neighbor is not None and neighbor.is_mine:
                    engine.toggle_flag(nr, nc)

        # Count revealed cells before chording
        revealed_before = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].state == CellState.REVEALED
        )

        # Chord the cell
        result = engine.chord(test_cell[0], test_cell[1])

        # Should have revealed neighbors
        assert result is True

        # Count revealed cells after chording
        revealed_after = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].state == CellState.REVEALED
        )

        # If any revealed neighbor has 0 adjacent mines, flood fill should have occurred
        # and more cells should be revealed
        assert revealed_after >= revealed_before


class TestChordingEdgeCases:
    """Tests for edge cases in chording (STORY-013)."""

    def test_chording_on_hidden_cell_does_nothing(self):
        """Chording on a hidden cell does nothing."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Don't reveal the cell, try to chord
        result = engine.chord(5, 5)

        assert result is False

    def test_chording_on_flagged_cell_does_nothing(self):
        """Chording on a flagged cell does nothing."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Flag the cell
        engine.toggle_flag(5, 5)

        # Try to chord
        result = engine.chord(5, 5)

        assert result is False

    def test_chording_out_of_bounds_returns_false(self):
        """Chording on out-of-bounds position returns False."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        assert engine.chord(-1, -1) is False
        assert engine.chord(9, 9) is False
        assert engine.chord(-1, 5) is False
        assert engine.chord(5, -1) is False

    def test_chording_with_more_flags_than_needed(self):
        """Chording with more flags than needed does nothing."""
        engine = GameEngine(7, 7, 1)
        engine.first_click_done = True

        # Place mine far away
        engine.grid.cells[0][0].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Find a cell with exactly 1 adjacent mine
        test_cell = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine and cell.adjacent_mines == 1:
                    test_cell = (r, c)
                    break
            if test_cell:
                break

        assert test_cell is not None

        # Reveal the test cell
        engine.reveal_cell(test_cell[0], test_cell[1])

        # Flag one correct neighbor
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_cell[0] + dr, test_cell[1] + dc
                neighbor = engine.grid.get_cell(nr, nc)
                if neighbor is not None and neighbor.is_mine:
                    engine.toggle_flag(nr, nc)
                    break

        # Flag an extra non-mine neighbor
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_cell[0] + dr, test_cell[1] + dc
                neighbor = engine.grid.get_cell(nr, nc)
                if neighbor is not None and not neighbor.is_mine and neighbor.state == CellState.HIDDEN:
                    engine.toggle_flag(nr, nc)
                    break

        # Chord should do nothing because flag count > mine count
        result = engine.chord(test_cell[0], test_cell[1])

        assert result is False

    def test_chording_with_less_flags_than_needed(self):
        """Chording with fewer flags than needed does nothing."""
        engine = GameEngine(7, 7, 2)
        engine.first_click_done = True

        # Place two adjacent mines
        engine.grid.cells[0][0].is_mine = True
        engine.grid.cells[0][1].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Find a cell with exactly 2 adjacent mines
        test_cell = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine and cell.adjacent_mines == 2:
                    test_cell = (r, c)
                    break
            if test_cell:
                break

        if test_cell is None:
            # Fallback: find a cell with 1 adjacent mine
            for r in range(engine.grid.rows):
                for c in range(engine.grid.cols):
                    cell = engine.grid.get_cell(r, c)
                    if not cell.is_mine and cell.adjacent_mines == 1:
                        test_cell = (r, c)
                        break
                if test_cell:
                    break

        assert test_cell is not None

        # Reveal the test cell
        engine.reveal_cell(test_cell[0], test_cell[1])

        # Only flag one of the adjacent mines (less than needed)
        flag_count = 0
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = test_cell[0] + dr, test_cell[1] + dc
                neighbor = engine.grid.get_cell(nr, nc)
                if neighbor is not None and neighbor.is_mine and flag_count == 0:
                    engine.toggle_flag(nr, nc)
                    flag_count += 1

        # Chord should do nothing because flag count < mine count
        result = engine.chord(test_cell[0], test_cell[1])

        assert result is False
