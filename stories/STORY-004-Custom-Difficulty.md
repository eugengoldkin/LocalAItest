# STORY-004-Custom-Difficulty

## Description
Allow users to define a custom difficulty by specifying grid width, height, and number of mines.

## Acceptance Criteria
- [ ] User can input a custom grid width (minimum 9, maximum configurable limit)
- [ ] User can input a custom grid height (minimum 9, maximum configurable limit)
- [ ] User can input a custom mine count (minimum 1, must be less than total cells)
- [ ] Input validation prevents invalid entries (e.g., mines > total cells)
- [ ] Selecting Custom mode initializes a new game with the user-defined parameters
- [ ] UI inputs are clearly labeled and easy to use

## Tasks
- [ ] Create custom difficulty input UI (width, height, mine count fields)
- [ ] Implement input validation logic (min/max bounds, mines < total cells)
- [ ] Add validation error messages for invalid inputs
- [ ] Wire custom input to game initialization
- [ ] Test edge cases (minimum values, maximum values, invalid inputs)

## Dependencies
- STORY-003-Difficulty-Presets
