# STORY-016-Bug-Fix-Flaky-Test-Reveal-Revealed-Cell

## Description
Fix the flaky test `test_reveal_revealed_cell_does_nothing` in `test_game_engine.py`. The test was intermittently failing because `place_mines(0, 0)` randomly placed mines on the grid, and if position (5, 5) happened to be selected as a mine, the subsequent `reveal_cell(5, 5)` call would trigger game over instead of revealing the cell.

## Root Cause
The test called `engine.place_mines(0, 0)` which excludes only the cell at (0, 0) and its 8 neighbors from mine placement. The test then called `engine.reveal_cell(5, 5)`, expecting the cell to be safely revealed. However, since (5, 5) was not in the exclusion zone, it could randomly be placed as a mine, causing:

1. First `reveal_cell(5, 5)` triggers game over (hits a mine)
2. Second `reveal_cell(5, 5)` returns `None` (game over blocks reveals)
3. Assertion `result == CellState.REVEALED` fails

This made the test flaky - it would pass when (5, 5) was not a mine and fail when it was.

## Acceptance Criteria
- [ ] Test `test_reveal_revealed_cell_does_nothing` passes consistently (100% of runs)
- [ ] Test `test_reveal_revealed_cell_does_nothing` does not trigger game over
- [ ] All 214 tests in the test suite pass
- [ ] No new test failures introduced

## Implementation

### Fix Applied
Changed `engine.place_mines(0, 0)` to `engine.place_mines(5, 5)` in the test.

**Before:**
```python
def test_reveal_revealed_cell_does_nothing(self):
    """AC2: Left-click on a revealed cell does nothing."""
    engine = GameEngine(9, 9, 10)
    engine.place_mines(0, 0)  # Excludes (0,0) area only

    engine.reveal_cell(5, 5)
    result = engine.reveal_cell(5, 5)

    assert result == CellState.REVEALED  # Could fail if (5,5) was a mine
```

**After:**
```python
def test_reveal_revealed_cell_does_nothing(self):
    """AC2: Left-click on a revealed cell does nothing."""
    engine = GameEngine(9, 9, 10)
    engine.place_mines(5, 5)  # Excludes (5,5) and its neighbors - safe zone
    engine.first_click_done = True  # Prevent double mine placement on reveal

    engine.reveal_cell(5, 5)
    result = engine.reveal_cell(5, 5)

    assert result == CellState.REVEALED  # Guaranteed safe
```

### Key Changes
1. **`place_mines(5, 5)`**: Places mines while excluding (5, 5) and its 8 neighbors from mine placement, guaranteeing the cell is safe.
2. **`first_click_done = True`**: Prevents `reveal_cell()` from triggering a second random mine placement, which could overwrite the safe zone.

## Test Results
All 214 tests pass consistently after the fix:

```
implementation/tests/test_game_engine.py::TestRevealCell::test_reveal_revealed_cell_does_nothing PASSED
...
214 passed in 4.63s
```

## Files Modified
- `implementation/tests/test_game_engine.py` - Fixed `test_reveal_revealed_cell_does_nothing` in `TestRevealCell` class

## Lessons Learned
- When writing tests that depend on specific cell states, ensure the test setup guarantees those states rather than relying on random outcomes.
- Use `place_mines(row, col)` with the target cell as the exclusion parameter when testing that cell's behavior.
- Always set `first_click_done = True` when manually placing mines to prevent the game engine from overriding the setup.

## Dependencies
- STORY-005: Cell Interaction (provides `place_mines` and `reveal_cell` mechanics)
- STORY-007: First-Click Safety (provides the safe zone mechanism)
