# STORY-008-Game-End-Conditions

## Description
Implement the win and loss conditions for the game, including detection, visual feedback, and game reset.

## Acceptance Criteria
- [x] Win condition: All non-mine cells are revealed → display win message
- [x] Loss condition: A mine is revealed → display loss message and reveal all mines
- [x] Game state transitions to "won" or "lost" and blocks further interaction
- [x] All mines are shown on the board after a loss (including incorrectly flagged cells)
- [x] Correctly flagged mines are visually distinguished from incorrectly placed flags on loss
- [x] Player can start a new game after winning or losing

## Tasks
- [x] Implement win condition check (compare revealed safe cells to total safe cells)
- [x] Implement loss condition trigger when a mine is clicked
- [x] Create win/loss message/dialog UI
- [x] Implement full mine reveal on game over
- [x] Visually distinguish correctly flagged vs. incorrectly flagged mines on loss
- [x] Block further cell interaction after game ends
- [x] Wire New Game button to reset the game state
- [x] Write unit tests for win/loss detection

## Dependencies
- STORY-006-Flood-Fill, STORY-007-First-Click-Safety

## Summary
Implemented complete game end conditions for the Minesweeper game, including win/loss detection, visual feedback, and game reset functionality.

## Changes Made

### 1. Core Game Engine (`implementation/src/core/game.py`)
- Added `correct_flags` and `incorrect_flags` tracking sets to `GameEngine`
- Updated `reset()` to clear flag tracking on game reset
- Enhanced `_reveal_all_mines()` to track which flags are correct vs incorrect
- Added `get_flag_feedback()` method to determine if a flagged cell is correct or incorrect

### 2. Visual Feedback (`implementation/src/config/constants.py`)
- Added game over visual feedback colors:
  - `CELL_CORRECTLY_FLAGGED_COLOR` (green) for correct flags
  - `CELL_INCORRECTLY_FLAGGED_COLOR` (red tint) for incorrect flags
  - `CELL_CORRECT_FLAG_MINE_COLOR` (black) for mine symbol on correct flags
  - `CELL_WRONG_FLAG_MINE_COLOR` (red) for mine symbol on incorrect flags
- Added dialog colors:
  - `DIALOG_BG`, `DIALOG_WON_COLOR`, `DIALOG_LOST_COLOR`
  - `DIALOG_FONT`, `DIALOG_BUTTON_FONT`, `DIALOG_BUTTON_BG`

### 3. Win/Loss Dialog (`implementation/src/ui/game_end_dialog.py`) - NEW FILE
- Created `GameEndDialog` class extending `tk.Toplevel`
- Shows "You Win!" (green) or "You Lose!" (red) message
- Includes "New Game" button that triggers game reset
- Modal dialog that blocks interaction with main window
- Supports Enter key to confirm and Escape key to close

### 4. Grid Frame Updates (`implementation/src/ui/grid_frame.py`)
- Updated `update_cell()` to show correct/incorrect flag feedback on game over
  - Correct flags: green background, black mine symbol
  - Incorrect flags: red tinted background, red X symbol
  - Normal flags: unchanged gray background
- Added `on_game_end` callback to GridFrame
- Updated `on_left_click()` to trigger game end dialog when game is over

### 5. Main Window Updates (`implementation/src/ui/main_window.py`)
- Added `_on_game_end()` method to show appropriate dialog
- Wired `on_game_end` callback to GridFrame in `_build_ui()`
- Updated docstrings to reflect STORY-008 integration

### 6. Unit Tests (`implementation/tests/test_game_end.py`) - NEW FILE
- **TestLossCondition** (5 tests): Loss detection, all mines revealed, game over state
- **TestCorrectIncorrectFlags** (5 tests): Flag feedback detection
- **TestWinCondition** (5 tests): Win detection, partial reveal, game over prevention
- **TestGameReset** (5 tests): Reset clears all game state
- **TestWinWithFlags** (2 tests): Winning with flags placed

## Acceptance Criteria Status
- ✅ Win condition: All non-mine cells are revealed → display win message
- ✅ Loss condition: A mine is revealed → display loss message and reveal all mines
- ✅ Game state transitions to "won" or "lost" and blocks further interaction
- ✅ All mines are shown on the board after a loss (including incorrectly flagged cells)
- ✅ Correctly flagged mines are visually distinguished from incorrectly placed flags on loss
- ✅ Player can start a new game after winning or losing

## Test Results
- 108 tests pass (including 22 new STORY-008 tests)
- No regressions in existing tests

## Notes
- The win condition requires ALL non-mine cells to be revealed (flagged cells don't count)
- On loss, correctly flagged mines show green background with black mine symbol
- On loss, incorrectly flagged cells show red tint with red X symbol
- The dialog is modal, preventing further interaction until "New Game" is clicked