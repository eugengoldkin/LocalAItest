# STORY-003-Difficulty-Presets

## Description
Implement the three standard difficulty presets: Beginner, Intermediate, and Expert.

## Acceptance Criteria
- [ ] Beginner preset: 9 columns, 9 rows, 10 mines
- [ ] Intermediate preset: 16 columns, 16 rows, 40 mines
- [ ] Expert preset: 30 columns, 16 rows, 99 mines
- [ ] Presets are selectable from the UI
- [ ] Selecting a preset initializes a new game with those dimensions and mine count

## Tasks
- [ ] Define difficulty preset constants/configuration
- [ ] Create a `DifficultyManager` or configuration module for presets
- [ ] Add UI elements (dropdown or buttons) to select difficulty presets
- [ ] Wire preset selection to game initialization logic
- [ ] Test each preset initializes the game correctly

## Dependencies
- STORY-002-Game-Model
