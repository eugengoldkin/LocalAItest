# STORY-005-Cell-Interaction

## Description
Implement the core cell interaction mechanics: revealing cells, flagging/unflagging, and handling clicks on mines and numbered cells.

## Acceptance Criteria
- [x] Left-click on a hidden cell reveals it
- [x] Left-click on a revealed numbered cell does nothing
- [x] Left-click on a revealed mine triggers game over
- [x] Right-click toggles flag on hidden cells (Hidden → Flagged → Hidden)
- [x] Flagged cells cannot be revealed by left-clicking
- [x] Revealed cells display the correct adjacent mine count (1-8)
- [x] Clicking a mine reveals all mines on the board (game over state)
- [x] First click is never a mine

## Tasks
- [x] Implement left-click event handler for revealing cells
- [x] Implement right-click event handler for toggling flags
- [x] Implement mine detection on click (game over condition)
- [x] Implement first-click safety mechanism (generate mines after first click)
- [x] Add visual indicators for flagged cells
- [x] Add visual indicators for revealed numbered cells
- [x] Write unit tests for cell interaction logic

## Dependencies
- STORY-002-GameModel ✅

## Implementation Details

### Files Modified
- `src/core/game.py` - Implemented `reveal_cell()`, `toggle_flag()`, `check_win_condition()`, `get_game_over_mines()`, and first-click safety via `place_mines()`.
- `src/ui/grid_frame.py` - Implemented grid rendering with Tkinter buttons, left-click (`on_left_click`) and right-click (`on_right_click`) event bindings, and `update_cell()` for visual state changes.
- `src/ui/main_window.py` - Wired GameEngine to GridFrame and HUD components, added `start_new_game()` and `change_difficulty()` methods.

### Files Created
- `tests/test_game_engine.py` - 27 unit tests covering reveal logic, flag toggling, mine detection, first-click safety, win conditions, reset, and adjacent mine counts.

### Key Design Decisions
- First-click safety is enforced by deferring mine placement until `reveal_cell()` is first called, excluding the clicked cell and its 8 neighbors.
- Game over state reveals all mines via `_reveal_all_mines()`, tracking positions in `_game_over_mines`.
- Win condition checks after every reveal: all non-mine cells must be revealed.
- GridFrame handles its own rendering and event binding, delegating state changes to GameEngine.

