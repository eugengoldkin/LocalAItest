"""Tests for Win/Loss Visual Feedback (STORY-015).

Tests for:
- Win dialog displays "You Win!" message with elapsed time
- Loss dialog displays "You Lose!" message without time
- GameEndDialog correctly handles elapsed_time parameter
- GridFrame correctly reveals mines on loss
- GridFrame correctly marks incorrect flags on loss
- GridFrame blocks interaction during game over
- MainWindow passes elapsed time to game end dialog
"""

from __future__ import annotations

import tkinter as tk
from unittest.mock import MagicMock, patch

import pytest

from src.core.cell import CellState
from src.core.game import GameEngine
from src.ui.game_end_dialog import GameEndDialog
from src.ui.grid_frame import GridFrame


@pytest.fixture
def root():
    """Create a Tkinter root window for tests."""
    r = tk.Tk()
    r.withdraw()
    yield r
    r.destroy()


class TestWinDialogWithTime:
    """Tests for win dialog displaying elapsed time (STORY-015)."""

    def test_win_dialog_shows_you_win_message(self, root):
        """Win dialog displays 'You Win!' message."""
        dialog = GameEndDialog(root, won=True)
        message = dialog.message_label.cget("text")
        assert message == "You Win!"

    def test_win_dialog_shows_elapsed_time(self, root):
        """Win dialog displays elapsed time."""
        dialog = GameEndDialog(root, won=True, elapsed_time=123)
        assert dialog.time_label is not None
        time_text = dialog.time_label.cget("text")
        assert time_text == "Time: 02:03"

    def test_win_dialog_shows_correct_time_format(self, root):
        """Win dialog formats time as MM:SS."""
        dialog = GameEndDialog(root, won=True, elapsed_time=0)
        assert dialog.time_label.cget("text") == "Time: 00:00"

    def test_win_dialog_one_minute(self, root):
        """Win dialog formats time correctly for one minute."""
        dialog = GameEndDialog(root, won=True, elapsed_time=60)
        assert dialog.time_label.cget("text") == "Time: 01:00"

    def test_win_dialog_sixty_minutes(self, root):
        """Win dialog formats time correctly for sixty minutes."""
        dialog = GameEndDialog(root, won=True, elapsed_time=3600)
        assert dialog.time_label.cget("text") == "Time: 60:00"

    def test_win_dialog_no_time_label_for_loss(self, root):
        """Loss dialog does not display time label."""
        dialog = GameEndDialog(root, won=False, elapsed_time=123)
        assert dialog.time_label is None

    def test_win_dialog_shows_correct_message(self, root):
        """Loss dialog displays 'You Lose!' message."""
        dialog = GameEndDialog(root, won=False)
        message = dialog.message_label.cget("text")
        assert message == "You Lose!"

    def test_win_dialog_default_elapsed_time_zero(self, root):
        """Win dialog defaults elapsed time to 0 when not provided."""
        dialog = GameEndDialog(root, won=True)
        assert dialog.elapsed_time == 0
        assert dialog.time_label is not None
        assert dialog.time_label.cget("text") == "Time: 00:00"

    def test_win_dialog_green_color(self, root):
        """Win dialog uses green color for message."""
        dialog = GameEndDialog(root, won=True)
        assert dialog.message_label.cget("fg") == "#00aa00"

    def test_loss_dialog_red_color(self, root):
        """Loss dialog uses red color for message."""
        dialog = GameEndDialog(root, won=False)
        assert dialog.message_label.cget("fg") == "#cc0000"


