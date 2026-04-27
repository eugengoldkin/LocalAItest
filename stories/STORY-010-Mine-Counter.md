# STORY-010-Mine-Counter

## Description
Implement a mine counter display that shows the number of remaining mines to be found, calculated as total mines minus total flags placed.

## Acceptance Criteria
- [ ] Mine counter displays the remaining mines (Total Mines - Total Flags)
- [ ] Counter updates in real-time as flags are placed or removed
- [ ] Counter supports negative numbers (e.g., -1) when more flags are placed than mines exist
- [ ] Counter resets to the total mine count on a new game
- [ ] Counter displays in a digital/numeric format
- [ ] Counter is visible and clearly labeled in the UI

## Tasks
- [ ] Create mine counter state in the game model
- [ ] Implement counter calculation (total mines - placed flags)
- [ ] Create counter display UI element
- [ ] Wire counter updates to flag placement/removal events
- [ ] Handle negative number display
- [ ] Wire counter reset to new game trigger
- [ ] Test counter accuracy with various flag combinations

## Dependencies
- STORY-005-Cell-Interaction
