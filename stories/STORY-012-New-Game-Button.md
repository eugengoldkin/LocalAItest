# STORY-012-New-Game-Button

## Description
Implement a New Game button (traditionally a smiley face icon) that resets and restarts the game with the currently selected difficulty settings.

## Acceptance Criteria
- [x] New Game button is visible and accessible in the UI
- [x] Clicking the button resets the game board (new grid, new mine placement)
- [x] Game resets to the currently selected difficulty (preset or custom)
- [x] Timer resets to 00:00
- [x] Mine counter resets to total mine count
- [x] Game state resets to "playing" (no win/loss overlay)
- [x] Button provides visual feedback on click (smiley face changes expression)

## Tasks
- [x] Create New Game button UI element (smiley face icon recommended)
- [x] Implement reset logic (grid, timer, mine counter, game state)
- [x] Wire button click to reset handler
- [x] Add visual feedback on button press
- [x] Test reset behavior with various game states and difficulties
- [x] Ensure first-click safety is re-established on new game

## Dependencies
- STORY-008-Game-End-Conditions, STORY-009-Timer, STORY-010-Mine-Counter
