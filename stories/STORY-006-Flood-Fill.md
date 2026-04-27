# STORY-006-Flood-Fill

## Description
Implement the flood fill algorithm that automatically reveals adjacent cells when a cell with 0 adjacent mines is clicked.

## Acceptance Criteria
- [ ] Clicking a cell with 0 adjacent mines reveals all adjacent cells
- [ ] The reveal process recurses through adjacent cells with 0 mines
- [ ] Recursion stops at cells with non-zero adjacent mine counts
- [ ] Flood fill works correctly on grid boundaries and corners
- [ ] Flood fill does not reveal flagged cells
- [ ] Flood fill respects game state (does not run during game over)

## Tasks
- [ ] Implement recursive flood fill algorithm in the game model
- [ ] Add boundary checking for grid edges
- [ ] Ensure flagged cells are excluded from flood fill
- [ ] Integrate flood fill into the cell click handler
- [ ] Test flood fill on various grid configurations (edges, corners, large empty areas)
- [ ] Optimize recursion to avoid stack overflow on large grids (consider iterative approach)

## Dependencies
- STORY-005-Cell-Interaction
