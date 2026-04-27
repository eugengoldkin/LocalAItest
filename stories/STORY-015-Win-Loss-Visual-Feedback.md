# STORY-015-Win-Loss-Visual-Feedback

## Description
Implement visual feedback for win and loss game states, including overlay messages, mine reveal on loss, and celebration on win.

## Acceptance Criteria
- [ ] On loss: all mines are revealed on the board
- [ ] On loss: incorrectly placed flags are marked (e.g., red X)
- [ ] On loss: a "Game Over" message is displayed
- [ ] On win: a "You Win!" message is displayed with elapsed time
- [ ] On win: the New Game button becomes visually active
- [ ] Game interaction is blocked during win/loss display
- [ ] Visual feedback is clear and unambiguous

## Tasks
- [ ] Implement mine reveal overlay for loss state
- [ ] Implement incorrect flag marking (e.g., red X on wrong flags)
- [ ] Create Game Over message UI component
- [ ] Create You Win message UI component with timer display
- [ ] Block cell interaction during game-end display
- [ ] Wire New Game button activation on win/loss
- [ ] Test visual feedback across all scenarios

## Dependencies
- STORY-008-Game-End-Conditions, STORY-012-New-Game-Button
