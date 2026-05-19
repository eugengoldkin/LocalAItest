"""Minesweeper - Win/Loss Dialog.

STORY-008: Win/loss message dialog UI.
STORY-015: Visual feedback for win/loss states including elapsed time display.
Shows a popup dialog when the player wins or loses.
"""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from src.config.constants import (
    DIALOG_BG,
    DIALOG_BUTTON_ACTIVE_BG,
    DIALOG_BUTTON_FONT,
    DIALOG_BUTTON_BG,
    DIALOG_FONT,
    DIALOG_LOST_COLOR,
    DIALOG_WON_COLOR,
    HUD_FONT,
)


class GameEndDialog(tk.Toplevel):
    """A dialog window shown on game over (win or loss).

    Attributes:
        master: The parent Tkinter widget.
        result_callback: Callback invoked when the player clicks "New Game".
        won: Whether the player won the game.
        elapsed_time: Elapsed time in seconds (shown on win).
    """

    def __init__(
        self,
        master: tk.Widget,
        won: bool,
        result_callback: Optional[tk.Callable[[], None]] = None,
        elapsed_time: int = 0,
    ) -> None:
        """Initialize the GameEndDialog.

        Args:
            master: The parent Tkinter widget.
            won: Whether the player won the game.
            result_callback: Optional callback for the "New Game" button.
            elapsed_time: Elapsed time in seconds when the game ended.
        """
        super().__init__(master)
        self.won = won
        self.result_callback = result_callback
        self.elapsed_time = elapsed_time

        self.title("Game Over")
        self.resizable(False, False)

        # Center the dialog on screen
        self.update_idletasks()
        width = 300
        height = 180
        x = self.winfo_x() + (self.winfo_width() - width) // 2
        y = self.winfo_y() + (self.winfo_height() - height) // 2
        self.geometry(f"+{x}+{y}")

        # Message label
        if won:
            message = "You Win!"
            color = DIALOG_WON_COLOR
        else:
            message = "You Lose!"
            color = DIALOG_LOST_COLOR

        self.message_label = tk.Label(
            self,
            text=message,
            font=DIALOG_FONT,
            fg=color,
            bg=DIALOG_BG,
        )
        self.message_label.pack(pady=(15, 5))

        # Time label (only shown on win)
        self.time_label: Optional[tk.Label] = None
        if won:
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            time_text = f"{minutes:02d}:{seconds:02d}"
            self.time_label = tk.Label(
                self,
                text=f"Time: {time_text}",
                font=HUD_FONT,
                fg="#333333",
                bg=DIALOG_BG,
            )
            self.time_label.pack(pady=(0, 5))

        # "New Game" button
        self.new_game_btn = tk.Button(
            self,
            text="New Game",
            font=DIALOG_BUTTON_FONT,
            bg=DIALOG_BUTTON_BG,
            activebackground=DIALOG_BUTTON_ACTIVE_BG,
            command=self._on_new_game,
            relief=tk.RAISED,
            bd=2,
        )
        self.new_game_btn.pack(pady=(5, 10))

        # Focus the button so Enter key triggers it
        self.new_game_btn.focus_set()
        self.bind("<Return>", lambda e: self._on_new_game())
        self.bind("<Escape>", lambda e: self.destroy())

    def _on_new_game(self) -> None:
        """Handle the New Game button click."""
        if self.result_callback:
            self.result_callback()
        self.destroy()
