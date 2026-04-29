"""Minesweeper - Grid Rendering tests (STORY-014).

Tests for GridFrame rendering functionality:
- Grid renders dynamically based on selected difficulty dimensions
- Hidden cells display a uniform button/box appearance
- Revealed cells display the correct adjacent mine count (1-8) or blank for 0
- Number colors follow standard Minesweeper convention
- Flagged cells display a flag icon/indicator
- Revealed mines display a mine icon
- Grid resizes correctly when switching difficulties
- Cells are evenly sized and properly aligned
"""

from __future__ import annotations

import tkinter as tk
import unittest
from unittest.mock import MagicMock, patch

from src.config.constants import (
    CELL_FONT,
    CELL_HIDDEN_COLOR,
    CELL_REVEALED_COLOR,
    CELL_FLAGGED_COLOR,
    CELL_MINE_COLOR,
    NUMBER_COLORS,
    FRAME_BG,
)
from src.core.cell import Cell, CellState
from src.core.grid import Grid
from src.core.game import GameEngine
from src.ui.grid_frame import GridFrame


class TestGridFrameRendering(unittest.TestCase):
    """Test GridFrame rendering functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the window during tests

    def tearDown(self):
        """Tear down test fixtures."""
        self.root.destroy()

    def test_grid_creates_buttons_for_all_cells(self):
        """Grid renders a button for each cell in the grid."""
        engine = GameEngine(rows=5, cols=5, total_mines=5)
        grid_frame = GridFrame(self.root, engine, rows=5, cols=5)

        self.assertEqual(len(grid_frame.cells), 5)
        for row in grid_frame.cells:
            self.assertEqual(len(row), 5)

    def test_hidden_cell_default_appearance(self):
        """Hidden cells display a uniform button/box appearance."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        # Update a hidden cell
        cell = engine.grid.get_cell(0, 0)
        self.assertEqual(cell.state, CellState.HIDDEN)
        grid_frame.update_cell(0, 0)

        btn = grid_frame.cells[0][0]
        self.assertEqual(btn["bg"], CELL_HIDDEN_COLOR)
        self.assertEqual(btn["relief"], tk.RAISED)
        self.assertEqual(btn["text"], "")

    def test_revealed_cell_with_number(self):
        """Revealed cells display the correct adjacent mine count."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        # Manually set up a cell with adjacent mines
        cell = engine.grid.get_cell(1, 1)
        cell.is_mine = False
        cell.adjacent_mines = 3
        cell.state = CellState.REVEALED
        grid_frame.update_cell(1, 1)

        btn = grid_frame.cells[1][1]
        self.assertEqual(btn["bg"], CELL_REVEALED_COLOR)
        self.assertEqual(btn["relief"], tk.SUNKEN)
        self.assertEqual(btn["text"], "3")
        self.assertEqual(btn["fg"], NUMBER_COLORS[3])

    def test_revealed_cell_with_zero_mines(self):
        """Revealed cells with 0 adjacent mines display blank."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        cell = engine.grid.get_cell(0, 0)
        cell.is_mine = False
        cell.adjacent_mines = 0
        cell.state = CellState.REVEALED
        grid_frame.update_cell(0, 0)

        btn = grid_frame.cells[0][0]
        self.assertEqual(btn["bg"], CELL_REVEALED_COLOR)
        self.assertEqual(btn["relief"], tk.SUNKEN)
        self.assertEqual(btn["text"], "")

    def test_revealed_mine_display(self):
        """Revealed mines display a mine icon."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        cell = engine.grid.get_cell(1, 1)
        cell.is_mine = True
        cell.state = CellState.REVEALED
        grid_frame.update_cell(1, 1)

        btn = grid_frame.cells[1][1]
        self.assertEqual(btn["bg"], CELL_MINE_COLOR)
        self.assertEqual(btn["relief"], tk.SUNKEN)
        self.assertEqual(btn["text"], "*")

    def test_flagged_cell_display(self):
        """Flagged cells display a flag indicator."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        cell = engine.grid.get_cell(0, 0)
        cell.is_mine = False
        cell.state = CellState.FLAGGED
        grid_frame.update_cell(0, 0)

        btn = grid_frame.cells[0][0]
        self.assertEqual(btn["bg"], CELL_FLAGGED_COLOR)
        self.assertEqual(btn["relief"], tk.RAISED)
        self.assertEqual(btn["text"], "F")
        self.assertEqual(btn["fg"], "red")

    def test_number_colors_follow_standard_convention(self):
        """Number colors follow standard Minesweeper convention."""
        # Verify the constants match the expected colors from minesweeper.md §5
        expected_colors = {
            1: "blue",
            2: "green",
            3: "red",
            4: "darkblue",
            5: "brown",
            6: "cyan",
            7: "black",
            8: "gray",
        }
        for number, expected_color in expected_colors.items():
            self.assertIn(number, NUMBER_COLORS)
            self.assertEqual(
                NUMBER_COLORS[number].lower(),
                expected_color.lower(),
                f"Number {number} color should be {expected_color}",
            )

    def test_all_number_colors_defined(self):
        """All numbers 1-8 have defined colors."""
        for i in range(1, 9):
            self.assertIn(i, NUMBER_COLORS)

    def test_update_cell_hidden_state(self):
        """Hidden cells render with correct appearance."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        cell = engine.grid.get_cell(0, 0)
        cell.state = CellState.HIDDEN
        grid_frame.update_cell(0, 0)

        btn = grid_frame.cells[0][0]
        self.assertEqual(btn["bg"], CELL_HIDDEN_COLOR)
        self.assertEqual(btn["relief"], tk.RAISED)
        self.assertEqual(btn["text"], "")

    def test_update_cell_question_state(self):
        """Question mark cells display with correct appearance."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        cell = engine.grid.get_cell(0, 0)
        cell.state = CellState.QUESTION
        grid_frame.update_cell(0, 0)

        btn = grid_frame.cells[0][0]
        self.assertEqual(btn["bg"], CELL_HIDDEN_COLOR)
        self.assertEqual(btn["relief"], tk.RAISED)
        self.assertEqual(btn["text"], "?")
        self.assertEqual(btn["fg"], "blue")

    def test_update_cell_correct_flag_on_game_over(self):
        """Correctly flagged mines show green background on game over."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        # Place mines and flag one correctly
        engine.place_mines(1, 1)
        cell = engine.grid.get_cell(0, 0)
        cell.is_mine = True
        cell.state = CellState.FLAGGED

        # Simulate game over with correct flag
        engine.game_over = True
        engine.correct_flags.add((0, 0))

        grid_frame.update_cell(0, 0)

        btn = grid_frame.cells[0][0]
        self.assertEqual(btn["bg"], "#00ff00")
        self.assertEqual(btn["text"], "F")

    def test_update_cell_incorrect_flag_on_game_over(self):
        """Incorrectly flagged cells show red background on game over."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        # Flag a cell that is not a mine
        cell = engine.grid.get_cell(0, 0)
        cell.is_mine = False
        cell.state = CellState.FLAGGED

        # Simulate game over with incorrect flag
        engine.game_over = True
        engine.incorrect_flags.add((0, 0))

        grid_frame.update_cell(0, 0)

        btn = grid_frame.cells[0][0]
        self.assertEqual(btn["bg"], "#ff6666")
        self.assertEqual(btn["text"], "X")
        self.assertEqual(btn["fg"], "red")

    def test_update_all_cells_refreshes_grid(self):
        """update_all_cells updates every cell in the grid."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        # Reveal a few cells
        engine.grid.get_cell(0, 0).state = CellState.REVEALED
        engine.grid.get_cell(1, 1).state = CellState.FLAGGED

        grid_frame.update_all_cells()

        # Verify all cells were updated
        self.assertEqual(grid_frame.cells[0][0]["bg"], CELL_REVEALED_COLOR)
        self.assertEqual(grid_frame.cells[1][1]["bg"], CELL_FLAGGED_COLOR)

    def test_grid_frame_with_different_dimensions(self):
        """GridFrame handles different grid dimensions correctly."""
        for rows, cols in [(9, 9), (16, 16), (16, 30), (5, 5)]:
            engine = GameEngine(rows=rows, cols=cols, total_mines=10)
            grid_frame = GridFrame(self.root, engine, rows=rows, cols=cols)

            self.assertEqual(len(grid_frame.cells), rows)
            for row in grid_frame.cells:
                self.assertEqual(len(row), cols)

    def test_cell_font_is_courier(self):
        """Cells use Courier font for consistent number display."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        btn = grid_frame.cells[0][0]
        self.assertEqual(btn["font"], CELL_FONT)

    def test_frame_background_color(self):
        """GridFrame uses the configured frame background color."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        self.assertEqual(grid_frame["bg"], FRAME_BG)

    def test_update_cell_out_of_bounds_safe(self):
        """update_cell handles out-of-bounds indices gracefully."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        # Should not raise an exception
        grid_frame.update_cell(-1, 0)
        grid_frame.update_cell(0, -1)
        grid_frame.update_cell(3, 0)
        grid_frame.update_cell(0, 3)

    def test_revealed_cell_adjacent_mine_count_accurate(self):
        """Revealed cells show accurate adjacent mine counts."""
        engine = GameEngine(rows=9, cols=9, total_mines=10)
        engine.place_mines(4, 4)
        grid_frame = GridFrame(self.root, engine, rows=9, cols=9)

        # Check that adjacent mine counts are correctly calculated
        # by revealing all non-mine cells first, then verifying their display
        for r in range(9):
            for c in range(9):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine:
                    cell.state = CellState.REVEALED
                    grid_frame.update_cell(r, c)
                    btn = grid_frame.cells[r][c]
                    if cell.adjacent_mines > 0:
                        self.assertEqual(
                            btn["text"],
                            str(cell.adjacent_mines),
                            f"Cell ({r},{c}) text mismatch",
                        )
                        self.assertEqual(
                            btn["fg"],
                            NUMBER_COLORS.get(cell.adjacent_mines, "black"),
                        )
                        self.assertEqual(btn["bg"], CELL_REVEALED_COLOR)
                        self.assertEqual(btn["relief"], tk.SUNKEN)
                    else:
                        self.assertEqual(btn["text"], "")
                        self.assertEqual(btn["bg"], CELL_REVEALED_COLOR)
                        self.assertEqual(btn["relief"], tk.SUNKEN)

    def test_left_click_binding_exists(self):
        """Grid cells have left-click bindings."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        btn = grid_frame.cells[0][0]
        bindings = btn.bind()
        self.assertIn("<Button-1>", bindings)

    def test_right_click_binding_exists(self):
        """Grid cells have right-click bindings."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        btn = grid_frame.cells[0][0]
        bindings = btn.bind()
        self.assertIn("<Button-3>", bindings)

    def test_grid_frame_packs_into_parent(self):
        """GridFrame can be packed into a parent widget."""
        engine = GameEngine(rows=3, cols=3, total_mines=2)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)
        grid_frame.pack(expand=True, fill=tk.BOTH)

        # Verify the frame is properly packed
        self.assertEqual(
            grid_frame.nametowidget(grid_frame.pack_info()["in"]), self.root
        )


