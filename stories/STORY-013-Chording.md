# STORY-013-Chording

## Description
Implement the chording feature: when a numbered cell has the correct number of flags around it, clicking it reveals all remaining unflagged neighbors.

## Acceptance Criteria
- [ ] Right-click on a revealed numbered cell triggers chording
- [ ] Chording only activates when the number of adjacent flags matches the cell's mine count
- [ ] All unflagged neighbors are revealed when chording activates
- [ ] If chording triggers a mine, the game ends (loss)
- [ ] If chording triggers flood fill (0 adjacent mines), flood fill is applied
- [ ] Chording does nothing if the flag count doesn't match the cell's mine count
- [ ] Chording is disabled during game over states

## Tasks
- [ ] Implement right-click handler for revealed numbered cells
- [ ] Add logic to compare adjacent flag count with cell's mine count
- [ ] Implement neighbor reveal for matching chording cases
- [ ] Integrate chording with flood fill for 0-count neighbors
- [ ] Handle mine hits during chording (game over)
- [ ] Add visual feedback for chording activation
- [ ] Write unit tests for chording logic

## Dependencies
- STORY-005-Cell-Interaction, STORY-006-Flood-Fill
