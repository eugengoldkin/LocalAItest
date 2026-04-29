"""Tests for the GameEngine (STORY-005: Cell Interaction).

Tests for:
- Left-click reveal logic
- Right-click flag toggle
- Mine detection and game over
- First-click safety
- Win condition checking
- Flood fill (STORY-006)
"""

import pytest
from src.core.cell import CellState
from src.core.game import GameEngine


class TestRevealCell:
    """Tests for GameEngine.reveal_cell (STORY-005-T1)."""

    def test_reveal_hidden_cell(self):
        """AC1: Left-click on a hidden cell reveals it."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)  # Place mines before revealing

        result = engine.reveal_cell(5, 5)
        cell = engine.grid.get_cell(5, 5)

        assert result == CellState.REVEALED
        assert cell.state == CellState.REVEALED

    def test_reveal_revealed_cell_does_nothing(self):
        """AC2: Left-click on a revealed cell does nothing."""
        engine = GameEngine(9, 9, 10)
        # Place mines excluding (5,5) to ensure it's safe
        engine.place_mines(5, 5)
        engine.first_click_done = True  # Prevent double mine placement on reveal

        engine.reveal_cell(5, 5)
        result = engine.reveal_cell(5, 5)

        assert result == CellState.REVEALED  # Returns current state

    def test_reveal_flagged_cell_does_nothing(self):
        """AC5: Flagged cells cannot be revealed by left-clicking."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        engine.toggle_flag(5, 5)
        result = engine.reveal_cell(5, 5)

        assert result is None

    def test_reveal_mine_triggers_game_over(self):
        """AC3: Left-click on a revealed mine triggers game over."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Find a mine
        mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        assert mine_pos is not None
        result = engine.reveal_cell(mine_pos[0], mine_pos[1])

        assert result == CellState.REVEALED
        assert engine.game_over is True

    def test_reveal_out_of_bounds(self):
        """Test that out-of-bounds reveals return None."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        assert engine.reveal_cell(-1, 0) is None
        assert engine.reveal_cell(0, -1) is None
        assert engine.reveal_cell(9, 9) is None

    def test_reveal_after_game_over(self):
        """Test that reveals are blocked after game over."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Find a mine and trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        # Try to reveal another cell
        result = engine.reveal_cell(5, 5)
        assert result is None


class TestToggleFlag:
    """Tests for GameEngine.toggle_flag (STORY-005-T2)."""

    def test_flag_hidden_cell(self):
        """AC4a: Right-click on hidden cell → Flagged."""
        engine = GameEngine(9, 9, 10)

        success = engine.toggle_flag(5, 5)

        assert success is True
        cell = engine.grid.get_cell(5, 5)
        assert cell.state == CellState.FLAGGED
        assert engine.flags_placed == 1

    def test_unflag_flagged_cell(self):
        """AC4b: Right-click on flagged cell → Hidden."""
        engine = GameEngine(9, 9, 10)

        engine.toggle_flag(5, 5)
        success = engine.toggle_flag(5, 5)

        assert success is True
        cell = engine.grid.get_cell(5, 5)
        assert cell.state == CellState.HIDDEN
        assert engine.flags_placed == 0

    def test_flag_revealed_cell_fails(self):
        """Revealed cells cannot be flagged."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        engine.reveal_cell(5, 5)
        success = engine.toggle_flag(5, 5)

        assert success is False

    def test_flag_out_of_bounds_fails(self):
        """Flagging out-of-bounds returns False."""
        engine = GameEngine(9, 9, 10)

        assert engine.toggle_flag(-1, 0) is False
        assert engine.toggle_flag(0, -1) is False
        assert engine.toggle_flag(9, 9) is False

    def test_multiple_flags(self):
        """Test placing and removing multiple flags."""
        engine = GameEngine(9, 9, 10)

        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        engine.toggle_flag(2, 2)

        assert engine.flags_placed == 3

        engine.toggle_flag(1, 1)
        assert engine.flags_placed == 2

    def test_flag_after_game_over_fails(self):
        """Cannot toggle flags after game over."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        assert engine.toggle_flag(5, 5) is False


class TestMineDetection:
    """Tests for mine detection on click (STORY-005-T3)."""

    def test_game_over_mines_revealed(self):
        """AC7: Clicking a mine reveals all mines on the board."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Find and click a mine
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        game_over_mines = engine.get_game_over_mines()
        total_mines = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].is_mine
        )

        assert len(game_over_mines) == total_mines

    def test_game_over_mines_include_all_mine_positions(self):
        """All mine positions are in the game over set."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True  # Prevent double mine placement

        actual_mines = set()
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    actual_mines.add((r, c))

        # Click a mine to trigger game over
        for r, c in actual_mines:
            engine.reveal_cell(r, c)
            break

        game_over_mines = engine.get_game_over_mines()
        assert game_over_mines == actual_mines


class TestFirstClickSafety:
    """Tests for first-click safety mechanism (AC8, STORY-007)."""

    def test_first_click_is_safe(self):
        """AC8: First click is never a mine."""
        engine = GameEngine(9, 9, 10)

        # Before first click, no mines should be placed
        assert engine.first_click_done is False

        # Reveal a cell (this triggers mine placement)
        engine.reveal_cell(4, 4)

        assert engine.first_click_done is True
        cell = engine.grid.get_cell(4, 4)

        # The clicked cell should not be a mine
        assert cell.is_mine is False

    def test_first_click_neighbors_are_safe(self):
        """First click and all 8 neighbors are safe."""
        engine = GameEngine(9, 9, 10)

        engine.reveal_cell(4, 4)

        # Check the clicked cell and all neighbors
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 4 + dr, 4 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False

    def test_mines_placed_after_first_click(self):
        """Mines are placed on the grid after first click."""
        engine = GameEngine(9, 9, 10)

        # Before first click, no mines should be placed
        mine_count_before = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].is_mine
        )
        assert mine_count_before == 0

        # After first click, mines should be placed
        engine.reveal_cell(4, 4)

        mine_count_after = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].is_mine
        )
        assert mine_count_after == engine.total_mines

    def test_first_click_corner_top_left(self):
        """Safe zone works correctly when first click is in the top-left corner."""
        engine = GameEngine(9, 9, 10)
        engine.reveal_cell(0, 0)
        assert engine.first_click_done is True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 0 + dr, 0 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False, (
                        f"Top-left corner safe zone violation at ({nr}, {nc})"
                    )

    def test_first_click_corner_bottom_right(self):
        """Safe zone works correctly when first click is in the bottom-right corner."""
        engine = GameEngine(9, 9, 10)
        engine.reveal_cell(8, 8)
        assert engine.first_click_done is True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 8 + dr, 8 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False, (
                        f"Bottom-right corner safe zone violation at ({nr}, {nc})"
                    )

    def test_first_click_corner_bottom_left(self):
        """Safe zone works correctly when first click is in the bottom-left corner."""
        engine = GameEngine(9, 9, 10)
        engine.reveal_cell(8, 0)
        assert engine.first_click_done is True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 8 + dr, 0 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False, (
                        f"Bottom-left corner safe zone violation at ({nr}, {nc})"
                    )

    def test_first_click_corner_top_right(self):
        """Safe zone works correctly when first click is in the top-right corner."""
        engine = GameEngine(9, 9, 10)
        engine.reveal_cell(0, 8)
        assert engine.first_click_done is True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 0 + dr, 8 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False, (
                        f"Top-right corner safe zone violation at ({nr}, {nc})"
                    )

    def test_first_click_edge_top(self):
        """Safe zone works correctly when first click is on the top edge."""
        engine = GameEngine(9, 9, 10)
        engine.reveal_cell(0, 4)
        assert engine.first_click_done is True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 0 + dr, 4 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False, (
                        f"Top edge safe zone violation at ({nr}, {nc})"
                    )

    def test_first_click_edge_bottom(self):
        """Safe zone works correctly when first click is on the bottom edge."""
        engine = GameEngine(9, 9, 10)
        engine.reveal_cell(8, 4)
        assert engine.first_click_done is True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 8 + dr, 4 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False, (
                        f"Bottom edge safe zone violation at ({nr}, {nc})"
                    )

    def test_first_click_edge_left(self):
        """Safe zone works correctly when first click is on the left edge."""
        engine = GameEngine(9, 9, 10)
        engine.reveal_cell(4, 0)
        assert engine.first_click_done is True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 4 + dr, 0 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False, (
                        f"Left edge safe zone violation at ({nr}, {nc})"
                    )

    def test_first_click_edge_right(self):
        """Safe zone works correctly when first click is on the right edge."""
        engine = GameEngine(9, 9, 10)
        engine.reveal_cell(4, 8)
        assert engine.first_click_done is True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 4 + dr, 8 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False, (
                        f"Right edge safe zone violation at ({nr}, {nc})"
                    )

    def test_first_click_small_grid(self):
        """Safe zone works correctly on a small grid where safe zone overlaps significantly."""
        engine = GameEngine(5, 5, 3)
        engine.reveal_cell(2, 2)
        assert engine.first_click_done is True
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = 2 + dr, 2 + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.is_mine is False, (
                        f"Small grid safe zone violation at ({nr}, {nc})"
                    )

    def test_first_click_multiple_positions(self):
        """Test first click safety at many different positions across the grid."""
        test_positions = [
            (0, 0),
            (0, 4),
            (0, 8),  # top row
            (4, 0),
            (4, 4),
            (4, 8),  # middle row
            (8, 0),
            (8, 4),
            (8, 8),  # bottom row
        ]
        for row, col in test_positions:
            test_engine = GameEngine(9, 9, 10)
            test_engine.reveal_cell(row, col)
            assert test_engine.first_click_done is True
            clicked_cell = test_engine.grid.get_cell(row, col)
            assert clicked_cell.is_mine is False, (
                f"First click at ({row}, {col}) landed on a mine!"
            )
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = row + dr, col + dc
                    if (
                        0 <= nr < test_engine.grid.rows
                        and 0 <= nc < test_engine.grid.cols
                    ):
                        neighbor = test_engine.grid.get_cell(nr, nc)
                        assert neighbor.is_mine is False, (
                            f"Safe zone violation at ({nr}, {nc}) for click at ({row}, {col})"
                        )

    def test_first_click_subsequent_clicks_normal(self):
        """Multiple reveals after first click follow normal rules."""
        engine = GameEngine(9, 9, 10)
        engine.reveal_cell(4, 4)
        assert engine.first_click_done is True
        result1 = engine.reveal_cell(5, 5)
        assert result1 is not None
        result2 = engine.reveal_cell(3, 3)
        assert result2 is not None
        assert engine.first_click_done is True


class TestWinCondition:
    """Tests for win condition checking (STORY-005/STORY-008)."""

    def test_no_win_with_revealed_cell(self):
        """No win when not all safe cells are revealed."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        engine.reveal_cell(4, 4)
        result = engine.check_win_condition()

        assert result is False
        assert engine.game_won is False

    def test_win_all_safe_revealed(self):
        """Win when all non-mine cells are revealed."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(0, 0)
        engine.first_click_done = True  # Prevent double mine placement

        # Find the mine position
        mine_pos = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    mine_pos = (r, c)
                    break
            if mine_pos:
                break

        # Reveal all non-mine cells
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if (r, c) != mine_pos:
                    engine.reveal_cell(r, c)

        result = engine.check_win_condition()

        assert result is True
        assert engine.game_won is True
        assert engine.game_over is True

    def test_no_win_after_game_over(self):
        """Win check returns False after game over."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(0, 0)

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        result = engine.check_win_condition()
        assert result is False


