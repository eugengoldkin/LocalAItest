# STORY-017-Fix-Flaky-Gameplay-Test

## Description
The test `test_custom_difficulty_gameplay` in `test_custom_difficulty.py` is flaky because it assumes a specific cell `(5, 5)` will remain hidden after the first click at `(0, 0)`. Due to random mine placement and flood fill behavior, the first click might trigger a flood fill that reveals `(5, 5)`, causing the flag assertion to fail. This story updates the test to be deterministic and robust against grid state variations.

## Root Cause
The test hardcoded coordinates `(5, 5)` for flagging after the first click at `(0, 0)`. When the first click reveals a large area via flood fill (due to 0 adjacent mines), the hardcoded coordinate might fall within the revealed area. Attempting to flag an already-revealed cell returns `False`, causing the test to fail intermittently.

## Acceptance Criteria
- [ ] `test_custom_difficulty_gameplay` passes consistently in CI and local runs
- [ ] Test verifies that a game can be started, a cell revealed, and a flag placed on a hidden cell
- [ ] Test no longer relies on hardcoded coordinates that are sensitive to flood-fill behavior

## Tasks
- [ ] Update `test_custom_difficulty_gameplay` to find a hidden cell dynamically after the first click
- [ ] Assert that flagging that dynamic cell succeeds
- [ ] Verify all tests pass

## Implementation

### Fix Applied
Changed the test to dynamically find a hidden cell after the first click, rather than relying on hardcoded coordinates.

**Before:**
```python
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
```

**After:**
```python
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

    # Find a cell that is still hidden after the first click.
    # This avoids the flaky behavior where hardcoded coordinates
    # (e.g., 5, 5) might be revealed by flood fill.
    target_row, target_col = None, None
    for r in range(engine.grid.rows):
        for c in range(engine.grid.cols):
            if engine.grid.cells[r][c].state == CellState.HIDDEN:
                target_row, target_col = r, c
                break
        if target_row is not None:
            break

    # Assert that we found at least one hidden cell
    assert target_row is not None
    assert target_col is not None

    # Flag the hidden cell
    success = engine.toggle_flag(target_row, target_col)
    assert success is True
    assert engine.flags_placed == 1
```

### Key Changes
1. **Dynamic hidden cell search**: Iterates through all cells to find one that is still `HIDDEN` after the first click, guaranteeing that flagging will succeed.
2. **Assertion for hidden cell existence**: Explicitly asserts that at least one hidden cell exists, providing a clear failure message if something unexpected occurs.

## Test Results
All tests pass consistently after the fix.

## Files Modified
- `implementation/tests/test_custom_difficulty.py` - Fixed `test_custom_difficulty_gameplay` in `TestGameEngineWithCustomDifficulty` class

## Lessons Learned
- When writing tests that depend on specific cell states after game actions, dynamically verify the cell state rather than assuming hardcoded coordinates will remain in the expected state.
- Flood fill behavior can reveal large portions of the grid unpredictably; tests should account for this by finding cells that satisfy the required state at runtime.

## Dependencies
- STORY-004: Custom Difficulty (provides custom difficulty setup)
- STORY-006: Flood Fill (provides flood fill mechanics that cause the flakiness)
