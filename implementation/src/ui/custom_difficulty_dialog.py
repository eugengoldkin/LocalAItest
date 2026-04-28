"""Minesweeper - Custom Difficulty Dialog.

STORY-004: Custom difficulty input UI (width, height, mine count fields).

Provides a modal dialog for users to define custom grid dimensions
and mine count, with input validation.
"""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import dataclass
from typing import Optional, Tuple

from src.config.difficulty import (
    MAX_GRID_HEIGHT,
    MAX_GRID_WIDTH,
    MIN_GRID_SIZE,
    MIN_MINES,
)


@dataclass
class CustomDifficultyInput:
    """Represents validated custom difficulty input.

    Attributes:
        rows: Number of rows (height) for the grid.
        cols: Number of columns (width) for the grid.
        mines: Number of mines to place on the board.
    """

    rows: int
    cols: int
    mines: int


class CustomDifficultyDialog(tk.Toplevel):
    """Modal dialog for custom difficulty input.

    Provides three input fields:
    - Grid Width (columns)
    - Grid Height (rows)
    - Mine Count

    Validates inputs before allowing the user to proceed.

    Attributes:
        parent: The parent Tkinter widget.
        result: The validated CustomDifficultyInput, or None if cancelled.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """Initialize the CustomDifficultyDialog.

        Args:
            parent: The parent Tkinter window.
        """
        super().__init__(parent)
        self.title("Custom Difficulty")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

        self.result: Optional[CustomDifficultyInput] = None

        # Input variables
        self.cols_var: tk.StringVar = tk.StringVar(value=str(MIN_GRID_SIZE))
        self.rows_var: tk.StringVar = tk.StringVar(value=str(MIN_GRID_SIZE))
        self.mines_var: tk.StringVar = tk.StringVar(value=str(MIN_MINES))

        # Error message variable
        self.error_var: tk.StringVar = tk.StringVar()

        self._build_ui()
        self._center_dialog()
        self.grab_set()  # Modal: block interaction with main window
        self.focus_set()

    def _build_ui(self) -> None:
        """Build the dialog UI with input fields and buttons."""
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Grid Width input
        ttk.Label(main_frame, text="Grid Width (columns):").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        cols_entry = ttk.Entry(
            main_frame,
            textvariable=self.cols_var,
            width=15,
        )
        cols_entry.grid(row=0, column=1, pady=5)
        cols_entry.bind("<KeyRelease>", self._validate_on_change)

        # Grid Height input
        ttk.Label(main_frame, text="Grid Height (rows):").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        rows_entry = ttk.Entry(
            main_frame,
            textvariable=self.rows_var,
            width=15,
        )
        rows_entry.grid(row=1, column=1, pady=5)
        rows_entry.bind("<KeyRelease>", self._validate_on_change)

        # Mine Count input
        ttk.Label(main_frame, text="Mine Count:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        mines_entry = ttk.Entry(
            main_frame,
            textvariable=self.mines_var,
            width=15,
        )
        mines_entry.grid(row=2, column=1, pady=5)
        mines_entry.bind("<KeyRelease>", self._validate_on_change)

        # Error message label
        ttk.Label(
            main_frame,
            textvariable=self.error_var,
            foreground="red",
        ).grid(row=3, column=0, columnspan=2, pady=5)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(
            button_frame,
            text="OK",
            command=self._on_ok,
            width=10,
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=self._on_cancel,
            width=10,
        ).pack(side=tk.LEFT, padx=5)

    def _center_dialog(self) -> None:
        """Center the dialog on the parent window."""
        self.update_idletasks()
        parent = self.master
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()

        dialog_width = self.winfo_width()
        dialog_height = self.winfo_height()

        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        self.geometry(f"+{x}+{y}")

    def _validate_on_change(self, event: tk.Event = None) -> None:
        """Validate inputs whenever they change.

        Updates the error message in real-time as the user types.

        Args:
            event: The Tkinter key release event (optional).
        """
        self.error_var.set("")

        cols_str = self.cols_var.get().strip()
        rows_str = self.rows_var.get().strip()
        mines_str = self.mines_var.get().strip()

        # Check for empty inputs
        if not cols_str or not rows_str or not mines_str:
            self.error_var.set("All fields are required.")
            return

        # Check for non-integer inputs
        try:
            cols = int(cols_str)
        except ValueError:
            self.error_var.set("Width must be a valid integer.")
            return

        try:
            rows = int(rows_str)
        except ValueError:
            self.error_var.set("Height must be a valid integer.")
            return

        try:
            mines = int(mines_str)
        except ValueError:
            self.error_var.set("Mine count must be a valid integer.")
            return

        # Validate bounds
        validation_error = self._validate_bounds(cols, rows, mines)
        if validation_error:
            self.error_var.set(validation_error)

    def _validate_bounds(self, cols: int, rows: int, mines: int) -> Optional[str]:
        """Validate the input bounds.

        Args:
            cols: Grid width (columns).
            rows: Grid height (rows).
            mines: Number of mines.

        Returns:
            An error message string if validation fails, None if valid.
        """
        # Check minimum grid size
        if cols < MIN_GRID_SIZE:
            return f"Width must be at least {MIN_GRID_SIZE}."
        if rows < MIN_GRID_SIZE:
            return f"Height must be at least {MIN_GRID_SIZE}."

        # Check maximum grid size
        if cols > MAX_GRID_WIDTH:
            return f"Width must be at most {MAX_GRID_WIDTH}."
        if rows > MAX_GRID_HEIGHT:
            return f"Height must be at most {MAX_GRID_HEIGHT}."

        # Check minimum mines
        if mines < MIN_MINES:
            return f"Mine count must be at least {MIN_MINES}."

        # Check mines < total cells
        total_cells = rows * cols
        if mines >= total_cells:
            return f"Mines ({mines}) must be less than total cells ({total_cells})."

        return None

    def _on_ok(self) -> None:
        """Handle OK button click. Validates and sets result if valid."""
        self.error_var.set("")

        cols_str = self.cols_var.get().strip()
        rows_str = self.rows_var.get().strip()
        mines_str = self.mines_var.get().strip()

        # Check for empty inputs
        if not cols_str or not rows_str or not mines_str:
            self.error_var.set("All fields are required.")
            return

        # Parse integers
        try:
            cols = int(cols_str)
            rows = int(rows_str)
            mines = int(mines_str)
        except ValueError:
            self.error_var.set("All fields must be valid integers.")
            return

        # Validate bounds
        validation_error = self._validate_bounds(cols, rows, mines)
        if validation_error:
            self.error_var.set(validation_error)
            return

        # All valid - set result and close
        self.result = CustomDifficultyInput(rows=rows, cols=cols, mines=mines)
        self.destroy()

    def _on_cancel(self) -> None:
        """Handle cancel button click or window close."""
        self.result = None
        self.destroy()
