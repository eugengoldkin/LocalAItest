# STORY-007-First-Click-Safety

## Description
Ensure the first click of the game never lands on a mine, and ideally never lands on a cell with 0 adjacent mines to provide a good starting experience.

## Acceptance Criteria
- [ ] Mines are generated after the first click (not at initialization)
- [ ] The first clicked cell is guaranteed to not contain a mine
- [ ] The first clicked cell and its neighbors are also guaranteed to be mine-free
- [ ] The game starts with the timer only after the first click
- [ ] Subsequent clicks follow normal game rules (can hit mines)

## Tasks
- [ ] Defer mine generation until the first click occurs
- [ ] Create a safe zone around the first clicked cell (no mines in clicked cell or adjacent cells)
- [ ] Generate mines randomly in the remaining cells after safe zone is established
- [ ] Start the timer on the first click
- [ ] Test with multiple first clicks to verify no mine placement on first click
- [ ] Test that safe zone works on grid edges and corners

## Dependencies
- STORY-005-Cell-Interaction
