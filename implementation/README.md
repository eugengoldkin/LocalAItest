# Minesweeper

A classic Minesweeper game implemented in Python using Tkinter.

## Overview

Minesweeper is a single-player puzzle game where the player must reveal all safe cells on a grid without detonating hidden mines. Cells display the number of adjacent mines, and players use logic to deduce mine locations. Flags can be placed to mark suspected mines.

## Features

- Configurable difficulty levels (Beginner, Intermediate, Expert)
- Custom difficulty support
- Flood fill for empty cells
- First-click safety guarantee
- Timer and mine counter
- Flag placement and chording support

## Technical Stack

- **Language**: Python 3.x
- **GUI Framework**: Tkinter (standard library)
- **Architecture**: Separated backend (game logic) and frontend (UI)

## Directory Structure

```
implementation/
├── src/
│   ├── core/          # Game logic (Cell, Grid, GameEngine)
│   ├── ui/            # Tkinter widgets (MainWindow, GridFrame, HUD)
│   ├── config/        # Constants, difficulty presets
│   └── utils/         # Helper functions
├── tests/             # Unit and integration tests
├── assets/            # Icons, images
├── main.py            # Entry point
├── requirements.txt   # Dependencies (none - stdlib only)
└── README.md          # This file
```

## Setup & Installation

### Prerequisites

- Python 3.8 or higher

### Installation

1. Navigate to the `implementation/` directory:
   ```bash
   cd implementation
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     venv\Scripts\Activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

### Running the Game

```bash
cd implementation
python main.py
```

## Running Tests

```bash
cd implementation
python -m pytest tests/
```

## Development

### Code Style

This project follows [PEP 8](https://peps.python.org/pep-0008/) conventions.

### Architecture

- **Backend** (`src/core/`): Contains all game logic - `Cell`, `Grid`, and `GameEngine` classes.
- **Frontend** (`src/ui/`): Contains Tkinter UI components - `MainWindow`, `GridFrame`, and `HUD`.
- **Config** (`src/config/`): Stores difficulty presets, constants, and configuration.
- **Separation of Concerns**: Game state is managed in `src/core/`. The UI only reads state and renders it.

## Story Tracking

Implementation is organized into stories documented in the `stories/` directory:

- [Story List](../stories/storylist.md)
- Each story file includes acceptance criteria and tasks

## License

This project is open source.
