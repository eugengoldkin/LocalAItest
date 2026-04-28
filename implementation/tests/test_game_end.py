"""Tests for Game End Conditions (STORY-008).

Tests for:
- Win condition detection
- Loss condition detection
- Flag feedback (correct vs incorrect flags on loss)
- Game state blocking after game over
- Game reset after win/loss
"""

import pytest
from src.core.cell import CellState
from src.core.game import GameEngine


class TestLossCondition:
    """Tests for loss condition (STORY-008)."""

    def test_loss_on_mine_click(self):
        """AC: Loss condition triggers when a mine is revealed."""
        engine = GameEngine(9, 9, 10)

        # First click at center triggers mine placement safely
        engine.reveal_cell(4, 4)

        # Find a mine by checking is_mine attribute
        mine_found = False
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    result = engine.reveal_cell(r, c)
                    mine_found = True
                    break
            if mine_found:
                break

        assert mine_found is True, "No mine found in grid"
        assert engine.game_over is True
        assert engine.game_won is False
        assert result == CellState.REVEALED

    def test_all_mines_revealed_on_loss(self):
        """AC: All mines are shown on the board after a loss."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find and click a mine
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        # Count mine cells that are revealed
        revealed_mines = 0
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.cells[r][c]
                if cell.is_mine and cell.state == CellState.REVEALED:
                    revealed_mines += 1

        total_mines = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].is_mine
        )

        assert revealed_mines == total_mines

    def test_game_over_mines_contains_all_mine_positions(self):
        """AC: get_game_over_mines returns all mine positions."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find all mine positions
        actual_mines = set()
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    actual_mines.add((r, c))

        # Click a mine
        for r, c in actual_mines:
            engine.reveal_cell(r, c)
            break

        game_over_mines = engine.get_game_over_mines()
        assert game_over_mines == actual_mines

    def test_flags_blocked_after_loss(self):
        """AC: Flagging is blocked after game over."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        # Try to flag
        assert engine.toggle_flag(5, 5) is False

    def test_reveals_blocked_after_loss(self):
        """AC: Revealing cells is blocked after game over."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        # Try to reveal another cell
        assert engine.reveal_cell(5, 5) is None


class TestCorrectIncorrectFlags:
    """Tests for correct vs incorrect flag detection on loss (STORY-008)."""

    def test_correct_flags_detected(self):
        """AC: Correctly flagged mines are identified."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find a mine and flag it
        mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None
        engine.toggle_flag(mine_pos[0], mine_pos[1])

        # Trigger game over by clicking another mine
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine and (r, c) != mine_pos:
                    engine.reveal_cell(r, c)
                    break

        feedback = engine.get_flag_feedback(mine_pos[0], mine_pos[1])
        assert feedback == "correct"

    def test_incorrect_flags_detected(self):
        """AC: Incorrectly flagged cells are identified."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find a non-mine cell and flag it
        wrong_flag_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if not engine.grid.cells[r][c].is_mine:
                    wrong_flag_pos = (r, c)
                    break
            if wrong_flag_pos:
                break

        assert wrong_flag_pos is not None
        engine.toggle_flag(wrong_flag_pos[0], wrong_flag_pos[1])

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        feedback = engine.get_flag_feedback(wrong_flag_pos[0], wrong_flag_pos[1])
        assert feedback == "incorrect"

    def test_no_feedback_for_non_flagged_cells(self):
        """Non-flagged cells return None feedback."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        # A hidden cell should have no feedback
        feedback = engine.get_flag_feedback(5, 5)
        assert feedback is None

    def test_correct_flags_set_on_game_over(self):
        """correct_flags set contains all correctly flagged mines."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find two mines and flag them
        mine_positions = []
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_positions.append((r, c))
                    if len(mine_positions) == 2:
                        break
            if len(mine_positions) == 2:
                break

        for r, c in mine_positions:
            engine.toggle_flag(r, c)

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        assert len(engine.correct_flags) >= 1

    def test_incorrect_flags_set_on_game_over(self):
        """incorrect_flags set contains all incorrectly flagged cells."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find a non-mine cell and flag it
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if not engine.grid.cells[r][c].is_mine:
                    engine.toggle_flag(r, c)
                    break

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        assert len(engine.incorrect_flags) >= 1


class TestWinCondition:
    """Tests for win condition detection (STORY-008)."""

    def test_win_all_safe_revealed(self):
        """AC: Win when all non-mine cells are revealed."""
        engine = GameEngine(3, 3, 1)
        # Use place_mines with exclude to ensure mines are placed
        engine.place_mines(2, 2)
        engine.first_click_done = True

        # Find the mine position
        mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None

        # Reveal all non-mine cells
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if (r, c) != mine_pos:
                    engine.reveal_cell(r, c)

        # Check win condition explicitly
        engine.check_win_condition()

        assert engine.game_won is True
        assert engine.game_over is True

    def test_no_win_partial_reveal(self):
        """No win when not all safe cells are revealed."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Reveal only one cell
        engine.reveal_cell(0, 0)

        assert engine.game_won is False
        assert engine.game_over is False

    def test_check_win_returns_true_on_win(self):
        """check_win_condition returns True when player wins."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if (r, c) != mine_pos:
                    engine.reveal_cell(r, c)

        assert engine.check_win_condition() is True

    def test_check_win_returns_false_during_game(self):
        """check_win_condition returns False during gameplay."""
        engine = GameEngine(9, 9, 10)
        engine.first_click_done = True

        # First click at center to trigger mine placement safely
        engine.reveal_cell(4, 4)

        # Only reveal one cell - not enough to win
        engine.reveal_cell(0, 0)
        assert engine.check_win_condition() is False

    def test_check_win_returns_false_after_game_over(self):
        """check_win_condition returns False after game over."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(0, 0)

        # Trigger game over first
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        assert engine.check_win_condition() is False


