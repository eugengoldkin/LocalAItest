"""Minesweeper - Timer tests.

STORY-009: Test timer accuracy and behavior across game states.
"""

import time
import unittest
from unittest.mock import MagicMock, patch

from src.core.game import GameEngine


class TestTimerState(unittest.TestCase):
    """Tests for initial timer state in GameEngine."""

    def test_timer_not_running_initially(self) -> None:
        """Timer should not be running when game is created."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        self.assertFalse(engine.timer_running)

    def test_elapsed_time_zero_initially(self) -> None:
        """Elapsed time should be 0 when game is created."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        self.assertEqual(engine.elapsed_time, 0)

    def test_formatted_time_initially(self) -> None:
        """Formatted time should be '00:00' when game is created."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        self.assertEqual(engine.get_formatted_time(), "00:00")

    def test_elapsed_time_zero_initially_via_getter(self) -> None:
        """get_elapsed_time() should return 0 when game is created."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        self.assertEqual(engine.get_elapsed_time(), 0)


class TestTimerStart(unittest.TestCase):
    """Tests for timer start logic (triggered on first click)."""

    def test_timer_starts_on_first_click(self) -> None:
        """Timer should start when the first cell is revealed."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        self.assertFalse(engine.timer_running)

        # First click reveals a cell (which triggers mine placement and timer start)
        engine.reveal_cell(4, 4)

        self.assertTrue(engine.timer_running)

    def test_timer_does_not_start_before_first_click(self) -> None:
        """Timer should not start before any cells are revealed."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        self.assertFalse(engine.timer_running)
        # No clicks yet, timer should still be stopped
        self.assertFalse(engine.timer_running)

    def test_timer_starts_after_first_click_safety(self) -> None:
        """Timer should start after first-click safety mine placement."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.reveal_cell(0, 0)
        self.assertTrue(engine.timer_running)
        self.assertTrue(engine.first_click_done)


class TestTimerStop(unittest.TestCase):
    """Tests for timer stop logic (triggered on win/loss)."""

    def test_timer_stops_on_loss(self) -> None:
        """Timer should stop when the player clicks a mine."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)

        # First click (safe)
        engine.reveal_cell(4, 4)
        self.assertTrue(engine.timer_running)

        # Click a mine (game over)
        # We need to find a mine position
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            else:
                continue
            break

        self.assertTrue(engine.game_over)
        self.assertFalse(engine.timer_running)

    def test_timer_stops_on_win(self) -> None:
        """Timer should stop when the player wins."""
        # Use a 5x5 grid so the safe zone doesn't cover everything
        engine = GameEngine(rows=5, cols=5, total_mines=1)

        # First click at center (safe)
        engine.reveal_cell(2, 2)
        self.assertTrue(engine.timer_running)

        # Find the mine that was placed and remove it
        actual_mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    actual_mine_pos = (r, c)
                    break
            else:
                continue
            break
        if actual_mine_pos:
            engine.grid.cells[actual_mine_pos[0]][actual_mine_pos[1]].is_mine = False
            engine.total_mines = 0

        # Now reveal all safe cells
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if not engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)

        # Manually trigger win condition check (normally done by the UI)
        engine.check_win_condition()

        self.assertTrue(engine.game_won)
        self.assertTrue(engine.game_over)
        self.assertFalse(engine.timer_running)


class TestTimerReset(unittest.TestCase):
    """Tests for timer reset logic (triggered on new game)."""

    def test_timer_resets_on_new_game(self) -> None:
        """Timer should reset to 00:00 when a new game starts."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)

        # Start the timer
        engine.reveal_cell(4, 4)
        self.assertTrue(engine.timer_running)

        # Reset the game
        engine.reset()

        self.assertFalse(engine.timer_running)
        self.assertEqual(engine.elapsed_time, 0)
        self.assertEqual(engine.get_formatted_time(), "00:00")

    def test_timer_resets_first_click_flag(self) -> None:
        """Timer and first-click flag should reset on new game."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.reveal_cell(4, 4)
        self.assertTrue(engine.first_click_done)

        engine.reset()

        self.assertFalse(engine.first_click_done)
        self.assertFalse(engine.timer_running)


