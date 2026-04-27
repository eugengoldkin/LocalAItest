"""Tests for the Grid model.

STORY-002: Unit tests for Grid class with mine placement and adjacency counting.
"""

import pytest
import random
from src.core.cell import Cell, CellState
from src.core.grid import Grid


class TestGrid:
    """Tests for the Grid class."""

    def test_create_grid_9x9(self):
        """Test creating a 9x9 grid."""
        grid = Grid(9, 9)
        assert grid.rows == 9
        assert grid.cols == 9
        assert len(grid.cells) == 9
        for row in grid.cells:
            assert len(row) == 9

    def test_create_grid_small(self):
        """Test creating a small grid."""
        grid = Grid(3, 3)
        assert grid.rows == 3
        assert grid.cols == 3
        assert len(grid.cells) == 3
        for row in grid.cells:
            assert len(row) == 3

    def test_create_grid_large(self):
        """Test creating a large grid."""
        grid = Grid(30, 30)
        assert grid.rows == 30
        assert grid.cols == 30

    def test_cells_initialized_hidden(self):
        """Test that all cells start in HIDDEN state."""
        grid = Grid(9, 9)
        for r in range(grid.rows):
            for c in range(grid.cols):
                cell = grid.cells[r][c]
                assert cell.state == CellState.HIDDEN
                assert cell.is_mine is False
                assert cell.adjacent_mines == 0

    def test_cell_coordinates(self):
        """Test that cell coordinates are set correctly."""
        grid = Grid(5, 5)
        for r in range(grid.rows):
            for c in range(grid.cols):
                cell = grid.cells[r][c]
                assert cell.row == r
                assert cell.col == c

    def test_get_cell_valid(self):
        """Test retrieving a valid cell."""
        grid = Grid(9, 9)
        cell = grid.get_cell(4, 4)
        assert cell is not None
        assert cell.row == 4
        assert cell.col == 4

    def test_get_cell_out_of_bounds(self):
        """Test that out-of-bounds returns None."""
        grid = Grid(9, 9)
        assert grid.get_cell(-1, 0) is None
        assert grid.get_cell(0, -1) is None
        assert grid.get_cell(9, 0) is None
        assert grid.get_cell(0, 9) is None
        assert grid.get_cell(10, 10) is None

    def test_reset(self):
        """Test that reset restores all cells to default state."""
        grid = Grid(3, 3)
        # Modify all cells
        for r in range(grid.rows):
            for c in range(grid.cols):
                grid.cells[r][c].is_mine = True
                grid.cells[r][c].state = CellState.REVEALED
                grid.cells[r][c].adjacent_mines = 8

        grid.reset()

        for r in range(grid.rows):
            for c in range(grid.cols):
                cell = grid.cells[r][c]
                assert cell.is_mine is False
                assert cell.state == CellState.HIDDEN
                assert cell.adjacent_mines == 0

    def test_reset_preserves_dimensions(self):
        """Test that reset does not change grid dimensions."""
        grid = Grid(5, 7)
        grid.reset()
        assert grid.rows == 5
        assert grid.cols == 7

    def test_repr(self):
        """Test the string representation of a Grid."""
        grid = Grid(9, 9)
        assert repr(grid) == "Grid(9x9)"

    def test_repr_custom(self):
        """Test repr with custom dimensions."""
        grid = Grid(30, 16)
        assert repr(grid) == "Grid(30x16)"


