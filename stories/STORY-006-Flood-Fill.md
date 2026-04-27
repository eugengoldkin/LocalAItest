# STORY-006-Flood-Fill

## Description
Implement the flood fill algorithm that automatically reveals adjacent cells when a cell with 0 adjacent mines is clicked.

## Acceptance Criteria
- [x] Clicking a cell with 0 adjacent mines reveals all adjacent cells
- [x] The reveal process recurses through adjacent cells with 0 mines
- [x] Recursion stops at cells with non-zero adjacent mine counts
- [x] Flood fill works correctly on grid boundaries and corners
- [x] Flood fill does not reveal flagged cells
- [x] Flood fill respects game state (does not run during game over)

## Tasks
- [x] Implement recursive flood fill algorithm in the game model
- [x] Add boundary checking for grid edges
- [x] Ensure flagged cells are excluded from flood fill
- [x] Integrate flood fill into the cell click handler
- [x] Test flood fill on various grid configurations (edges, corners, large empty areas)
- [x] Optimize recursion to avoid stack overflow on large grids (consider iterative approach)

## Dependencies
- STORY-005-Cell-Interaction

## Implementation Notes
- Used **iterative BFS (Breadth-First Search)** approach with `collections.deque` instead of recursion to avoid stack overflow on large grids.
- Flood fill is triggered automatically in `reveal_cell()` when a cell with 0 adjacent mines is revealed.
- A `visited` set tracks processed cells to prevent infinite loops and redundant processing.
- Flagged cells are skipped during flood fill but are not treated as visited, so they act as natural boundaries.
