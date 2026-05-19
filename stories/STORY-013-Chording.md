# STORY-013-Chording

## Description
Implement the chording feature: when a numbered cell has the correct number of flags around it, clicking it reveals all remaining unflagged neighbors.

## Acceptance Criteria
- [x] Right-click on a revealed numbered cell triggers chording
- [x] Chording only activates when the number of adjacent flags matches the cell's mine count
- [x] All unflagged neighbors are revealed when chording activates
- [x] If chording triggers a mine, the game ends (loss)
- [x] If chording triggers flood fill (0 adjacent mines), flood fill is applied
- [x] Chording does nothing if the flag count doesn't match the cell's mine count
- [x] Chording is disabled during game over states

## Tasks
- [x] Implement right-click handler for revealed numbered cells
- [x] Add logic to compare adjacent flag count with cell's mine count
- [x] Implement neighbor reveal for matching chording cases
- [x] Integrate chording with flood fill for 0-count neighbors
- [x] Handle mine hits during chording (game over)
- [x] Add visual feedback for chording activation
- [x] Write unit tests for chording logic

## Dependencies
- STORY-005-Cell-Interaction, STORY-006-Flood-Fill

