"""Tests for custom difficulty (STORY-004).

Tests for:
- CustomDifficultyDialog validation logic
- CustomDifficultyInput dataclass
- Input validation (min/max bounds, mines < total cells)
- Edge cases (minimum values, maximum values, invalid inputs)
"""

import pytest

from src.config.difficulty import (
    MAX_GRID_HEIGHT,
    MAX_GRID_WIDTH,
    MIN_GRID_SIZE,
    MIN_MINES,
)
from src.core.game import GameEngine
from src.ui.custom_difficulty_dialog import (
    CustomDifficultyDialog,
    CustomDifficultyInput,
)


class TestCustomDifficultyInput:
    """Tests for the CustomDifficultyInput dataclass."""

    def test_creation_valid_input(self):
        """CustomDifficultyInput can be created with valid values."""
        custom = CustomDifficultyInput(rows=10, cols=10, mines=5)
        assert custom.rows == 10
        assert custom.cols == 10
        assert custom.mines == 5

    def test_creation_minimum_values(self):
        """CustomDifficultyInput can be created with minimum values."""
        custom = CustomDifficultyInput(
            rows=MIN_GRID_SIZE,
            cols=MIN_GRID_SIZE,
            mines=MIN_MINES,
        )
        assert custom.rows == MIN_GRID_SIZE
        assert custom.cols == MIN_GRID_SIZE
        assert custom.mines == MIN_MINES

    def test_creation_maximum_values(self):
        """CustomDifficultyInput can be created with maximum values."""
        # Max mines should be less than total cells (rows * cols - 1)
        custom = CustomDifficultyInput(
            rows=MAX_GRID_HEIGHT,
            cols=MAX_GRID_WIDTH,
            mines=(MAX_GRID_HEIGHT * MAX_GRID_WIDTH) - 1,
        )
        assert custom.rows == MAX_GRID_HEIGHT
        assert custom.cols == MAX_GRID_WIDTH
        assert custom.mines == (MAX_GRID_HEIGHT * MAX_GRID_WIDTH) - 1

    def test_comparison(self):
        """CustomDifficultyInput dataclasses can be compared."""
        c1 = CustomDifficultyInput(rows=10, cols=10, mines=5)
        c2 = CustomDifficultyInput(rows=10, cols=10, mines=5)
        assert c1 == c2

    def test_not_equal(self):
        """Different CustomDifficultyInput values are not equal."""
        c1 = CustomDifficultyInput(rows=10, cols=10, mines=5)
        c2 = CustomDifficultyInput(rows=10, cols=10, mines=6)
        assert c1 != c2


class TestValidationLimits:
    """Tests for validation limit constants."""

    def test_min_grid_size_is_9(self):
        """Minimum grid size constant is 9."""
        assert MIN_GRID_SIZE == 9

    def test_max_grid_width_is_50(self):
        """Maximum grid width constant is 50."""
        assert MAX_GRID_WIDTH == 50

    def test_max_grid_height_is_50(self):
        """Maximum grid height constant is 50."""
        assert MAX_GRID_HEIGHT == 50

    def test_min_mines_is_1(self):
        """Minimum mines constant is 1."""
        assert MIN_MINES == 1


@pytest.fixture(scope="module")
def _shared_tk_root():
    """Provide a shared Tk root window for all dialog tests."""
    root = pytest.importorskip("tkinter").Tk()
    root.withdraw()
    yield root
    root.destroy()


