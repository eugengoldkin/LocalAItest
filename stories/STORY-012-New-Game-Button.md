# STORY-012-New-Game-Button

## Description
Implement a New Game button (traditionally a smiley face icon) that resets and restarts the game with the currently selected difficulty settings.

## Acceptance Criteria
- [ ] New Game button is visible and accessible in the UI
- [ ] Clicking the button resets the game board (new grid, new mine placement)
- [ ] Game resets to the currently selected difficulty (preset or custom)
- [ ] Timer resets to 00:00
- [ ] Mine counter resets to total mine count
- [ ] Game state resets to "playing" (no win/loss overlay)
- [ ] Button provides visual feedback on click (e.g., smiley face changes expression)

## Tasks
- [ ] Create New Game button UI element (smiley face icon recommended)
- [ ] Implement reset logic (grid, timer, mine counter, game state)
- [ ] Wire button click to reset handler
- [ ] Add visual feedback on button press
- [ ] Test reset behavior with various game states and difficulties
- [ ] Ensure first-click safety is re-established on new game

## Dependencies
- STORY-008-Game-End-Conditions, STORY-009-Timer, STORY-010-Mine-Counter
