# STORY-009-Timer

## Description
Implement a game timer that starts on the first click and stops when the game ends, displaying elapsed time in MM:SS format.

## Acceptance Criteria
- [ ] Timer starts counting on the first click of the game
- [ ] Timer stops when the game is won or lost
- [ ] Timer displays in MM:SS format (e.g., 01:23)
- [ ] Timer resets to 00:00 on a new game
- [ ] Timer updates at least once per second
- [ ] Maximum timer value is 999 seconds (standard Minesweeper limit)

## Tasks
- [ ] Create timer state variable in the game model
- [ ] Implement timer start logic (triggered on first click)
- [ ] Implement timer stop logic (triggered on win/loss)
- [ ] Implement timer reset logic (triggered on new game)
- [ ] Create timer display UI element
- [ ] Format time as MM:SS
- [ ] Cap timer at 999 seconds
- [ ] Test timer accuracy and behavior across game states

## Dependencies
- STORY-007-First-Click-Safety