class TestTimerFormat(unittest.TestCase):
    """Tests for MM:SS time formatting."""

    def test_format_seconds(self) -> None:
        """Time should format correctly for seconds."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.elapsed_time = 5
        self.assertEqual(engine.get_formatted_time(), "00:05")

    def test_format_minutes(self) -> None:
        """Time should format correctly for minutes."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.elapsed_time = 60
        self.assertEqual(engine.get_formatted_time(), "01:00")

    def test_format_minutes_and_seconds(self) -> None:
        """Time should format correctly for minutes and seconds."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.elapsed_time = 90
        self.assertEqual(engine.get_formatted_time(), "01:30")

    def test_format_max_time(self) -> None:
        """Time should format correctly at maximum value (999 seconds)."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.elapsed_time = 999
        self.assertEqual(engine.get_formatted_time(), "16:39")

    def test_format_large_minutes(self) -> None:
        """Time should format correctly for larger minute values."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.elapsed_time = 599
        self.assertEqual(engine.get_formatted_time(), "09:59")


class TestTimerCap(unittest.TestCase):
    """Tests for timer capping at MAX_TIME (999 seconds)."""

    def test_timer_capped_at_max_time(self) -> None:
        """Timer should not exceed 999 seconds."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.timer_running = True
        engine._start_time = time.time() - 2000  # Simulate 2000 seconds ago
        formatted = engine.get_formatted_time()
        # Should still show 16:39 (999 seconds)
        self.assertEqual(formatted, "16:39")

    def test_get_elapsed_time_returns_capped_value(self) -> None:
        """get_elapsed_time() should return capped value."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.elapsed_time = 1000
        engine.timer_running = True
        engine._start_time = time.time() - 2000  # Simulate 2000 seconds ago
        self.assertEqual(engine.get_elapsed_time(), 999)

    def test_timer_stays_at_max_when_running(self) -> None:
        """Timer should stay at MAX_TIME even if real time exceeds it."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.elapsed_time = 999
        # Set a very high start time to simulate elapsed time > 999
        engine.timer_running = True
        engine._start_time = time.time() - 2000  # 2000 seconds ago
        result = engine.get_elapsed_time()
        self.assertEqual(result, 999)


class TestTimerAccuracy(unittest.TestCase):
    """Tests for timer accuracy during gameplay."""

    def test_elapsed_time_updates_while_running(self) -> None:
        """Elapsed time should increase while timer is running."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.reveal_cell(4, 4)
        self.assertTrue(engine.timer_running)

        initial_time = engine.get_elapsed_time()
        time.sleep(0.1)
        new_time = engine.get_elapsed_time()

        # After 0.1 seconds, elapsed time should be the same or greater
        # (it could be the same if less than a full second has passed)
        self.assertGreaterEqual(new_time, initial_time)

    def test_elapsed_time_stops_on_game_over(self) -> None:
        """Elapsed time should stop updating when game ends."""
        engine = GameEngine(rows=5, cols=5, total_mines=5)

        # First click (safe)
        engine.reveal_cell(2, 2)
        self.assertTrue(engine.timer_running)

        # Force game over by revealing a mine
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            else:
                continue
            break

        self.assertTrue(engine.game_over)
        time_before = engine.elapsed_time

        time.sleep(0.1)
        time_after = engine.elapsed_time

        # Time should not change after game over
        self.assertEqual(time_before, time_after)


class TestTimerAcrossGameStates(unittest.TestCase):
    """Tests for timer behavior across different game states."""

    def test_timer_starts_on_first_click_and_stops_on_game_over(self) -> None:
        """Full lifecycle: start on first click, stop on game over."""
        engine = GameEngine(rows=5, cols=5, total_mines=5)

        # Before first click
        self.assertFalse(engine.timer_running)
        self.assertEqual(engine.get_formatted_time(), "00:00")

        # First click starts timer
        engine.reveal_cell(2, 2)
        self.assertTrue(engine.timer_running)
        time.sleep(1.1)
        self.assertGreater(engine.get_elapsed_time(), 0)

        # Game over stops timer
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            else:
                continue
            break

        self.assertTrue(engine.game_over)
        self.assertFalse(engine.timer_running)

    def test_timer_resets_on_new_game(self) -> None:
        """Full lifecycle: start, stop, reset, start again."""
        engine = GameEngine(rows=5, cols=5, total_mines=5)

        # First game
        engine.reveal_cell(2, 2)
        self.assertTrue(engine.timer_running)

        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            else:
                continue
            break

        self.assertTrue(engine.game_over)
        self.assertFalse(engine.timer_running)

        # New game
        engine.reset()
        self.assertFalse(engine.timer_running)
        self.assertEqual(engine.elapsed_time, 0)
        self.assertEqual(engine.get_formatted_time(), "00:00")

        # Timer starts again on next click
        engine.reveal_cell(2, 2)
        self.assertTrue(engine.timer_running)

    def test_timer_on_win(self) -> None:
        """Timer should stop and show final time on win."""
        engine = GameEngine(rows=5, cols=5, total_mines=1)

        # First click (safe)
        engine.reveal_cell(2, 2)
        self.assertTrue(engine.timer_running)

        # Find the mine position and remove it
        actual_mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    actual_mine_pos = (r, c)
                    break
            else:
                continue
            break
        if actual_mine_pos:
            engine.grid.cells[actual_mine_pos[0]][actual_mine_pos[1]].is_mine = False
            engine.total_mines = 0

        # Reveal all safe cells
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if not engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)

        # Time should be > 0 (some time elapsed while timer was running)
        time.sleep(1.1)
        elapsed_before_check = engine.get_elapsed_time()

        # Manually trigger win condition check
        engine.check_win_condition()

        self.assertTrue(engine.game_won)
        self.assertTrue(engine.game_over)
        self.assertFalse(engine.timer_running)
        # Time should be > 0 (some time elapsed)
        self.assertGreater(elapsed_before_check, 0)


if __name__ == "__main__":
    unittest.main()
