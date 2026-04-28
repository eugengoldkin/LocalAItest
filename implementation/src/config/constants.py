"""Minesweeper - Constants and visual configuration.

STORY-001-T4: Create config files for constants.
Visual standards from minesweeper.md §5:
- Number colors: 1=Blue, 2=Green, 3=Red, 4=DarkBlue, 5=Brown, 6=Cyan, 7=Black, 8=Gray
- Cell states must be visually distinct (Hidden, Revealed, Flagged, Mine)
"""

from __future__ import annotations

# Visual constants
CELL_SIZE: int = 30  # pixels
CELL_PADDING: int = 1

# Number colors as specified in minesweeper.md §5
NUMBER_COLORS: dict[int, str] = {
    1: "blue",
    2: "green",
    3: "red",
    4: "darkblue",
    5: "brown",
    6: "cyan",
    7: "black",
    8: "gray",
}

# Cell background colors
CELL_HIDDEN_COLOR: str = "c0c0c0"
CELL_REVEALED_COLOR: str = "d0d0d0"
CELL_FLAGGED_COLOR: str = "c0c0c0"
CELL_MINE_COLOR: str = "ff0000"
CELL_MINE_REVEALED_COLOR: str = "808080"

# Game over visual feedback colors (STORY-008)
CELL_CORRECTLY_FLAGGED_COLOR: str = "00ff00"  # Green background for correct flags
CELL_INCORRECTLY_FLAGGED_COLOR: str = "ff6666"  # Red tint for incorrect flags
CELL_WRONG_FLAG_MINE_COLOR: str = "ff0000"  # Mine symbol on incorrect flag
CELL_CORRECT_FLAG_MINE_COLOR: str = "000000"  # Black mine symbol on correct flag

# Dialog colors (STORY-008)
DIALOG_BG: str = "white"
DIALOG_WON_COLOR: str = "00aa00"
DIALOG_LOST_COLOR: str = "cc0000"
DIALOG_FONT: tuple = ("Arial", 14, "bold")
DIALOG_BUTTON_FONT: tuple = ("Arial", 12)
DIALOG_BUTTON_BG: str = "e0e0e0"
DIALOG_BUTTON_ACTIVE_BG: str = "c0c0c0"

# UI colors
BG_COLOR: str = "white"
BORDER_COLOR: str = "808080"
FRAME_BG: str = "e0e0e0"

# Font settings
CELL_FONT: str = "Courier 16 bold"
TITLE_FONT: tuple = ("Arial", 18, "bold")
HUD_FONT: tuple = ("Courier", 16)
