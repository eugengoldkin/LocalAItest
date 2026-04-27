# STORY-008-Game-End-Conditions

## Description
Implement the win and loss conditions for the game, including detection, visual feedback, and game reset.

## Acceptance Criteria
- [ ] Win condition: All non-mine cells are revealed → display win message
- [ ] Loss condition: A mine is revealed → display loss message and reveal all mines
- [ ] Game state transitions to "won" or "lost" and blocks further interaction
- [ ] All mines are shown on the board after a loss (including incorrectly flagged cells)
- [ ] Correctly flagged mines are visually distinguished from incorrectly placed flags on loss
- [ ] Player can start a new game after winning or losing

## Tasks
- [ ] Implement win condition check (compare revealed safe cells to total safe cells)
- [ ] Implement loss condition trigger when a mine is clicked
- [ ] Create win/loss message/dialog UI
- [ ] Implement full mine reveal on game over
- [ ] Visually distinguish correctly flagged vs. incorrectly flagged mines on loss
- [ ] Block further cell interaction after game ends
- [ ] Wire New Game button to reset the game state
- [ ] Write unit tests for win/loss detection

## Dependencies
- STORY-006-Flood-Fill, STORY-007-First-Click-Safety
