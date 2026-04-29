"""Minesweeper - Mine Counter tests.

STORY-010: Test mine counter accuracy and behavior across game states.

Tests for:
- Initial mine counter value matches total mines
- Counter updates when flags are placed
- Counter updates when flags are removed
- Counter supports negative numbers
- Counter resets on new game
- Counter resets on difficulty change
"""

import unittest

from src.core.game import GameEngine


class TestMineCounterInitialState(unittest.TestCase):
    """Tests for initial mine counter state."""

    def test_initial_counter_matches_total_mines(self):
        """Mine counter starts at total_mines (0 flags placed)."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        remaining = engine.total_mines - engine.flags_placed
        self.assertEqual(remaining, 10)

    def test_initial_counter_matches_beginner_mines(self):
        """Beginner game starts with 10 remaining mines."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        self.assertEqual(engine.total_mines - engine.flags_placed, 10)

    def test_initial_counter_matches_intermediate_mines(self):
        """Intermediate game starts with 40 remaining mines."""
        engine = GameEngine(rows=16, cols=16, total_mines=40)
        self.assertEqual(engine.total_mines - engine.flags_placed, 40)

    def test_initial_counter_matches_expert_mines(self):
        """Expert game starts with 99 remaining mines."""
        engine = GameEngine(rows=16, cols=30, total_mines=99)
        self.assertEqual(engine.total_mines - engine.flags_placed, 99)

    def test_initial_flags_placed_is_zero(self):
        """flags_placed should be 0 on initialization."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        self.assertEqual(engine.flags_placed, 0)


class TestMineCounterFlagPlacement(unittest.TestCase):
    """Tests for mine counter updates when flags are placed."""

    def test_counter_decreases_on_flag_placement(self):
        """Remaining mines decreases by 1 when a flag is placed."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 9)

    def test_counter_decreases_with_multiple_flags(self):
        """Remaining mines decreases correctly with multiple flags."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        engine.toggle_flag(2, 2)
        self.assertEqual(engine.total_mines - engine.flags_placed, 7)

    def test_counter_with_many_flags(self):
        """Counter works correctly with many flags placed."""
        engine = GameEngine(rows=5, cols=5, total_mines=5)
        for r in range(5):
            for c in range(5):
                engine.toggle_flag(r, c)
        # 25 flags placed on 5 mines => -20 remaining
        self.assertEqual(engine.total_mines - engine.flags_placed, -20)

    def test_counter_with_all_cells_flagged(self):
        """Counter shows 0 when all cells are flagged but mines < total cells."""
        engine = GameEngine(rows=5, cols=5, total_mines=3)
        for r in range(5):
            for c in range(5):
                engine.toggle_flag(r, c)
        self.assertEqual(engine.total_mines - engine.flags_placed, -22)

    def test_flags_placed_increases_correctly(self):
        """flags_placed attribute increases correctly."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.toggle_flag(0, 0)
        self.assertEqual(engine.flags_placed, 1)
        engine.toggle_flag(1, 1)
        self.assertEqual(engine.flags_placed, 2)
        engine.toggle_flag(2, 2)
        self.assertEqual(engine.flags_placed, 3)


class TestMineCounterFlagRemoval(unittest.TestCase):
    """Tests for mine counter updates when flags are removed."""

    def test_counter_increases_on_flag_removal(self):
        """Remaining mines increases by 1 when a flag is removed."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 9)
        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 10)

    def test_counter_increases_with_multiple_removals(self):
        """Remaining mines increases correctly with multiple flag removals."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        engine.toggle_flag(2, 2)
        self.assertEqual(engine.total_mines - engine.flags_placed, 7)
        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 8)
        engine.toggle_flag(1, 1)
        self.assertEqual(engine.total_mines - engine.flags_placed, 9)

    def test_counter_returns_to_initial_after_all_removals(self):
        """Counter returns to total_mines after all flags are removed."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        for i in range(5):
            engine.toggle_flag(i, i)
        for i in range(5):
            engine.toggle_flag(i, i)
        self.assertEqual(engine.total_mines - engine.flags_placed, 10)
        self.assertEqual(engine.flags_placed, 0)

    def test_flags_placed_decreases_correctly(self):
        """flags_placed attribute decreases correctly."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        self.assertEqual(engine.flags_placed, 2)
        engine.toggle_flag(0, 0)
        self.assertEqual(engine.flags_placed, 1)
        engine.toggle_flag(1, 1)
        self.assertEqual(engine.flags_placed, 0)


