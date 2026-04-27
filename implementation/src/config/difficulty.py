"""Minesweeper - Difficulty presets configuration.

STORY-001-T3: Choose GUI framework (Tkinter) and document decision.
STORY-001-T4: Create config files for difficulty presets.

Difficulty presets as defined in minesweeper.md section 2.1.1:
- Beginner: 9x9 grid, 10 mines
- Intermediate: 16x16 grid, 40 mines
- Expert: 30x16 grid, 99 mines
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Difficulty:
    """Represents a difficulty preset.

    Attributes:
        name: The display name of the difficulty.
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.
        mines: Number of mines on the board.
    """

    name: str
    rows: int
    cols: int
    mines: int


# GUI Framework Decision Document
# ===============================
# Framework: Tkinter (standard library)
#
# Rationale:
# - Tkinter is included with Python, requiring no external dependencies.
# - Sufficient for the Minesweeper game's widget needs (buttons, labels, frames).
# - Aligns with the project's technical stack requirements (minesweeper.md §4).
# - Simpler setup and maintenance compared to Pygame for a grid-based UI game.
# - Tkinter's grid/pack geometry managers map well to the Minesweeper board layout.
#
# Decision Date: 2025-01-01
# Author: Project Initiation


# Difficulty presets per minesweeper.md §2.1.1
DIFFICULTY_PRESETS: Dict[str, Difficulty] = {
    "Beginner": Difficulty(name="Beginner", rows=9, cols=9, mines=10),
    "Intermediate": Difficulty(name="Intermediate", rows=16, cols=16, mines=40),
    "Expert": Difficulty(name="Expert", rows=16, cols=30, mines=99),
}

# Default difficulty shown when the game starts
DEFAULT_DIFFICULTY: str = "Beginner"

# Custom difficulty validation limits
MIN_GRID_SIZE: int = 9
MAX_GRID_WIDTH: int = 50
MAX_GRID_HEIGHT: int = 50
MIN_MINES: int = 1
