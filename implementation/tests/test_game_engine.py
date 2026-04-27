"""Tests for the GameEngine (STORY-005: Cell Interaction).

Tests for:
- Left-click reveal logic
- Right-click flag toggle
- Mine detection and game over
- First-click safety
- Win condition checking
"""

import pytest
from src.core.cell import CellState
from src.core.game import GameEngine


class TestRevealCell:
    """Tests for GameEngine.reveal_cell (STORY-005-T1)."""

    def test_reveal_hidden_cell(self):
        """AC1: Left-click on a hidden cell reveals it."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)  # Place mines before revealing

        result = engine.reveal_cell(5, 5)
        cell = engine.grid.get_cell(5, 5)

        assert result == CellState.REVEALED
        assert cell.state == CellState.REVEALED

    def test_reveal_revealed_cell_does_nothing(self):
        """AC2: Left-click on a revealed cell does nothing."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        engine.reveal_cell(5, 5)
        result = engine.reveal_cell(5, 5)

        assert result == CellState.REVEALED  # Returns current state

    def test_reveal_flagged_cell_does_nothing(self):
        """AC5: Flagged cells cannot be revealed by left-clicking."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        engine.toggle_flag(5, 5)
        result = engine.reveal_cell(5, 5)

        assert result is None

    def test_reveal_mine_triggers_game_over(self):
        """AC3: Left-click on a revealed mine triggers game over."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Find a mine
        mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None
        result = engine.reveal_cell(mine_pos[0], mine_pos[1])

        assert result == CellState.REVEALED
        assert engine.game_over is True

    def test_reveal_out_of_bounds(self):
        """Test that out-of-bounds reveals return None."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        assert engine.reveal_cell(-1, 0) is None
        assert engine.reveal_cell(0, -1) is None
        assert engine.reveal_cell(9, 9) is None

    def test_reveal_after_game_over(self):
        """Test that reveals are blocked after game over."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Find a mine and trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        # Try to reveal another cell
        result = engine.reveal_cell(5, 5)
        assert result is None


