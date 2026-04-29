"""Minesweeper - HUD (Heads-Up Display) component.

STORY-001-T2: Create base module files: ui.py (stubbed as hud.py).
STORY-009: Implement timer display in MM:SS format.
STORY-010: Implement mine counter display.
Tkinter frame showing mine counter and timer.
"""

from __future__ import annotations

import tkinter as tk
from typing import Optional


class HUD(tk.Frame):
    """Heads-up display showing mine counter and timer.

    Attributes:
        master: The parent widget.
        mine_counter_label: Label displaying remaining mines.
        timer_label: Label displaying elapsed time in MM:SS format.
    """

    def __init__(self, master: tk.Widget) -> None:
        """Initialize the HUD.

        Args:
            master: The parent Tkinter widget.

        STORY-001-T2: Stub implementation for HUD.__init__().
        STORY-009: Initialize timer label with proper formatting.
        """
        super().__init__(master)

        self.mine_counter_label: tk.Label = tk.Label(
            self, text="Mines: 0", font=("Courier", 16)
        )
        self.mine_counter_label.pack(side=tk.LEFT, padx=10)

        self.timer_label: tk.Label = tk.Label(self, text="00:00", font=("Courier", 16))
        self.timer_label.pack(side=tk.RIGHT, padx=10)

    def update_mine_counter(self, count: int) -> None:
        """Update the mine counter display.

        Supports negative numbers (e.g., -1) when more flags are placed
        than mines exist.

        Args:
            count: The number of remaining mines (can be negative).
        """
        self.mine_counter_label.config(text=f"Mines: {count}")

    def update_timer(self, elapsed_seconds: int) -> None:
        """Update the timer display in MM:SS format.

        STORY-009: Update timer display with elapsed time.
        Time is formatted as MM:SS (e.g., 01:23, 16:39).
        Maximum time is 999 seconds (16:39).

        Args:
            elapsed_seconds: The elapsed time in seconds.
        """
        # Cap at maximum time (999 seconds = 16:39)
        time = min(elapsed_seconds, 999)
        minutes = time // 60
        seconds = time % 60
        formatted_time = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=formatted_time)