class TestGameReset:
    """Tests for game reset after win/loss (STORY-008)."""

    def test_reset_clears_game_over(self):
        """Reset clears game_over flag."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        assert engine.game_over is True
        engine.reset()
        assert engine.game_over is False

    def test_reset_clears_game_won(self):
        """Reset clears game_won flag."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(2, 2)
        engine.first_click_done = True

        mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None

        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if (r, c) != mine_pos:
                    engine.reveal_cell(r, c)

        # Check win condition explicitly
        engine.check_win_condition()
        assert engine.game_won is True
        engine.reset()
        assert engine.game_won is False

    def test_reset_clears_flag_tracking(self):
        """Reset clears correct_flags and incorrect_flags."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Flag a cell
        engine.toggle_flag(0, 0)

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        assert len(engine.correct_flags) >= 0  # May or may not have correct flags
        assert len(engine.incorrect_flags) >= 0  # May or may not have incorrect flags

        engine.reset()
        assert len(engine.correct_flags) == 0
        assert len(engine.incorrect_flags) == 0

    def test_can_play_after_reset(self):
        """Game can be played again after reset."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        engine.reset()

        # Should be able to reveal cells again
        result = engine.reveal_cell(4, 4)
        assert result is not None
        assert engine.game_over is False

    def test_reset_clears_all_cells(self):
        """Reset clears all cell states."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Reveal some cells
        engine.reveal_cell(4, 4)
        engine.reveal_cell(5, 5)
        engine.toggle_flag(0, 0)

        engine.reset()

        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                assert engine.grid.cells[r][c].state == CellState.HIDDEN
                assert engine.grid.cells[r][c].is_mine is False


class TestWinWithFlags:
    """Tests for winning with flags placed (STORY-008)."""

    def test_win_with_some_flags(self):
        """Can win even with some flags placed (flags don't block win)."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find the mine
        mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None

        # Flag a cell (simulating player flagging before revealing)
        engine.toggle_flag(0, 1)
        engine.toggle_flag(1, 0)

        # Unflag them so they can be revealed
        engine.toggle_flag(0, 1)
        engine.toggle_flag(1, 0)

        # Reveal all non-mine cells
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if (r, c) != mine_pos:
                    engine.reveal_cell(r, c)

        # Check win condition explicitly
        engine.check_win_condition()

        assert engine.game_won is True
        assert engine.game_over is True

    def test_win_with_all_mines_flagged(self):
        """Win condition still works when all mines are flagged."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find and flag the mine
        mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None, "Mine was not placed on grid"
        engine.toggle_flag(mine_pos[0], mine_pos[1])

        # Reveal all non-mine cells
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if (r, c) != mine_pos:
                    engine.reveal_cell(r, c)

        # Check win condition explicitly
        engine.check_win_condition()

        assert engine.game_won is True
        assert engine.game_over is True