class TestToggleFlag:
    """Tests for GameEngine.toggle_flag (STORY-005-T2)."""

    def test_flag_hidden_cell(self):
        """AC4a: Right-click on hidden cell → Flagged."""
        engine = GameEngine(9, 9, 10)

        success = engine.toggle_flag(5, 5)

        assert success is True
        cell = engine.grid.get_cell(5, 5)
        assert cell.state == CellState.FLAGGED
        assert engine.flags_placed == 1

    def test_unflag_flagged_cell(self):
        """AC4b: Right-click on flagged cell → Hidden."""
        engine = GameEngine(9, 9, 10)

        engine.toggle_flag(5, 5)
        success = engine.toggle_flag(5, 5)

        assert success is True
        cell = engine.grid.get_cell(5, 5)
        assert cell.state == CellState.HIDDEN
        assert engine.flags_placed == 0

    def test_flag_revealed_cell_fails(self):
        """Revealed cells cannot be flagged."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        engine.reveal_cell(5, 5)
        success = engine.toggle_flag(5, 5)

        assert success is False

    def test_flag_out_of_bounds_fails(self):
        """Flagging out-of-bounds returns False."""
        engine = GameEngine(9, 9, 10)

        assert engine.toggle_flag(-1, 0) is False
        assert engine.toggle_flag(0, -1) is False
        assert engine.toggle_flag(9, 9) is False

    def test_multiple_flags(self):
        """Test placing and removing multiple flags."""
        engine = GameEngine(9, 9, 10)

        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        engine.toggle_flag(2, 2)

        assert engine.flags_placed == 3

        engine.toggle_flag(1, 1)
        assert engine.flags_placed == 2

    def test_flag_after_game_over_fails(self):
        """Cannot toggle flags after game over."""
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

        assert engine.toggle_flag(5, 5) is False


class TestMineDetection:
    """Tests for mine detection on click (STORY-005-T3)."""

    def test_game_over_mines_revealed(self):
        """AC7: Clicking a mine reveals all mines on the board."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Find and click a mine
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        game_over_mines = engine.get_game_over_mines()
        total_mines = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].is_mine
        )

        assert len(game_over_mines) == total_mines

    def test_game_over_mines_include_all_mine_positions(self):
        """All mine positions are in the game over set."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True  # Prevent double mine placement

        actual_mines = set()
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    actual_mines.add((r, c))

        # Click a mine to trigger game over
        for r, c in actual_mines:
            engine.reveal_cell(r, c)
            break

        game_over_mines = engine.get_game_over_mines()
        assert game_over_mines == actual_mines


class TestFirstClickSafety:
    """Tests for first-click safety mechanism (AC8, STORY-007)."""

    def test_first_click_is_safe(self):
        """AC8: First click is never a mine."""
        engine = GameEngine(9, 9, 10)

        # Before first click, no mines should be placed
        assert engine.first_click_done is False

        # Reveal a cell (this triggers mine placement)
        engine.reveal_cell(4, 4)

        assert engine.first_click_done is True
        cell = engine.grid.get_cell(4, 4)

        # The clicked cell should not be a mine
        assert cell.is_mine is False

    def test_first_click_neighbors_are_safe(self):
        """First click and all 8 neighbors are safe."""
        engine = GameEngine(9, 9, 10)

        engine.reveal_cell(4, 4)

        # Check the clicked cell and all neighbors
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 4 + dr, 4 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False

    def test_mines_placed_after_first_click(self):
        """Mines are placed on the grid after first click."""
        engine = GameEngine(9, 9, 10)

        # Before first click, no mines should be placed
        mine_count_before = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].is_mine
        )
        assert mine_count_before == 0

        # After first click, mines should be placed
        engine.reveal_cell(4, 4)

        mine_count_after = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].is_mine
        )
        assert mine_count_after == engine.total_mines


class TestWinCondition:
    """Tests for win condition checking (STORY-005/STORY-008)."""

    def test_no_win_with_revealed_cell(self):
        """No win when not all safe cells are revealed."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        engine.reveal_cell(4, 4)
        result = engine.check_win_condition()

        assert result is False
        assert engine.game_won is False

    def test_win_all_safe_revealed(self):
        """Win when all non-mine cells are revealed."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(0, 0)
        engine.first_click_done = True  # Prevent double mine placement

        # Find the mine position
        mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        # Reveal all non-mine cells
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if (r, c) != mine_pos:
                    engine.reveal_cell(r, c)

        result = engine.check_win_condition()

        assert result is True
        assert engine.game_won is True
        assert engine.game_over is True

    def test_no_win_after_game_over(self):
        """Win check returns False after game over."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(0, 0)

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        result = engine.check_win_condition()
        assert result is False


class TestReset:
    """Tests for game reset functionality."""

    def test_reset_clears_game_state(self):
        """Reset clears game_over and game_won flags."""
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

        engine.reset()

        assert engine.game_over is False
        assert engine.game_won is False
        assert engine.flags_placed == 0
        assert engine.first_click_done is False

    def test_reset_clears_flags(self):
        """Reset clears all flags."""
        engine = GameEngine(9, 9, 10)

        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        engine.toggle_flag(2, 2)

        assert engine.flags_placed == 3

        engine.reset()

        assert engine.flags_placed == 0
        # All cells should be back to HIDDEN
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                assert engine.grid.cells[r][c].state == CellState.HIDDEN


class TestAdjacentMineCount:
    """Tests for adjacent mine count functionality."""

    def test_adjacent_mine_count_center(self):
        """Adjacent mine count for center cell."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        count = engine.get_adjacent_mine_count(4, 4)
        assert isinstance(count, int)
        assert 0 <= count <= 8

    def test_adjacent_mine_count_corner(self):
        """Adjacent mine count for corner cell (fewer neighbors)."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        count = engine.get_adjacent_mine_count(0, 0)
        assert isinstance(count, int)
        assert 0 <= count <= 3

    def test_adjacent_mine_count_out_of_bounds(self):
        """Out-of-bounds returns 0."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        assert engine.get_adjacent_mine_count(-1, -1) == 0
        assert engine.get_adjacent_mine_count(9, 9) == 0
        assert engine.get_adjacent_mine_count(-1, 5) == 0

    def test_adjacent_mine_count_matches_cell(self):
        """Adjacent mine count matches the cell's stored value."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                count = engine.get_adjacent_mine_count(r, c)
                cell = engine.grid.get_cell(r, c)
                assert count == cell.adjacent_mines
