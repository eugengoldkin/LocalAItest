"""Tests for difficulty presets (STORY-003).

Tests for:
- Difficulty preset values (Beginner, Intermediate, Expert)
- DifficultyManager/configuration module
- Preset selection from UI
- Game initialization with selected presets
"""

import pytest

from src.config.difficulty import (
    DEFAULT_DIFFICULTY,
    DIFFICULTY_PRESETS,
    Difficulty,
    MAX_GRID_HEIGHT,
    MAX_GRID_WIDTH,
    MIN_GRID_SIZE,
    MIN_MINES,
)


class TestDifficultyPresets:
    """Tests for difficulty preset values (AC1-AC3)."""

    def test_beginner_preset(self):
        """AC1: Beginner preset has correct dimensions."""
        preset = DIFFICULTY_PRESETS["Beginner"]
        assert preset.name == "Beginner"
        assert preset.cols == 9
        assert preset.rows == 9
        assert preset.mines == 10

    def test_intermediate_preset(self):
        """AC2: Intermediate preset has correct dimensions."""
        preset = DIFFICULTY_PRESETS["Intermediate"]
        assert preset.name == "Intermediate"
        assert preset.cols == 16
        assert preset.rows == 16
        assert preset.mines == 40

    def test_expert_preset(self):
        """AC3: Expert preset has correct dimensions."""
        preset = DIFFICULTY_PRESETS["Expert"]
        assert preset.name == "Expert"
        assert preset.cols == 30
        assert preset.rows == 16
        assert preset.mines == 99

    def test_all_presets_defined(self):
        """All three standard presets are defined."""
        expected_presets = {"Beginner", "Intermediate", "Expert"}
        assert set(DIFFICULTY_PRESETS.keys()) == expected_presets

    def test_presets_are_immutable(self):
        """Difficulty presets are frozen dataclasses (immutable)."""
        preset = DIFFICULTY_PRESETS["Beginner"]
        with pytest.raises(Exception):
            preset.rows = 10

    def test_default_difficulty_is_valid(self):
        """DEFAULT_DIFFICULTY is a valid preset key."""
        assert DEFAULT_DIFFICULTY in DIFFICULTY_PRESETS

    def test_default_difficulty_is_beginner(self):
        """Default difficulty is Beginner."""
        assert DEFAULT_DIFFICULTY == "Beginner"


class TestDifficultyValidationLimits:
    """Tests for custom difficulty validation limits."""

    def test_min_grid_size(self):
        """Minimum grid size is 9."""
        assert MIN_GRID_SIZE == 9

    def test_max_grid_width(self):
        """Maximum grid width is 50."""
        assert MAX_GRID_WIDTH == 50

    def test_max_grid_height(self):
        """Maximum grid height is 50."""
        assert MAX_GRID_HEIGHT == 50

    def test_min_mines(self):
        """Minimum mines is 1."""
        assert MIN_MINES == 1


class TestDifficultyDataclass:
    """Tests for the Difficulty dataclass."""

    def test_difficulty_creation(self):
        """Difficulty dataclass can be instantiated."""
        difficulty = Difficulty(name="Test", rows=10, cols=10, mines=5)
        assert difficulty.name == "Test"
        assert difficulty.rows == 10
        assert difficulty.cols == 10
        assert difficulty.mines == 5

    def test_difficulty_comparison(self):
        """Difficulty dataclasses can be compared."""
        d1 = Difficulty(name="Test", rows=10, cols=10, mines=5)
        d2 = Difficulty(name="Test", rows=10, cols=10, mines=5)
        assert d1 == d2

    def test_difficulty_as_dict_key(self):
        """Difficulty dataclass can be used as a dict key (hashable)."""
        d = Difficulty(name="Test", rows=10, cols=10, mines=5)
        dict_test = {d: "value"}
        assert dict_test[d] == "value"


class TestDifficultyPresetUsage:
    """Tests for using difficulty presets with GameEngine."""

    def test_beginner_preset_initializes_game(self):
        """Beginner preset creates a valid game engine."""
        from src.core.game import GameEngine

        preset = DIFFICULTY_PRESETS["Beginner"]
        engine = GameEngine(
            rows=preset.rows,
            cols=preset.cols,
            total_mines=preset.mines,
        )

        assert engine.grid.rows == preset.rows
        assert engine.grid.cols == preset.cols
        assert engine.total_mines == preset.mines
        assert engine.flags_placed == 0
        assert not engine.game_over
        assert not engine.game_won
        assert not engine.first_click_done

    def test_intermediate_preset_initializes_game(self):
        """Intermediate preset creates a valid game engine."""
        from src.core.game import GameEngine

        preset = DIFFICULTY_PRESETS["Intermediate"]
        engine = GameEngine(
            rows=preset.rows,
            cols=preset.cols,
            total_mines=preset.mines,
        )

        assert engine.grid.rows == preset.rows
        assert engine.grid.cols == preset.cols
        assert engine.total_mines == preset.mines

    def test_expert_preset_initializes_game(self):
        """Expert preset creates a valid game engine."""
        from src.core.game import GameEngine

        preset = DIFFICULTY_PRESETS["Expert"]
        engine = GameEngine(
            rows=preset.rows,
            cols=preset.cols,
            total_mines=preset.mines,
        )

        assert engine.grid.rows == preset.rows
        assert engine.grid.cols == preset.cols
        assert engine.total_mines == preset.mines

    def test_all_presets_create_valid_grids(self):
        """All presets create grids with correct cell counts."""
        from src.core.game import GameEngine

        for name, preset in DIFFICULTY_PRESETS.items():
            engine = GameEngine(
                rows=preset.rows,
                cols=preset.cols,
                total_mines=preset.mines,
            )

            # Verify grid dimensions
            assert engine.grid.rows == preset.rows, (
                f"{name}: rows mismatch"
            )
            assert engine.grid.cols == preset.cols, (
                f"{name}: cols mismatch"
            )

            # Verify total cells match
            total_cells = engine.grid.rows * engine.grid.cols
            assert len(engine.grid.cells) == engine.grid.rows
            for row in engine.grid.cells:
                assert len(row) == engine.grid.cols

            # Verify mine count is valid (less than total cells)
            assert preset.mines < total_cells, (
                f"{name}: mines ({preset.mines}) >= total cells ({total_cells})"
            )

    def test_game_reset_after_preset_change(self):
        """Game can be reset after changing presets."""
        from src.core.game import GameEngine

        # Start with Beginner
        beginner = DIFFICULTY_PRESETS["Beginner"]
        engine = GameEngine(
            rows=beginner.rows,
            cols=beginner.cols,
            total_mines=beginner.mines,
        )

        # Place some flags
        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        assert engine.flags_placed == 2

        # Reset
        engine.reset()
        assert engine.flags_placed == 0
        assert not engine.game_over

        # Change to Intermediate
        intermediate = DIFFICULTY_PRESETS["Intermediate"]
        engine = GameEngine(
            rows=intermediate.rows,
            cols=intermediate.cols,
            total_mines=intermediate.mines,
        )

        assert engine.grid.rows == intermediate.rows
        assert engine.grid.cols == intermediate.cols
        assert engine.total_mines == intermediate.mines