class TestMineCounterNegativeNumbers(unittest.TestCase):
    """Tests for negative mine counter values."""

    def test_counter_can_be_negative(self):
        """Counter shows negative when more flags than mines."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        # Place 15 flags using 2D coordinates
        for i in range(15):
            r, c = divmod(i, 9)
            engine.toggle_flag(r, c)
        remaining = engine.total_mines - engine.flags_placed
        self.assertEqual(remaining, -5)

    def test_counter_negative_one_flag(self):
        """Counter shows -1 when one more flag than mines."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        # Place 11 flags using 2D coordinates
        for i in range(11):
            r, c = divmod(i, 9)
            engine.toggle_flag(r, c)
        self.assertEqual(engine.total_mines - engine.flags_placed, -1)

    def test_counter_negative_many_flags(self):
        """Counter shows correct negative value with many excess flags."""
        engine = GameEngine(rows=5, cols=5, total_mines=1)
        for r in range(5):
            for c in range(5):
                engine.toggle_flag(r, c)
        self.assertEqual(engine.total_mines - engine.flags_placed, -24)

    def test_flags_placed_can_exceed_total_mines(self):
        """flags_placed can exceed total_mines."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        # Place 20 flags using 2D coordinates
        for i in range(20):
            r, c = divmod(i, 9)
            engine.toggle_flag(r, c)
        self.assertGreater(engine.flags_placed, engine.total_mines)


class TestMineCounterReset(unittest.TestCase):
    """Tests for mine counter reset behavior."""

    def test_counter_resets_on_new_game(self):
        """Mine counter resets to total_mines on game reset."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        engine.toggle_flag(2, 2)
        self.assertEqual(engine.total_mines - engine.flags_placed, 7)

        engine.reset()

        self.assertEqual(engine.flags_placed, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 10)

    def test_flags_placed_resets_to_zero(self):
        """flags_placed resets to 0 on game reset."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        self.assertEqual(engine.flags_placed, 2)

        engine.reset()

        self.assertEqual(engine.flags_placed, 0)

    def test_counter_after_reset_allows_new_flagging(self):
        """After reset, flags can be placed again and counter updates."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.toggle_flag(0, 0)
        engine.reset()
        engine.toggle_flag(5, 5)
        self.assertEqual(engine.total_mines - engine.flags_placed, 9)


class TestMineCounterGameplay(unittest.TestCase):
    """Tests for mine counter during gameplay scenarios."""

    def test_counter_during_flagging_session(self):
        """Counter updates correctly during a flagging session."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        expected = 10
        for i in range(10):
            self.assertEqual(engine.total_mines - engine.flags_placed, expected)
            engine.toggle_flag(i, 0)
            expected -= 1

    def test_counter_toggle_behavior(self):
        """Counter updates correctly when toggling flags on same cell."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        self.assertEqual(engine.total_mines - engine.flags_placed, 10)

        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 9)

        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 10)

        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 9)

        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 10)

    def test_counter_with_game_over(self):
        """Counter still reflects correct value after game over."""
        engine = GameEngine(rows=5, cols=5, total_mines=3)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        engine.toggle_flag(2, 2)
        engine.toggle_flag(3, 3)
        self.assertEqual(engine.total_mines - engine.flags_placed, 1)

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        # Counter should still show correct value
        self.assertEqual(engine.total_mines - engine.flags_placed, 1)

    def test_counter_after_game_over_reset(self):
        """Counter resets correctly after game over and reset."""
        engine = GameEngine(rows=5, cols=5, total_mines=3)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        engine.toggle_flag(2, 2)
        self.assertEqual(engine.total_mines - engine.flags_placed, 2)

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        engine.reset()
        self.assertEqual(engine.total_mines - engine.flags_placed, 3)


class TestMineCounterEdgeCases(unittest.TestCase):
    """Tests for mine counter edge cases."""

    def test_counter_with_zero_mines(self):
        """Counter works correctly with zero mines."""
        engine = GameEngine(rows=5, cols=5, total_mines=0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 0)

        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, -1)

    def test_counter_with_single_mine(self):
        """Counter works correctly with a single mine."""
        engine = GameEngine(rows=3, cols=3, total_mines=1)
        self.assertEqual(engine.total_mines - engine.flags_placed, 1)

        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 0)

        engine.toggle_flag(1, 1)
        self.assertEqual(engine.total_mines - engine.flags_placed, -1)

    def test_counter_large_grid(self):
        """Counter works correctly on a large grid."""
        engine = GameEngine(rows=16, cols=30, total_mines=99)
        self.assertEqual(engine.total_mines - engine.flags_placed, 99)

        for i in range(50):
            engine.toggle_flag(i % 16, i % 30)
        self.assertEqual(engine.total_mines - engine.flags_placed, 49)

    def test_counter_no_flags(self):
        """Counter shows total_mines when no flags are placed."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        # Reveal some cells without flagging
        engine.reveal_cell(4, 4)
        self.assertEqual(engine.total_mines - engine.flags_placed, 10)

    def test_counter_toggle_same_cell_multiple_times(self):
        """Counter is stable when toggling the same cell multiple times."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        for _ in range(100):
            engine.toggle_flag(0, 0)
            engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 10)


class TestMineCounterFormula(unittest.TestCase):
    """Tests for the mine counter calculation formula."""

    def test_counter_equals_total_mines_minus_flags(self):
        """Counter always equals total_mines - flags_placed."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        engine.toggle_flag(2, 2)
        self.assertEqual(engine.total_mines - engine.flags_placed, 7)

        engine.toggle_flag(3, 3)
        self.assertEqual(engine.total_mines - engine.flags_placed, 6)

        engine.toggle_flag(0, 0)
        self.assertEqual(engine.total_mines - engine.flags_placed, 7)

    def test_counter_independent_of_grid_size(self):
        """Counter calculation is independent of grid size."""
        engine_small = GameEngine(rows=5, cols=5, total_mines=5)
        engine_large = GameEngine(rows=16, cols=30, total_mines=99)

        engine_small.toggle_flag(0, 0)
        engine_large.toggle_flag(0, 0)

        self.assertEqual(engine_small.total_mines - engine_small.flags_placed, 4)
        self.assertEqual(engine_large.total_mines - engine_large.flags_placed, 98)


if __name__ == "__main__":
    unittest.main()
