# STORY-010-Mine-Counter

## Description
Implement a mine counter display that shows the number of remaining mines to be found, calculated as total mines minus total flags placed.

## Acceptance Criteria
- [x] `HUD` component calculates remaining mines as `total_mines - flags_placed`
- [x] Counter updates instantly when `GridFrame` triggers `on_mine_counter_update` callback
- [x] Counter supports negative values (e.g., "-1") when user over-flags
- [x] Counter resets to `total_mines` on `start_new_game()` or `change_difficulty()`
- [x] Counter displays using a monospaced/digital font for fixed-width alignment
- [x] Counter is visible in the `HUD` frame at the top of the `MainWindow`

## Tasks
- [x] Create mine counter state in the game model
- [x] Implement counter calculation (total mines - placed flags)
- [x] Create counter display UI element
- [x] Wire counter updates to flag placement/removal events
- [x] Handle negative number display
- [x] Wire counter reset to new game trigger
- [x] Test counter accuracy with various flag combinations

## Dependencies
- STORY-005-Cell-Interaction