class TestValidationLogic:
    """Tests for validation logic in CustomDifficultyDialog."""

    def _create_dialog(self, root):
        """Helper to create a dialog instance for testing.

        Args:
            root: A shared Tkinter root window to use as parent.
        """
        dialog = CustomDifficultyDialog(root)
        return dialog

    def test_valid_minimum_values(self, _shared_tk_root):
        """Minimum valid values pass validation."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=MIN_GRID_SIZE,
            rows=MIN_GRID_SIZE,
            mines=MIN_MINES,
        )
        assert error is None
        dialog.destroy()

    def test_valid_custom_values(self, _shared_tk_root):
        """Valid custom values pass validation."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=20,
            rows=15,
            mines=30,
        )
        assert error is None
        dialog.destroy()

    def test_width_below_minimum(self, _shared_tk_root):
        """Width below minimum triggers error."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=MIN_GRID_SIZE - 1,
            rows=MIN_GRID_SIZE,
            mines=MIN_MINES,
        )
        assert error is not None
        assert "at least" in error.lower()
        dialog.destroy()

    def test_height_below_minimum(self, _shared_tk_root):
        """Height below minimum triggers error."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=MIN_GRID_SIZE,
            rows=MIN_GRID_SIZE - 1,
            mines=MIN_MINES,
        )
        assert error is not None
        assert "at least" in error.lower()
        dialog.destroy()

    def test_width_above_maximum(self, _shared_tk_root):
        """Width above maximum triggers error."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=MAX_GRID_WIDTH + 1,
            rows=MIN_GRID_SIZE,
            mines=MIN_MINES,
        )
        assert error is not None
        assert "at most" in error.lower()
        dialog.destroy()

    def test_height_above_maximum(self, _shared_tk_root):
        """Height above maximum triggers error."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=MIN_GRID_SIZE,
            rows=MAX_GRID_HEIGHT + 1,
            mines=MIN_MINES,
        )
        assert error is not None
        assert "at most" in error.lower()
        dialog.destroy()

    def test_mines_below_minimum(self, _shared_tk_root):
        """Mine count below minimum triggers error."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=MIN_GRID_SIZE,
            rows=MIN_GRID_SIZE,
            mines=MIN_MINES - 1,
        )
        assert error is not None
        assert "at least" in error.lower()
        dialog.destroy()

    def test_mines_equals_total_cells(self, _shared_tk_root):
        """Mines equal to total cells triggers error."""
        dialog = self._create_dialog(_shared_tk_root)
        rows = 10
        cols = 10
        error = dialog._validate_bounds(
            cols=cols,
            rows=rows,
            mines=rows * cols,
        )
        assert error is not None
        assert "less than" in error.lower()
        dialog.destroy()

    def test_mines_greater_than_total_cells(self, _shared_tk_root):
        """Mines greater than total cells triggers error."""
        dialog = self._create_dialog(_shared_tk_root)
        rows = 10
        cols = 10
        error = dialog._validate_bounds(
            cols=cols,
            rows=rows,
            mines=rows * cols + 1,
        )
        assert error is not None
        assert "less than" in error.lower()
        dialog.destroy()

    def test_mines_equals_total_cells_minus_one(self, _shared_tk_root):
        """Mines equal to total cells minus one passes validation."""
        dialog = self._create_dialog(_shared_tk_root)
        rows = 10
        cols = 10
        error = dialog._validate_bounds(
            cols=cols,
            rows=rows,
            mines=rows * cols - 1,
        )
        assert error is None
        dialog.destroy()

    def test_large_grid_valid(self, _shared_tk_root):
        """Large valid grid passes validation."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=MAX_GRID_WIDTH,
            rows=MAX_GRID_HEIGHT,
            mines=(MAX_GRID_WIDTH * MAX_GRID_HEIGHT) - 1,
        )
        assert error is None
        dialog.destroy()

    def test_edge_case_small_grid(self, _shared_tk_root):
        """Smallest possible valid grid passes."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=MIN_GRID_SIZE,
            rows=MIN_GRID_SIZE,
            mines=MIN_MINES,
        )
        assert error is None
        dialog.destroy()


class TestGameEngineWithCustomDifficulty:
    """Tests for using custom difficulty with GameEngine."""

    def test_custom_difficulty_initializes_game(self):
        """Custom difficulty creates a valid game engine."""
        custom = CustomDifficultyInput(rows=12, cols=12, mines=15)
        engine = GameEngine(
            rows=custom.rows,
            cols=custom.cols,
            total_mines=custom.mines,
        )

        assert engine.grid.rows == custom.rows
        assert engine.grid.cols == custom.cols
        assert engine.total_mines == custom.mines
        assert not engine.game_over
        assert not engine.game_won

    def test_custom_difficulty_small_grid(self):
        """Custom difficulty with small grid works."""
        custom = CustomDifficultyInput(
            rows=MIN_GRID_SIZE, cols=MIN_GRID_SIZE, mines=MIN_MINES
        )
        engine = GameEngine(
            rows=custom.rows,
            cols=custom.cols,
            total_mines=custom.mines,
        )

        assert engine.grid.rows == MIN_GRID_SIZE
        assert engine.grid.cols == MIN_GRID_SIZE
        assert engine.total_mines == MIN_MINES

    def test_custom_difficulty_large_grid(self):
        """Custom difficulty with large grid works."""
        custom = CustomDifficultyInput(
            rows=25,
            cols=25,
            mines=50,
        )
        engine = GameEngine(
            rows=custom.rows,
            cols=custom.cols,
            total_mines=custom.mines,
        )

        assert engine.grid.rows == 25
        assert engine.grid.cols == 25
        assert engine.total_mines == 50

    def test_custom_difficulty_gameplay(self):
        """Custom difficulty game can be played."""
        custom = CustomDifficultyInput(rows=10, cols=10, mines=10)
        engine = GameEngine(
            rows=custom.rows,
            cols=custom.cols,
            total_mines=custom.mines,
        )

        # First click should work
        state = engine.reveal_cell(0, 0)
        assert state is not None

        # Should not be game over
        assert not engine.game_over

        # Flag a cell far from the first click to avoid flood-fill revealing it
        target_row, target_col = 5, 5
        success = engine.toggle_flag(target_row, target_col)
        assert success is True
        assert engine.flags_placed == 1

    def test_custom_difficulty_reset(self):
        """Custom difficulty game can be reset."""
        custom = CustomDifficultyInput(rows=10, cols=10, mines=10)
        engine = GameEngine(
            rows=custom.rows,
            cols=custom.cols,
            total_mines=custom.mines,
        )

        # Flag before revealing
        engine.toggle_flag(1, 1)
        assert engine.flags_placed == 1

        # Play a bit
        engine.reveal_cell(0, 0)

        # Reset
        engine.reset()
        assert engine.flags_placed == 0
        assert not engine.game_over
        assert not engine.game_won
        assert not engine.first_click_done


class TestEdgeCases:
    """Tests for edge cases in custom difficulty."""

    def _create_dialog(self, root):
        """Helper to create a dialog instance for testing.

        Args:
            root: A shared Tkinter root window to use as parent.
        """
        dialog = CustomDifficultyDialog(root)
        return dialog

    def test_very_small_valid_grid(self, _shared_tk_root):
        """Smallest valid grid: 9x9 with 1 mine."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=9,
            rows=9,
            mines=1,
        )
        assert error is None
        dialog.destroy()

    def test_mines_one_less_than_cells(self, _shared_tk_root):
        """Mines exactly one less than total cells is valid."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=10,
            rows=10,
            mines=99,
        )
        assert error is None
        dialog.destroy()

    def test_negative_values(self, _shared_tk_root):
        """Negative mine count triggers error."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=10,
            rows=10,
            mines=-1,
        )
        assert error is not None
        dialog.destroy()

    def test_zero_values(self, _shared_tk_root):
        """Zero mine count triggers error."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=10,
            rows=10,
            mines=0,
        )
        assert error is not None
        dialog.destroy()

    def test_very_large_grid(self, _shared_tk_root):
        """Maximum size grid with valid mines."""
        dialog = self._create_dialog(_shared_tk_root)
        error = dialog._validate_bounds(
            cols=MAX_GRID_WIDTH,
            rows=MAX_GRID_HEIGHT,
            mines=1,
        )
        assert error is None
        dialog.destroy()