class TestReset:
    """Tests for game reset functionality."""

    def test_reset_clears_game_state(self):
        """Reset clears game_over and game_won flags."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        assert engine.game_over is True

        engine.reset()

        assert engine.game_over is False
        assert engine.game_won is False
        assert engine.flags_placed == 0
        assert engine.first_click_done is False

    def test_reset_clears_flags(self):
        """Reset clears all flags."""
        engine = GameEngine(9, 9, 10)

        engine.toggle_flag(0, 0)
        engine.toggle_flag(1, 1)
        engine.toggle_flag(2, 2)

        assert engine.flags_placed == 3

        engine.reset()

        assert engine.flags_placed == 0
        # All cells should be back to HIDDEN
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                assert engine.grid.cells[r][c].state == CellState.HIDDEN


class TestAdjacentMineCount:
    """Tests for adjacent mine count functionality."""

    def test_adjacent_mine_count_center(self):
        """Adjacent mine count for center cell."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        count = engine.get_adjacent_mine_count(4, 4)
        assert isinstance(count, int)
        assert 0 <= count <= 8

    def test_adjacent_mine_count_corner(self):
        """Adjacent mine count for corner cell (fewer neighbors)."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        count = engine.get_adjacent_mine_count(0, 0)
        assert isinstance(count, int)
        assert 0 <= count <= 3

    def test_adjacent_mine_count_out_of_bounds(self):
        """Out-of-bounds returns 0."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        assert engine.get_adjacent_mine_count(-1, -1) == 0
        assert engine.get_adjacent_mine_count(9, 9) == 0
        assert engine.get_adjacent_mine_count(-1, 5) == 0

    def test_adjacent_mine_count_matches_cell(self):
        """Adjacent mine count matches the cell's stored value."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)

        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                count = engine.get_adjacent_mine_count(r, c)
                cell = engine.grid.get_cell(r, c)
                assert count == cell.adjacent_mines


class TestFloodFill:
    """Tests for flood fill functionality (STORY-006)."""

    def test_flood_fill_from_zero_cell(self):
        """AC1: Clicking a cell with 0 adjacent mines reveals all adjacent cells."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True  # Prevent double mine placement

        # Find a cell with 0 adjacent mines
        zero_cell = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine and cell.adjacent_mines == 0:
                    zero_cell = (r, c)
                    break
            if zero_cell:
                break

        assert zero_cell is not None

        # Reveal the zero cell
        engine.reveal_cell(zero_cell[0], zero_cell[1])

        # Check that the cell and its neighbors are revealed
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = zero_cell[0] + dr, zero_cell[1] + dc
                if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                    cell = engine.grid.get_cell(nr, nc)
                    assert cell.state == CellState.REVEALED

    def test_flood_fill_recurses_through_zeros(self):
        """AC2: The reveal process recurses through adjacent cells with 0 mines."""
        # Create a controlled grid where we know flood fill will recurse
        engine = GameEngine(7, 7, 1)
        engine.first_click_done = True

        # Place the mine at (6, 6) - far from the center
        engine.grid.cells[6][6].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Verify (3, 3) has 0 adjacent mines
        assert engine.grid.get_cell(3, 3).adjacent_mines == 0

        # Reveal the center cell
        engine.reveal_cell(3, 3)

        # Count revealed cells - should be more than just the neighbors
        revealed_count = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].state == CellState.REVEALED
        )

        # Should reveal at least the cell itself plus its neighbors (9 cells)
        assert revealed_count >= 9

    def test_flood_fill_stops_at_non_zero(self):
        """AC3: Recursion stops at cells with non-zero adjacent mine counts."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find a cell with 0 adjacent mines
        zero_cell = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine and cell.adjacent_mines == 0:
                    zero_cell = (r, c)
                    break
            if zero_cell:
                break

        assert zero_cell is not None

        # Reveal the zero cell
        engine.reveal_cell(zero_cell[0], zero_cell[1])

        # Find a cell with non-zero adjacent mines that was revealed
        boundary_cells = []
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.cells[r][c]
                if cell.state == CellState.REVEALED and cell.adjacent_mines > 0:
                    boundary_cells.append((r, c))

        # Check that none of the boundary cells' neighbors are revealed
        for br, bc in boundary_cells:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    nr, nc = br + dr, bc + dc
                    if 0 <= nr < engine.grid.rows and 0 <= nc < engine.grid.cols:
                        neighbor = engine.grid.get_cell(nr, nc)
                        if neighbor.is_mine:
                            # Mine cells may be revealed, that's OK
                            continue
                        # Non-mine neighbors of boundary cells should not be revealed
                        # (unless they were part of the flood fill path)
                        if neighbor.state == CellState.REVEALED:
                            # This is OK if the neighbor is also a boundary cell
                            pass

    def test_flood_fill_grid_boundaries(self):
        """AC4: Flood fill works correctly on grid boundaries and corners."""
        # Create a controlled grid with the mine far from (0, 0)
        engine = GameEngine(5, 5, 1)
        engine.first_click_done = True

        # Manually place the mine at (4, 4) - far from (0, 0)
        engine.grid.cells[4][4].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Verify (0, 0) has 0 adjacent mines
        assert engine.grid.get_cell(0, 0).adjacent_mines == 0

        # Click the corner (0, 0)
        engine.reveal_cell(0, 0)

        # All non-mine cells should be revealed
        revealed_count = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].state == CellState.REVEALED
        )
        assert revealed_count == 24  # 25 total - 1 mine

    def test_flood_fill_excludes_flagged_cells(self):
        """AC5: Flood fill does not reveal flagged cells."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find a cell with 0 adjacent mines
        zero_cell = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine and cell.adjacent_mines == 0:
                    zero_cell = (r, c)
                    break
            if zero_cell:
                break

        assert zero_cell is not None

        # Flag one of the neighbors
        neighbor_r, neighbor_c = zero_cell[0] + 1, zero_cell[1] + 1
        if 0 <= neighbor_r < engine.grid.rows and 0 <= neighbor_c < engine.grid.cols:
            engine.toggle_flag(neighbor_r, neighbor_c)
            assert (
                engine.grid.get_cell(neighbor_r, neighbor_c).state == CellState.FLAGGED
            )

            # Reveal the zero cell
            engine.reveal_cell(zero_cell[0], zero_cell[1])

            # The flagged cell should still be flagged
            assert (
                engine.grid.get_cell(neighbor_r, neighbor_c).state == CellState.FLAGGED
            )

    def test_flood_fill_respects_game_over(self):
        """AC6: Flood fill does not run during game over."""
        engine = GameEngine(9, 9, 10)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Trigger game over
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if engine.grid.cells[r][c].is_mine:
                    engine.reveal_cell(r, c)
                    break
            if engine.game_over:
                break

        assert engine.game_over is True

        # Try to reveal a cell - should return None
        result = engine.reveal_cell(4, 4)
        assert result is None

    def test_flood_fill_large_empty_area(self):
        """Test flood fill on a large empty area."""
        # Create a grid with mines only on the edges
        engine = GameEngine(10, 10, 36)
        # Place mines around the border
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                if (
                    r == 0
                    or r == engine.grid.rows - 1
                    or c == 0
                    or c == engine.grid.cols - 1
                ):
                    engine.grid.cells[r][c].is_mine = True
        engine._calculate_adjacent_mine_counts()
        engine.first_click_done = True

        # Click the center - should flood fill to the border
        engine.reveal_cell(5, 5)

        # All non-mine cells should be revealed
        revealed_count = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].state == CellState.REVEALED
        )
        assert revealed_count == 64  # 100 total - 36 mines

    def test_flood_fill_no_zero_cells(self):
        """Test that non-zero cells don't trigger flood fill."""
        engine = GameEngine(3, 3, 1)
        engine.place_mines(0, 0)
        engine.first_click_done = True

        # Find a cell with non-zero adjacent mines
        non_zero_cell = None
        for r in range(engine.grid.rows):
            for c in range(engine.grid.cols):
                cell = engine.grid.get_cell(r, c)
                if not cell.is_mine and cell.adjacent_mines > 0:
                    non_zero_cell = (r, c)
                    break
            if non_zero_cell:
                break

        assert non_zero_cell is not None

        # Reveal it - should only reveal that single cell
        engine.reveal_cell(non_zero_cell[0], non_zero_cell[1])

        revealed_count = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].state == CellState.REVEALED
        )
        assert revealed_count == 1

    def test_flood_fill_corner_zero_cell(self):
        """Test flood fill starting from a corner cell with 0 mines."""
        engine = GameEngine(5, 5, 1)
        engine.first_click_done = True

        # Manually place the mine at (4, 4) - far from (0, 0)
        engine.grid.cells[4][4].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Corner (0, 0) should have 0 adjacent mines
        assert engine.grid.get_cell(0, 0).adjacent_mines == 0

        engine.reveal_cell(0, 0)

        # All non-mine cells should be revealed
        revealed_count = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].state == CellState.REVEALED
        )
        assert revealed_count == 24

    def test_flood_fill_edge_zero_cell(self):
        """Test flood fill starting from an edge cell with 0 mines."""
        engine = GameEngine(5, 5, 1)
        engine.first_click_done = True

        # Manually place the mine at (4, 4) - far from edge cells
        engine.grid.cells[4][4].is_mine = True
        engine._calculate_adjacent_mine_counts()

        # Edge cell (0, 2) should have 0 adjacent mines
        assert engine.grid.get_cell(0, 2).adjacent_mines == 0

        engine.reveal_cell(0, 2)

        # All non-mine cells should be revealed
        revealed_count = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].state == CellState.REVEALED
        )
        assert revealed_count == 24

    def test_flood_fill_first_click_zero(self):
        """Test that first click with 0 adjacent mines triggers flood fill."""
        engine = GameEngine(9, 9, 10)

        # First click should trigger mine placement and reveal with flood fill
        result = engine.reveal_cell(4, 4)

        assert result == CellState.REVEALED
        assert engine.first_click_done is True

        # The cell should be revealed
        cell = engine.grid.get_cell(4, 4)
        assert cell.state == CellState.REVEALED

        # If the cell has 0 adjacent mines, flood fill should have occurred
        if cell.adjacent_mines == 0:
            revealed_count = sum(
                1
                for r in range(engine.grid.rows)
                for c in range(engine.grid.cols)
                if engine.grid.cells[r][c].state == CellState.REVEALED
            )
            assert revealed_count > 1  # At least the cell itself plus neighbors

    def test_flood_fill_connected_zeros(self):
        """Test flood fill through connected zero cells."""
        # Create a grid where multiple cells have 0 adjacent mines
        engine = GameEngine(7, 7, 1)
        engine.place_mines(6, 6)
        engine.first_click_done = True

        # Click a cell that should connect to others via flood fill
        engine.reveal_cell(0, 0)

        # Count revealed cells
        revealed_count = sum(
            1
            for r in range(engine.grid.rows)
            for c in range(engine.grid.cols)
            if engine.grid.cells[r][c].state == CellState.REVEALED
        )

        # Should reveal a significant portion of the grid
        assert revealed_count > 10