class TestGridSerialization:
    """Tests for Grid serialization (to_dict / from_dict)."""

    def test_to_dict_default_grid(self):
        """Test serializing a default grid."""
        grid = Grid(3, 3)
        data = grid.to_dict()

        assert data["rows"] == 3
        assert data["cols"] == 3
        assert len(data["cells"]) == 3
        for row in data["cells"]:
            assert len(row) == 3

    def test_to_dict_modified_grid(self):
        """Test serializing a grid with modified cells."""
        grid = Grid(2, 2)
        grid.cells[0][0].is_mine = True
        grid.cells[0][0].state = CellState.FLAGGED
        grid.cells[0][0].adjacent_mines = 3
        grid.cells[1][1].state = CellState.REVEALED

        data = grid.to_dict()

        assert data["cells"][0][0]["is_mine"] is True
        assert data["cells"][0][0]["state"] == "flagged"
        assert data["cells"][0][0]["adjacent_mines"] == 3
        assert data["cells"][1][1]["state"] == "revealed"

    def test_from_dict(self):
        """Test deserializing a grid from a dictionary."""
        data = {
            "rows": 2,
            "cols": 3,
            "cells": [
                [
                    {"row": 0, "col": 0, "is_mine": True, "state": "flagged", "adjacent_mines": 1},
                    {"row": 0, "col": 1, "is_mine": False, "state": "revealed", "adjacent_mines": 0},
                    {"row": 0, "col": 2, "is_mine": False, "state": "hidden", "adjacent_mines": 0},
                ],
                [
                    {"row": 1, "col": 0, "is_mine": False, "state": "hidden", "adjacent_mines": 2},
                    {"row": 1, "col": 1, "is_mine": True, "state": "hidden", "adjacent_mines": 0},
                    {"row": 1, "col": 2, "is_mine": False, "state": "revealed", "adjacent_mines": 0},
                ],
            ],
        }

        grid = Grid.from_dict(data)

        assert grid.rows == 2
        assert grid.cols == 3
        assert grid.cells[0][0].is_mine is True
        assert grid.cells[0][0].state == CellState.FLAGGED
        assert grid.cells[0][0].adjacent_mines == 1
        assert grid.cells[1][1].is_mine is True
        assert grid.cells[1][1].state == CellState.HIDDEN

    def test_roundtrip_serialization(self):
        """Test that serializing and deserializing preserves grid state."""
        original = Grid(3, 3)
        original.cells[0][0].is_mine = True
        original.cells[0][0].state = CellState.FLAGGED
        original.cells[0][0].adjacent_mines = 2
        original.cells[1][1].state = CellState.REVEALED
        original.cells[1][1].adjacent_mines = 5

        data = original.to_dict()
        restored = Grid.from_dict(data)

        assert restored.rows == original.rows
        assert restored.cols == original.cols
        assert restored.cells[0][0].is_mine == original.cells[0][0].is_mine
        assert restored.cells[0][0].state == original.cells[0][0].state
        assert restored.cells[0][0].adjacent_mines == original.cells[0][0].adjacent_mines
        assert restored.cells[1][1].state == original.cells[1][1].state
        assert restored.cells[1][1].adjacent_mines == original.cells[1][1].adjacent_mines


class TestGridMinePlacement:
    """Tests for mine placement on the Grid via GameEngine."""

    def test_mine_placement_counts(self):
        """Test that the correct number of mines are placed."""
        from src.core.game import GameEngine

        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        mine_count = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].is_mine
        )
        assert mine_count == 10

    def test_mines_not_in_excluded_area(self):
        """Test that no mines are placed in the excluded area."""
        from src.core.game import GameEngine

        engine = GameEngine(9, 9, 10)
        engine.place_mines(4, 4)

        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 4 + dr, 4 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    assert engine.grid.cells[nr][nc].is_mine is False

    def test_adjacent_mine_count_center(self):
        """Test adjacent mine count for a cell in the center of the grid."""
        from src.core.game import GameEngine

        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        count = engine.get_adjacent_mine_count(4, 4)
        assert isinstance(count, int)
        assert 0 <= count <= 8

    def test_adjacent_mine_count_edge(self):
        """Test adjacent mine count for a cell on the edge."""
        from src.core.game import GameEngine

        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        count = engine.get_adjacent_mine_count(0, 0)
        assert isinstance(count, int)
        assert 0 <= count <= 3

    def test_adjacent_mine_count_corner(self):
        """Test adjacent mine count for a corner cell."""
        from src.core.game import GameEngine

        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        count = engine.get_adjacent_mine_count(0, 0)
        assert isinstance(count, int)
        assert 0 <= count <= 3

    def test_adjacent_mine_count_out_of_bounds(self):
        """Test that out-of-bounds returns 0."""
        from src.core.game import GameEngine

        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        assert engine.get_adjacent_mine_count(-1, -1) == 0
        assert engine.get_adjacent_mine_count(9, 9) == 0

    def test_all_cells_have_adjacent_counts(self):
        """Test that all cells have their adjacent mine counts set."""
        from src.core.game import GameEngine

        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.cells[r][c]
                assert isinstance(cell.adjacent_mines, int)
                assert cell.adjacent_mines >= 0

    def test_mine_count_matches_actual(self):
        """Test that the placed mine count matches total_mines."""
        from src.core.game import GameEngine

        engine = GameEngine(10, 10, 20)
        engine.place_mines(5, 5)

        actual_mines = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].is_mine
        )
        assert actual_mines == engine.total_mines

    def test_mine_count_capped_by_available_cells(self):
        """Test that mine count is capped when mines > available cells."""
        from src.core.game import GameEngine

        # 5x5 grid = 25 cells, exclude (2,2) and neighbors = 9 excluded
        engine = GameEngine(5, 5, 20)
        engine.place_mines(2, 2)

        actual_mines = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].is_mine
        )
        assert actual_mines == 16

    def test_reproducible_with_seed(self):
        """Test that mine placement is reproducible with a fixed seed."""
        from src.core.game import GameEngine

        random.seed(42)
        engine1 = GameEngine(9, 9, 10)
        engine1.place_mines(0, 0)

        random.seed(42)
        engine2 = GameEngine(9, 9, 10)
        engine2.place_mines(0, 0)

        for r in range(engine1.grid.rows):
            for c in range(engine1.grid.cols):
                assert engine1.grid.cells[r][c].is_mine == engine2.grid.cells[r][c].is_mine