class TestGridRenderingIntegration(unittest.TestCase):
    """Integration tests for grid rendering with game engine."""

    def setUp(self):
        """Set up test fixtures."""
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        """Tear down test fixtures."""
        self.root.destroy()

    def test_reveal_cell_updates_display(self):
        """Revealing a cell updates its visual state."""
        engine = GameEngine(rows=3, cols=3, total_mines=1)
        engine.place_mines(1, 1)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        # Before reveal
        self.assertEqual(engine.grid.get_cell(0, 0).state, CellState.HIDDEN)

        # Reveal the cell
        engine.reveal_cell(0, 0)

        # After reveal
        self.assertEqual(engine.grid.get_cell(0, 0).state, CellState.REVEALED)
        grid_frame.update_cell(0, 0)

        btn = grid_frame.cells[0][0]
        self.assertEqual(btn["bg"], CELL_REVEALED_COLOR)
        self.assertEqual(btn["relief"], tk.SUNKEN)

    def test_toggle_flag_updates_display(self):
        """Toggling a flag updates its visual state."""
        engine = GameEngine(rows=3, cols=3, total_mines=1)
        grid_frame = GridFrame(self.root, engine, rows=3, cols=3)

        # Toggle flag on
        engine.toggle_flag(0, 0)
        grid_frame.update_cell(0, 0)

        btn = grid_frame.cells[0][0]
        self.assertEqual(btn["text"], "F")
        self.assertEqual(btn["fg"], "red")
        self.assertEqual(btn["relief"], tk.RAISED)

        # Toggle flag off
        engine.toggle_flag(0, 0)
        grid_frame.update_cell(0, 0)

        self.assertEqual(btn["text"], "")
        self.assertEqual(btn["relief"], tk.RAISED)


if __name__ == "__main__":
    unittest.main()
