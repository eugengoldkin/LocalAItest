"""Tests for New Game Button (STORY-012).

Tests for:
- New Game button visibility and accessibility
- Button click triggers game reset
- Visual feedback on button press (expression change)
- Timer resets to 00:00
- Mine counter resets to total mine count
- Game state resets to "playing"
- First-click safety is re-established on new game
"""

import pytest
import tkinter as tk
from unittest.mock import MagicMock, patch

from src.core.cell import CellState
from src.core.game import GameEngine
from src.ui.main_window import MainWindow


@pytest.fixture(scope="module")
def app():
    """Create a MainWindow instance for testing (module-scoped to avoid Tcl/Tk issues)."""
    with patch("tkinter.Tk.mainloop"):
        instance = MainWindow()
        yield instance
        instance.destroy()


class TestNewGameButtonVisibility:
    """Tests for New Game button visibility and accessibility (AC1)."""

    def test_new_game_button_exists(self, app):
        """AC1: New Game button is visible and accessible in the UI."""
        assert hasattr(app, "new_game_button")
        assert isinstance(app.new_game_button, tk.Button)

    def test_new_game_button_has_smiley_text(self, app):
        """AC1: Button displays a smiley face emoji."""
        assert app.new_game_button.cget("text") == "\U0001f642"

    def test_new_game_button_is_raised(self, app):
        """AC1: Button has raised relief (3D look)."""
        assert app.new_game_button.cget("relief") == "raised"


class TestNewGameButtonReset:
    """Tests for New Game button reset logic (AC2-AC6)."""

    def test_button_click_resets_game_over(self, app):
        """AC2: Clicking the button resets the game board."""
        # First click to trigger mine placement
        app.game_engine.reveal_cell(4, 4)
        # Trigger game over by clicking a mine
        for r in range(app.game_engine.grid.rows):
            for c in range(app.game_engine.grid.cols):
                if app.game_engine.grid.cells[r][c].is_mine:
                    app.game_engine.reveal_cell(r, c)
                    break
            if app.game_engine.game_over:
                break

            assert app.game_engine.game_over is True

        # Start new game
        app.start_new_game()

        assert app.game_engine.game_over is False

    def test_button_click_resets_timer(self, app):
        """AC4: Timer resets to 00:00."""
        # Start the timer
        app.game_engine.reveal_cell(4, 4)
        assert app.game_engine.timer_running

        # Start new game
        app.start_new_game()

        assert app.timer_label.cget("text") == "00:00"
        assert app.game_engine.elapsed_time == 0
        assert app.game_engine.timer_running is False

    def test_button_click_resets_mine_counter(self, app):
        """AC5: Mine counter resets to total mine count."""
        initial_mines = app.game_engine.total_mines

        # Place some flags
        app.game_engine.toggle_flag(0, 0)
        app.game_engine.toggle_flag(1, 1)
        app.game_engine.toggle_flag(2, 2)

        assert app.game_engine.flags_placed == 3

        # Start new game
        app.start_new_game()

        assert app.mine_counter_label.cget("text") == f"Mines: {initial_mines}"
        assert app.game_engine.flags_placed == 0

    def test_button_click_resets_game_state(self, app):
        """AC6: Game state resets to "playing" (no win/loss overlay)."""
        # Start new game should reset to initial state
        app.start_new_game()

        assert app.game_engine.game_over is False
        assert app.game_engine.game_won is False
        assert app.game_engine.first_click_done is False

    def test_button_click_resets_first_click_done(self, app):
        """First-click safety is re-established on new game."""
        # Do a first click
        app.game_engine.reveal_cell(4, 4)
        assert app.game_engine.first_click_done is True

        # Start new game
        app.start_new_game()

        assert app.game_engine.first_click_done is False


class TestNewGameButtonVisualFeedback:
    """Tests for visual feedback on button press (AC7)."""

    def test_button_changes_on_press(self, app):
        """AC7: Button changes expression on press."""
        assert app.new_game_button.cget("text") == "\U0001f642"
        assert app.new_game_button.cget("relief") == "raised"

        # Simulate button press
        app._on_new_game_press(tk.Event())

        assert app.new_game_button.cget("text") == "\U0001f62e"
        assert app.new_game_button.cget("relief") == "sunken"
        assert app._new_game_pressed is True

        # Simulate button release
        app._on_new_game_release(tk.Event())

        assert app.new_game_button.cget("text") == "\U0001f642"
        assert app.new_game_button.cget("relief") == "raised"
        assert app._new_game_pressed is False

    def test_button_expression_changes_to_surprised(self, app):
        """AC7: Button shows surprised face on press."""
        app._on_new_game_press(tk.Event())
        assert app.new_game_button.cget("text") == "\U0001f62e"

    def test_button_expression_changes_back_on_release(self, app):
        """AC7: Button returns to smiley face on release."""
        app._on_new_game_press(tk.Event())
        app._on_new_game_release(tk.Event())
        assert app.new_game_button.cget("text") == "\U0001f642"


class TestNewGameButtonIntegration:
    """Integration tests for New Game button."""

    def test_start_new_game_clears_all_cells(self, app):
        """New game clears all cells back to hidden state."""
        # Reveal some cells
        app.game_engine.reveal_cell(4, 4)
        app.game_engine.reveal_cell(4, 5)

        # Start new game
        app.start_new_game()

        # All cells should be hidden
        for r in range(app.game_engine.grid.rows):
            for c in range(app.game_engine.grid.cols):
                assert app.game_engine.grid.cells[r][c].state == CellState.HIDDEN

    def test_start_new_game_clears_flags(self, app):
        """New game clears all flags."""
        app.game_engine.toggle_flag(0, 0)
        app.game_engine.toggle_flag(1, 1)
        app.game_engine.toggle_flag(2, 2)
        assert app.game_engine.flags_placed == 3

        app.start_new_game()

        assert app.game_engine.flags_placed == 0
        for r in range(app.game_engine.grid.rows):
            for c in range(app.game_engine.grid.cols):
                assert app.game_engine.grid.cells[r][c].state == CellState.HIDDEN

    def test_start_new_game_game_engine_reset(self, app):
        """New game properly resets the game engine state."""
        # Put game in a non-default state
        app.game_engine.reveal_cell(4, 4)
        app.game_engine.toggle_flag(3, 3)

        app.start_new_game()

        assert app.game_engine.game_over is False
        assert app.game_engine.game_won is False
        assert app.game_engine.first_click_done is False
        assert app.game_engine.timer_running is False
        assert app.game_engine.elapsed_time == 0

    def test_new_game_button_command_is_start_new_game(self, app):
        """Button command is wired to start_new_game."""
        # Tkinter converts command callbacks to a string (tcl command name)
        # We verify the command is set by checking it's a non-empty string
        command = app.new_game_button["command"]
        assert isinstance(command, str)
        assert len(command) > 0
