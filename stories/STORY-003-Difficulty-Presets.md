# STORY-003-Difficulty-Presets

## Description
Implement the three standard difficulty presets: Beginner, Intermediate, and Expert.

## Acceptance Criteria
- [x] Beginner preset: 9 columns, 9 rows, 10 mines
- [x] Intermediate preset: 16 columns, 16 rows, 40 mines
- [x] Expert preset: 30 columns, 16 rows, 99 mines
- [x] Presets are selectable from the UI
- [x] Selecting a preset initializes a new game with those dimensions and mine count

## Tasks
- [x] Define difficulty preset constants/configuration
- [x] Create a `DifficultyManager` or configuration module for presets
- [x] Add UI elements (dropdown or buttons) to select difficulty presets
- [x] Wire preset selection to game initialization logic
- [x] Test each preset initializes the game correctly

## Dependencies
- STORY-002-Game-Model

