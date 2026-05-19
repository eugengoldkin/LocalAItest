# STORY-015-Win-Loss-Visual-Feedback

## Description
Implement visual feedback for win and loss game states, including overlay messages, mine reveal on loss, and celebration on win.

## Acceptance Criteria
- [x] On loss: all mines are revealed on the board
- [x] On loss: incorrectly placed flags are marked (e.g., red X)
- [x] On loss: a "Game Over" message is displayed
- [x] On win: a "You Win!" message is displayed with elapsed time
- [x] On win: the New Game button becomes visually active
- [x] Game interaction is blocked during win/loss display
- [x] Visual feedback is clear and unambiguous

## Tasks
- [x] Implement mine reveal overlay for loss state
- [x] Implement incorrect flag marking (e.g., red X on wrong flags)
- [x] Create Game Over message UI component
- [x] Create You Win message UI component with timer display
- [x] Block cell interaction during game-end display
- [x] Wire New Game button activation on win/loss
- [x] Test visual feedback across all scenarios

## Implementation Notes
- Core logic for mine reveals, incorrect flag marking, and interaction blocking was already implemented in previous stories (STORY-008 and STORY-014).
- This story focused on integrating the elapsed time display into the `GameEndDialog` and ensuring proper data flow from `MainWindow`.
- `GameEndDialog` was updated to accept an `elapsed_time` parameter and render a `MM:SS` formatted time label on wins.
- `MainWindow._on_game_end` was updated to pass the elapsed time from `self.game_engine.get_elapsed_time()`.
- Comprehensive test coverage added in `test_story_015.py` (26 tests) covering dialog content, time formatting, grid visual states, and interaction blocking.
- All 26 new tests pass. All 277 existing tests pass.

## Dependencies
- STORY-008-Game-End-Conditions, STORY-012-New-Game-Button


