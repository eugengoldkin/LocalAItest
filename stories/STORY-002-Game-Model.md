# STORY-002-Game-Model

## Description
Implement the core game model including the grid data structure, cell states, and mine placement logic.

## Acceptance Criteria
- [x] Grid class supports configurable width and height
- [x] Cell class supports states: Hidden, Revealed, Flagged
- [x] Mines are placed randomly on the grid at initialization
- [x] Each cell calculates and stores the count of adjacent mines (8 neighbors: horizontal, vertical, diagonal)
- [x] Grid can be serialized/deserialized for state management

## Tasks
- [x] Implement `Cell` class with state management (Hidden, Revealed, Flagged)
- [x] Implement `Grid` class with configurable dimensions
- [x] Implement random mine placement algorithm
- [x] Implement adjacent mine counting logic for each cell
- [x] Add grid serialization methods (to_dict, from_dict)
- [x] Write unit tests for Cell and Grid classes

## Dependencies
- STORY-001-Project-Setup

