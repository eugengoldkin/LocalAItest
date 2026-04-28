# STORY-004-Custom-Difficulty

## Description
Allow users to define a custom difficulty by specifying grid width, height, and number of mines.

## Acceptance Criteria
- [x] UI inputs are clearly labeled and easy to use
## Tasks
- [x] Create custom difficulty input UI (width, height, mine count fields)
- [x] Implement input validation logic (min/max bounds, mines < total cells)
- [x] Add validation error messages for invalid inputs
- [x] Wire custom input to game initialization
- [x] Test edge cases (minimum values, maximum values, invalid inputs)

## Dependencies
- STORY-003-Difficulty-Presets

## Status
**Completed** — All acceptance criteria met and all tests passing.

## Notes
- Fixed test file bug: `request.getfixturevalue("root")` was used without importing `request`. Replaced with a module-scoped `_shared_tk_root` fixture to avoid Tkinter Tcl library exhaustion from creating too many root windows.
