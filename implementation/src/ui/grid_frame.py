"""Minesweeper - Grid frame UI component.

STORY-005: Implement grid rendering and cell interaction event bindings.
STORY-014: Visual rendering of the game grid with colors and icons.

Tkinter frame that renders the Minesweeper game grid.
"""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from src.config.constants import (
    BG_COLOR,
    BORDER_COLOR,
    CELL_FLAGGED_COLOR,
    CELL_FONT,
    CELL_HIDDEN_COLOR,
    CELL_MINE_COLOR,
    CELL_MINE_REVEALED_COLOR,
    CELL_REVEALED_COLOR,
    FRAME_BG,
    NUMBER_COLORS,
)
from src.core.cell import CellState


class GridFrame(tk.Frame):
    """Tkinter frame that renders the Minesweeper game grid.

    Attributes:
        master: The parent widget.
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.
        cell_size: Size of each cell in pixels.
        cells: 2D list of Tkinter button widgets.
        game_engine: Reference to the GameEngine instance for state access.
    """

    def __init__(
        self,
        master: tk.Widget,
        game_engine,
        rows: int,
        cols: int,
        cell_size: int = 30,
    ) -> None:
        """Initialize the GridFrame.

        Args:
            master: The parent Tkinter widget.
            game_engine: The GameEngine instance providing game state.
            rows: Number of rows in the grid.
            cols: Number of columns in the grid.
            cell_size: Size of each cell in pixels (default 30).
        """
        super().__init__(master, bg=FRAME_BG)
        self.rows: int = rows
        self.cols: int = cols
        self.cell_size: int = cell_size
        self.game_engine = game_engine
        self.cells: list[list[tk.Button]] = []

        self.render()

    def render(self) -> None:
        """Render the grid in the frame.

        STORY-014: Create buttons for each cell with proper styling.
        """
        for r in range(self.rows):
            row_buttons = []
            for c in range(self.cols):
                btn = tk.Button(
                    self,
                    width=2,
                    height=1,
                    font=(CELL_FONT),
                    bg=CELL_HIDDEN_COLOR,
                    fg="black",
                    relief=tk.RAISED,
                    bd=2,
                    command=None,  # Set dynamically via lambda
                )
                # Bind left-click to reveal cell (STORY-005-T1)
                btn.bind(
                    "<Button-1>",
                    lambda e, row=r, col=c: self.on_left_click(row, col),
                )
                # Bind right-click to toggle flag (STORY-005-T2)
                btn.bind(
                    "<Button-3>",
                    lambda e, row=r, col=c: self.on_right_click(row, col),
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                row_buttons.append(btn)
            self.cells.append(row_buttons)

    def update_cell(self, row: int, col: int) -> None:
        """Update a single cell's visual state based on game state.

        STORY-005-T5/T6: Visual indicators for flagged and revealed cells.
        STORY-014: Display correct colors and content for each state.

        Args:
            row: Row index of the cell.
            col: Column index of the cell.
        """
        cell = self.game_engine.grid.get_cell(row, col)
        if cell is None or not self.cells:
            return

        btn = self.cells[row][col]

        if cell.state == CellState.REVEALED:
            if cell.is_mine:
                # Revealed mine (game over)
                btn.config(
                    bg=CELL_MINE_COLOR,
                    fg="white",
                    relief=tk.SUNKEN,
                    bd=1,
                    text="*",
                )
            elif cell.adjacent_mines > 0:
                # Revealed numbered cell
                btn.config(
                    bg=CELL_REVEALED_COLOR,
                    fg=NUMBER_COLORS.get(cell.adjacent_mines, "black"),
                    relief=tk.SUNKEN,
                    bd=1,
                    text=str(cell.adjacent_mines),
                )
            else:
                # Revealed empty cell (0 adjacent mines)
                btn.config(
                    bg=CELL_REVEALED_COLOR,
                    fg="black",
                    relief=tk.SUNKEN,
                    bd=1,
                    text="",
                )
        elif cell.state == CellState.FLAGGED:
            # Flagged cell
            btn.config(
                bg=CELL_FLAGGED_COLOR,
                fg="red",
                relief=tk.RAISED,
                bd=2,
                text="F",
            )
        elif cell.state == CellState.HIDDEN:
            # Hidden cell
            btn.config(
                bg=CELL_HIDDEN_COLOR,
                fg="black",
                relief=tk.RAISED,
                bd=2,
                text="",
            )
        elif cell.state == CellState.QUESTION:
            # Question mark cell
            btn.config(
                bg=CELL_HIDDEN_COLOR,
                fg="blue",
                relief=tk.RAISED,
                bd=2,
                text="?",
            )

    def update_all_cells(self) -> None:
        """Update all cells' visual state.

        Used after game start or reset to refresh the entire grid.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                self.update_cell(r, c)

    def on_left_click(self, row: int, col: int) -> None:
        """Handle left-click event on a cell.

        STORY-005-T1: Left-click event handler for revealing cells.
        - Reveals hidden cells
        - Does nothing on revealed cells
        - Does nothing on flagged cells

        Args:
            row: Row index of the clicked cell.
            col: Column index of the clicked cell.
        """
        if self.game_engine.game_over:
            return

        new_state = self.game_engine.reveal_cell(row, col)

        if new_state is not None:
            self.update_cell(row, col)

            # Check win condition after reveal (STORY-008)
            if not self.game_engine.game_over:
                self.game_engine.check_win_condition()
                if self.game_engine.game_won:
                    # Update all cells to show win state
                    self.update_all_cells()
        else:
            # Check win condition even if no state change (for flood fill scenarios)
            if not self.game_engine.game_over:
                self.game_engine.check_win_condition()
                if self.game_engine.game_won:
                    self.update_all_cells()

    def on_right_click(self, row: int, col: int) -> None:
        """Handle right-click event on a cell.

        STORY-005-T2: Right-click event handler for toggling flags.
        - Toggles hidden <-> flagged
        - Does nothing on revealed cells

        Args:
            row: Row index of the clicked cell.
            col: Column index of the clicked cell.
        """
        if self.game_engine.game_over:
            return

        success = self.game_engine.toggle_flag(row, col)

        if success:
            self.update_cell(row, col)