class TestGridMineRevealOnLoss:
    """Tests for mine reveal on game loss (STORY-015)."""

    def test_revealed_mine_shows_red_background(self, root):
        """Revealed mines display with red background on loss."""
        engine = GameEngine(rows=3, cols=3, total_mines=1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        grid_frame = GridFrame(root, engine, rows=3, cols=3)

        # Find the mine
        mine_pos = None
        for r in range(3):
            for c in range(3):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None
        engine.grid.get_cell(*mine_pos).state = CellState.REVEALED
        grid_frame.update_cell(*mine_pos)

        btn = grid_frame.cells[mine_pos[0]][mine_pos[1]]
        assert btn["bg"] == "#ff0000"
        assert btn["text"] == "*"
        assert btn["relief"] == tk.SUNKEN

    def test_correctly_flagged_mine_shows_green_on_loss(self, root):
        """Correctly flagged mines show green background on loss."""
        engine = GameEngine(rows=3, cols=3, total_mines=1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        grid_frame = GridFrame(root, engine, rows=3, cols=3)

        # Find and flag a mine
        mine_pos = None
        for r in range(3):
            for c in range(3):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None
        engine.grid.get_cell(*mine_pos).state = CellState.FLAGGED
        engine.game_over = True
        engine.correct_flags.add(mine_pos)

        grid_frame.update_cell(*mine_pos)

        btn = grid_frame.cells[mine_pos[0]][mine_pos[1]]
        assert btn["bg"] == "#00ff00"
        assert btn["text"] == "F"
        assert btn["relief"] == tk.RAISED

    def test_incorrectly_flagged_cell_shows_red_x_on_loss(self, root):
        """Incorrectly flagged cells show red X on loss."""
        engine = GameEngine(rows=3, cols=3, total_mines=1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        grid_frame = GridFrame(root, engine, rows=3, cols=3)

        # Find a non-mine cell
        non_mine_pos = None
        for r in range(3):
            for c in range(3):
                if not engine.grid.cells[r][c].is_mine:
                    non_mine_pos = (r, c)
                    break
            if non_mine_pos:
                break

        assert non_mine_pos is not None
        engine.grid.get_cell(*non_mine_pos).state = CellState.FLAGGED
        engine.game_over = True
        engine.incorrect_flags.add(non_mine_pos)

        grid_frame.update_cell(*non_mine_pos)

        btn = grid_frame.cells[non_mine_pos[0]][non_mine_pos[1]]
        assert btn["bg"] == "#ff6666"
        assert btn["text"] == "X"
        assert btn["fg"] == "red"
        assert btn["relief"] == tk.SUNKEN


class TestGridInteractionBlocking:
    """Tests for blocking interaction during game over (STORY-015)."""

    def test_left_click_blocked_on_game_over(self):
        """Left-click does nothing when game is over."""
        engine = GameEngine(rows=3, cols=3, total_mines=1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Trigger game over
        for r in range(3):
            for c in range(3):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        assert engine.game_over is True

        # Try to reveal another cell
        result = engine.reveal_cell(1, 1)
        assert result is None

    def test_right_click_blocked_on_game_over(self):
        """Right-click (flagging) does nothing when game is over."""
        engine = GameEngine(rows=3, cols=3, total_mines=1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Trigger game over
        for r in range(3):
            for c in range(3):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break

        assert engine.game_over is True

        # Try to flag
        result = engine.toggle_flag(1, 1)
        assert result is False

    def test_game_over_dialog_is_modal(self):
        """Game end dialog is modal and blocks interaction."""
        root = tk.Tk()
        root.withdraw()
        try:
            dialog = GameEndDialog(root, won=True, elapsed_time=0)
            assert dialog.state() == "normal"
            # grab_set() should make it modal
            dialog.grab_set()
            # The grab_set() call should succeed without error
        finally:
            root.destroy()


class TestMainWindowPassesElapsedTime:
    """Tests for MainWindow passing elapsed time to dialog (STORY-015)."""

    def test_on_game_end_passes_elapsed_time(self):
        """MainWindow._on_game_end passes elapsed time to dialog."""
        from src.ui.main_window import MainWindow

        with patch.object(MainWindow, "__init__", lambda self: None):
            mw = MainWindow()
            mw.root = tk.Tk()
            mw.root.withdraw()
            mw.game_engine = MagicMock()
            mw.game_engine.get_elapsed_time.return_value = 456

            with patch("src.ui.main_window.GameEndDialog") as MockDialog:
                mw._on_game_end(won=True)

                MockDialog.assert_called_once()
                call_kwargs = MockDialog.call_args[1]
                assert call_kwargs["elapsed_time"] == 456
                assert call_kwargs["won"] is True

            mw.root.destroy()

    def test_on_game_end_passes_zero_time(self):
        """MainWindow passes 0 elapsed time when timer hasn't started."""
        from src.ui.main_window import MainWindow

        with patch.object(MainWindow, "__init__", lambda self: None):
            mw = MainWindow()
            mw.root = tk.Tk()
            mw.root.withdraw()
            mw.game_engine = MagicMock()
            mw.game_engine.get_elapsed_time.return_value = 0

            with patch("src.ui.main_window.GameEndDialog") as MockDialog:
                mw._on_game_end(won=False)

                MockDialog.assert_called_once()
                call_kwargs = MockDialog.call_args[1]
                assert call_kwargs["elapsed_time"] == 0
                assert call_kwargs["won"] is False

            mw.root.destroy()


class TestGridUpdateAllCellsOnGameEnd:
    """Tests for updating all cells on game end (STORY-015)."""

    def test_update_all_cells_shows_game_over_state(self, root):
        """update_all_cells correctly shows game over visual state."""
        engine = GameEngine(rows=3, cols=3, total_mines=1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        grid_frame = GridFrame(root, engine, rows=3, cols=3)

        # Find the mine and flag it correctly
        mine_pos = None
        for r in range(3):
            for c in range(3):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None
        engine.grid.get_cell(*mine_pos).state = CellState.FLAGGED
        engine.game_over = True
        engine.correct_flags.add(mine_pos)

        # Update all cells
        grid_frame.update_all_cells()

        # Check the flagged mine shows green
        btn = grid_frame.cells[mine_pos[0]][mine_pos[1]]
        assert btn["bg"] == "#00ff00"
        assert btn["text"] == "F"

    def test_update_all_cells_shows_unflagged_mines(self, root):
        """update_all_cells reveals unflagged mines on loss."""
        engine = GameEngine(rows=3, cols=3, total_mines=1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        grid_frame = GridFrame(root, engine, rows=3, cols=3)

        # Find the mine
        mine_pos = None
        for r in range(3):
            for c in range(3):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None
        engine.grid.get_cell(*mine_pos).state = CellState.REVEALED
        engine.game_over = True

        # Update all cells
        grid_frame.update_all_cells()

        # Check the mine shows red background
        btn = grid_frame.cells[mine_pos[0]][mine_pos[1]]
        assert btn["bg"] == "#ff0000"
        assert btn["text"] == "*"


class TestWinDialogTimeFormats:
    """Additional tests for various time formats in win dialog (STORY-015)."""

    def test_time_zero_seconds(self, root):
        """Time displays correctly for 0 seconds."""
        dialog = GameEndDialog(root, won=True, elapsed_time=0)
        assert dialog.time_label.cget("text") == "Time: 00:00"

    def test_time_single_digit_minutes(self, root):
        """Time displays correctly for single digit minutes."""
        dialog = GameEndDialog(root, won=True, elapsed_time=59)
        assert dialog.time_label.cget("text") == "Time: 00:59"

    def test_time_exactly_one_minute(self, root):
        """Time displays correctly for exactly one minute."""
        dialog = GameEndDialog(root, won=True, elapsed_time=60)
        assert dialog.time_label.cget("text") == "Time: 01:00"

    def test_time_five_minutes(self, root):
        """Time displays correctly for five minutes."""
        dialog = GameEndDialog(root, won=True, elapsed_time=300)
        assert dialog.time_label.cget("text") == "Time: 05:00"

    def test_time_with_both_components(self, root):
        """Time displays correctly with both minutes and seconds."""
        dialog = GameEndDialog(root, won=True, elapsed_time=123)
        assert dialog.time_label.cget("text") == "Time: 02:03"

    def test_time_large_seconds(self, root):
        """Time displays correctly with large seconds value."""
        dialog = GameEndDialog(root, won=True, elapsed_time=999)
        assert dialog.time_label.cget("text") == "Time: 16:39"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
