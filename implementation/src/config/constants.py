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

# UI colors
BG_COLOR: str = "white"
BORDER_COLOR: str = "808080"
FRAME_BG: str = "e0e0e0"

# Font settings
CELL_FONT: str = "Courier 16 bold"
TITLE_FONT: tuple = ("Arial", 18, "bold")
HUD_FONT: tuple = ("Courier", 16)
