# STORY-002-Game-Model

## Description
Implement the core game model including the grid data structure, cell states, and mine placement logic.

## Acceptance Criteria
- [ ] Grid class supports configurable width and height
- [ ] Cell class supports states: Hidden, Revealed, Flagged
- [ ] Mines are placed randomly on the grid at initialization
- [ ] Each cell calculates and stores the count of adjacent mines (8 neighbors: horizontal, vertical, diagonal)
- [ ] Grid can be serialized/deserialized for state management

## Tasks
- [ ] Implement `Cell` class with state management (Hidden, Revealed, Flagged)
- [ ] Implement `Grid` class with configurable dimensions
- [ ] Implement random mine placement algorithm
- [ ] Implement adjacent mine counting logic for each cell
- [ ] Add grid serialization methods (to_dict, from_dict)
- [ ] Write unit tests for Cell and Grid classes

## Dependencies
- STORY-001-Project-Setup
