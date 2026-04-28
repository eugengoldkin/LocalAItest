# STORY-007-First-Click-Safety

## Description
Ensure the first click of the game never lands on a mine, and ideally never lands on a cell with 0 adjacent mines to provide a good starting experience.

## Acceptance Criteria
- [x] Mines are generated after the first click (not at initialization)
- [x] The first clicked cell is guaranteed to not contain a mine
- [x] The first clicked cell and its neighbors are also guaranteed to be mine-free
- [x] The game starts with the timer only after the first click
- [x] Subsequent clicks follow normal game rules (can hit mines)

## Tasks
- [x] Defer mine generation until the first click occurs
- [x] Create a safe zone around the first clicked cell (no mines in clicked cell or adjacent cells)
- [x] Generate mines randomly in the remaining cells after safe zone is established
- [x] Start the timer on the first click
- [x] Test with multiple first clicks to verify no mine placement on first click
- [x] Test that safe zone works on grid edges and corners

## Dependencies
- STORY-005-Cell-Interaction

