"""Minesweeper - Main window UI.

STORY-001-T2: Create base module files: ui.py (stubbed as main_window.py).
The main Tkinter application window.
"""

from __future__ import annotations

import tkinter as tk
from typing import Optional


class MainWindow:
    """The main Tkinter window for the Minesweeper game.

    Attributes:
        root: The root Tkinter window.
        game_frame: Frame containing the game grid.
        hud_frame: Frame containing the HUD (mine counter, timer).
    """

    def __init__(self) -> None:
        """Initialize the MainWindow.

        STORY-001-T2: Stub implementation for MainWindow.__init__().
        """
        self.root: tk.Tk = tk.Tk()
        self.root.title("Minesweeper")
        self.root.resizable(True, True)

        # Placeholder frames - to be implemented in STORY-014
        self.hud_frame: Optional[tk.Frame] = None
        self.game_frame: Optional[tk.Frame] = None

        self._build_ui()

    def _build_ui(self) -> None:
        """Build the initial UI structure.

        STORY-001-T2: Stub implementation for MainWindow._build_ui().
        Creates placeholder frames for future story implementations.
        """
        # HUD frame (for mine counter and timer) - STORY-009, STORY-010
        self.hud_frame = tk.Frame(self.root)
        self.hud_frame.pack(fill=tk.X, padx=10, pady=5)

        # Game grid frame - STORY-014
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

    def run(self) -> None:
        """Start the Tkinter event loop.

        STORY-001-T2: Stub implementation for MainWindow.run().
        """
        self.root.mainloop()

    def destroy(self) -> None:
        """Destroy the Tkinter window and clean up resources."""
        self.root.destroy()
