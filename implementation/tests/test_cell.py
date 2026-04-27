"""Tests for the Cell model.

STORY-002: Unit tests for Cell class with state management.
"""

import pytest
from src.core.cell import Cell, CellState


class TestCell:
    """Tests for the Cell class."""

    def test_initial_state(self):
        """Test that a new Cell starts in HIDDEN state with no mine."""
        cell = Cell(0, 0)
        assert cell.row == 0
        assert cell.col == 0
        assert cell.is_mine is False
        assert cell.state == CellState.HIDDEN
        assert cell.adjacent_mines == 0

    def test_set_mine(self):
        """Test that a Cell can be marked as containing a mine."""
        cell = Cell(1, 2)
        cell.is_mine = True
        assert cell.is_mine is True

    def test_set_state(self):
        """Test that a Cell's state can be changed."""
        cell = Cell(0, 0)
        cell.state = CellState.REVEALED
        assert cell.state == CellState.REVEALED

        cell.state = CellState.FLAGGED
        assert cell.state == CellState.FLAGGED

        cell.state = CellState.QUESTION
        assert cell.state == CellState.QUESTION

    def test_set_adjacent_mine_count(self):
        """Test that adjacent mine count can be set."""
        cell = Cell(3, 3)
        cell.adjacent_mines = 4
        assert cell.adjacent_mines == 4

    def test_reset(self):
        """Test that reset restores the cell to default state."""
        cell = Cell(2, 2)
        cell.is_mine = True
        cell.state = CellState.REVEALED
        cell.adjacent_mines = 7

        cell.reset()

        assert cell.is_mine is False
        assert cell.state == CellState.HIDDEN
        assert cell.adjacent_mines == 0

    def test_reset_preserves_coordinates(self):
        """Test that reset does not change row/col."""
        cell = Cell(5, 7)
        cell.reset()
        assert cell.row == 5
        assert cell.col == 7

    def test_repr(self):
        """Test the string representation of a Cell."""
        cell = Cell(1, 2)
        cell.is_mine = True
        cell.state = CellState.FLAGGED
        expected = "Cell(1,2) mine=True state=flagged"
        assert repr(cell) == expected

    def test_repr_hidden(self):
        """Test repr for a default cell."""
        cell = Cell(0, 0)
        expected = "Cell(0,0) mine=False state=hidden"
        assert repr(cell) == expected

    def test_to_dict(self):
        """Test serialization of a Cell to a dictionary."""
        cell = Cell(3, 4)
        cell.is_mine = True
        cell.state = CellState.FLAGGED
        cell.adjacent_mines = 5

        data = cell.to_dict()

        assert data["row"] == 3
        assert data["col"] == 4
        assert data["is_mine"] is True
        assert data["state"] == "flagged"
        assert data["adjacent_mines"] == 5

    def test_from_dict(self):
        """Test deserialization of a Cell from a dictionary."""
        data = {
            "row": 7,
            "col": 8,
            "is_mine": True,
            "state": "revealed",
            "adjacent_mines": 3,
        }

        cell = Cell.from_dict(data)

        assert cell.row == 7
        assert cell.col == 8
        assert cell.is_mine is True
        assert cell.state == CellState.REVEALED
        assert cell.adjacent_mines == 3

    def test_roundtrip_serialization(self):
        """Test that serializing and deserializing preserves all data."""
        original = Cell(2, 3)
        original.is_mine = True
        original.state = CellState.FLAGGED
        original.adjacent_mines = 6

        data = original.to_dict()
        restored = Cell.from_dict(data)

        assert restored.row == original.row
        assert restored.col == original.col
        assert restored.is_mine == original.is_mine
        assert restored.state == original.state
        assert restored.adjacent_mines == original.adjacent_mines

    def test_roundtrip_serialization_hidden(self):
        """Test roundtrip with a default (hidden) cell."""
        original = Cell(0, 0)
        data = original.to_dict()
        restored = Cell.from_dict(data)

        assert restored.row == 0
        assert restored.col == 0
        assert restored.is_mine is False
        assert restored.state == CellState.HIDDEN
        assert restored.adjacent_mines == 0
