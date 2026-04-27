"""Minesweeper - HUD (Heads-Up Display) component.

STORY-001-T2: Create base module files: ui.py (stubbed as hud.py).
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
        timer_label: Label displaying elapsed time.
    """

    def __init__(self, master: tk.Widget) -> None:
        """Initialize the HUD.

        Args:
            master: The parent Tkinter widget.

        STORY-001-T2: Stub implementation for HUD.__init__().
        """
        super().__init__(master)

        self.mine_counter_label: tk.Label = tk.Label(
            self, text="Mines: 0", font=("Courier", 16)
        )
        self.mine_counter_label.pack(side=tk.LEFT, padx=10)

        self.timer_label: tk.Label = tk.Label(
            self, text="Time: 0s", font=("Courier", 16)
        )
        self.timer_label.pack(side=tk.RIGHT, padx=10)

    def update_mine_counter(self, count: int) -> None:
        """Update the mine counter display.

        Args:
            count: The number of remaining mines.

        STORY-001-T2: Stub implementation for HUD.update_mine_counter().
        """
        # TODO: Implement mine counter update (STORY-010)
        pass

    def update_timer(self, seconds: int) -> None:
        """Update the timer display.

        Args:
            seconds: The elapsed time in seconds.

        STORY-001-T2: Stub implementation for HUD.update_timer().
        """
        # TODO: Implement timer update (STORY-009)
        pass
