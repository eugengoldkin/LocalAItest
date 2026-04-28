# STORY-009-Timer

## Description
Implement a game timer that starts on the first click and stops when the game ends, displaying elapsed time in MM:SS format.

## Acceptance Criteria
- [x] Timer starts counting on the first click of the game
- [x] Timer stops when the game is won or lost
- [x] Timer displays in MM:SS format (e.g., 01:23)
- [x] Timer resets to 00:00 on a new game
- [x] Timer updates at least once per second
- [x] Maximum timer value is 999 seconds (standard Minesweeper limit)

## Tasks
- [x] Create timer state variable in the game model
- [x] Implement timer start logic (triggered on first click)
- [x] Implement timer stop logic (triggered on win/loss)
- [x] Implement timer reset logic (triggered on new game)
- [x] Create timer display UI element
- [x] Format time as MM:SS
- [x] Cap timer at 999 seconds
- [x] Test timer accuracy and behavior across game states

## Dependencies
- STORY-007-First-Click-Safety
