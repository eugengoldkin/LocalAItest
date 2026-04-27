# Minesweeper Game Requirements

## 1. Overview
The goal is to implement the classic Minesweeper game using Python. The game involves a grid of cells where some contain hidden mines. The player must reveal all safe cells without detonating a mine.

## 2. Functional Requirements

### 2.1 Grid & Initialization
- **Grid Dimensions**: The game board should be configurable based on the selected difficulty.
- **Mine Count**: The total number of mines depends on the difficulty level.
- **Randomization**: Mines must be placed randomly across the grid upon initialization. The first click must never be a mine (and ideally not a '0' to ensure a good start).

### 2.1.1 Difficulty Levels
The game must offer the following standard difficulty presets:
- **Beginner**: 9 columns, 9 rows, 10 mines.
- **Intermediate**: 16 columns, 16 rows, 40 mines.
- **Expert**: 30 columns, 16 rows, 99 mines.

### 2.1.2 Custom Difficulty
- **Custom Mode**: Allow the user to define:
  - Grid Width (minimum 9, maximum configurable limit).
  - Grid Height (minimum 9, maximum configurable limit).
  - Number of Mines (must be less than total cells, minimum 1).
- **Validation**: Input fields should prevent invalid entries (e.g., mines > total cells).
### 2.2 Cell States
Each cell must support the following states:
- **Hidden**: The default state; the content is unknown to the player.
- **Revealed**: The content (number or mine) is visible.
- **Flagged**: The player suspects a mine is present here (visual indicator required).
- **Question Mark**: (Optional) Intermediate state between hidden and flagged.

### 2.3 Core Gameplay Mechanics
- **Clicking a Mine**: If a player reveals a cell containing a mine, the game ends immediately (Loss). All mines on the board should be revealed.
- **Clicking a Number**: Reveals the specific cell, displaying the number of mines in adjacent cells (horizontal, vertical, and diagonal neighbors).
- **Clicking Empty Space (0)**: If a cell has 0 adjacent mines, it automatically reveals all adjacent cells. This process recurses until cells with numbers are reached (Flood Fill algorithm).
- **Flagging**: Players can toggle a flag on hidden cells via right-click. Flagged cells cannot be revealed by left-clicking.
- **Chording**: (Optional) If a numbered cell has the correct number of flags around it, clicking it reveals all remaining unflagged neighbors.

### 2.4 Game Logic
- **Win Condition**: The game is won when all non-mine cells are revealed.
- **Loss Condition**: The game is lost when a mine is revealed.
- **Timer**: A timer should track the duration of the game from the first move. It should stop when the game ends.

## 3. User Interface (UI) Requirements
- **Difficulty Menu**: A dropdown or button group to select between Beginner, Intermediate, Expert, and Custom.
- **Mine Counter**:
  - A digital display showing the number of remaining mines to be found.
  - Calculation: `Total Mines - Total Flags Placed`.
  - Should support negative numbers (e.g., -1) if the player places more flags than there are mines.
- **New Game Button**: A button (often a smiley face icon in classic versions) to restart the game with current settings.
- **Grid Layout**: The grid should resize dynamically based on the selected difficulty.
## 4. Technical Stack
- **Language**: Python 3.x
- **GUI Framework**: Tkinter (Standard library) or Pygame.
- **Data Structures**: 2D List or Array to represent the grid.

## 5. Non-Functional Requirements
- **Performance**: The game should respond to user inputs immediately without lag.
- **Usability**: Visual distinction between numbers (1-8) and colors. Clear icons for flags and mines.
- **Code Quality**: Modular design separating game logic (backend) from the user interface (frontend).

