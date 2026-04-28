"""Minesweeper - Main window UI.

STORY-005: Wire GameEngine to UI components for cell interaction.
STORY-009: Timer integration (stub for future).
STORY-010: Mine counter integration (stub for future).
STORY-012: New Game button (stub for future).
STORY-008: Win/loss message dialog UI.

The main Tkinter application window.
"""

from __future__ import annotations

import tkinter as tk
from typing import Optional

from src.config.difficulty import DEFAULT_DIFFICULTY, DIFFICULTY_PRESETS
from src.core.game import GameEngine
from src.ui.game_end_dialog import GameEndDialog
from src.ui.grid_frame import GridFrame
from src.ui.hud import HUD


class MainWindow:
    """The main Tkinter window for the Minesweeper game.

    Attributes:
        root: The root Tkinter window.
        game_engine: The GameEngine instance managing game state.
        grid_frame: Frame containing the game grid.
        hud_frame: Frame containing the HUD (mine counter, timer).
        difficulty: Currently selected difficulty preset name.
    """

    def __init__(self) -> None:
        """Initialize the MainWindow.

        Creates the root window, game engine, and builds the UI.
        """
        self.root: tk.Tk = tk.Tk()
        self.root.title("Minesweeper")
        self.root.resizable(True, True)

        # Default difficulty
        self.difficulty: str = DEFAULT_DIFFICULTY
        preset = DIFFICULTY_PRESETS[self.difficulty]
        self.game_engine: GameEngine = GameEngine(
            rows=preset.rows,
            cols=preset.cols,
            total_mines=preset.mines,
        )

        # HUD frame (for mine counter and timer) - STORY-009, STORY-010
        self.hud_frame: tk.Frame = tk.Frame(self.root)
        self.hud_frame.pack(fill=tk.X, padx=10, pady=5)

        # Mine counter label
        self.mine_counter_label: tk.Label = tk.Label(
            self.hud_frame,
            text=f"Mines: {self.game_engine.total_mines}",
            font=("Courier", 16),
        )
        self.mine_counter_label.pack(side=tk.LEFT, padx=10)

        # Timer label
        self.timer_label: tk.Label = tk.Label(
            self.hud_frame,
            text="Time: 0s",
            font=("Courier", 16),
        )
        self.timer_label.pack(side=tk.RIGHT, padx=10)

                # Game grid frame - STORY-014
        self.game_frame: Optional[GridFrame] = None

        self._build_ui()

    def _on_game_end(self, won: bool) -> None:
        """Handle game end by showing the appropriate dialog.

        STORY-008: Show win/loss dialog when the game ends.
        """
        dialog = GameEndDialog(
            self.root,
            won=won,
            result_callback=self.start_new_game,
        )
        dialog.grab_set()  # Modal: block interaction with main window

    def _build_ui(self) -> None:

    def _build_ui(self) -> None:
        """Build the initial UI structure.

        Creates the game grid frame and packs all UI components.
        """
                # Create game grid frame with game engine reference
        self.game_frame = GridFrame(
            self.root,
            self.game_engine,
            self.game_engine.grid.rows,
            self.game_engine.grid.cols,
        )
        # STORY-008: Wire up game end callback
        self.game_frame.on_game_end = self._on_game_end
        self.game_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self.root.mainloop()

    def destroy(self) -> None:
        """Destroy the Tkinter window and clean up resources."""
        self.root.destroy()

    def start_new_game(self) -> None:
        """Start a new game with the current difficulty settings.

        STORY-012: New Game button resets the game state and re-renders the grid.
        """
        self.game_engine.reset()
        self.mine_counter_label.config(text=f"Mines: {self.game_engine.total_mines}")
        self.timer_label.config(text="Time: 0s")

        # Destroy old grid frame and create a new one
        if self.game_frame is not None:
            self.game_frame.destroy()
        self.game_frame = GridFrame(
            self.root,
            self.game_engine,
            self.game_engine.grid.rows,
            self.game_engine.grid.cols,
        )
        self.game_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

    def change_difficulty(self, difficulty_name: str) -> None:
        """Change the game difficulty and start a new game.

        Args:
            difficulty_name: Name of the difficulty preset (e.g., 'Beginner').
        """
        if difficulty_name not in DIFFICULTY_PRESETS:
            return

        self.difficulty = difficulty_name
        preset = DIFFICULTY_PRESETS[difficulty_name]

        self.game_engine = GameEngine(
            rows=preset.rows,
            cols=preset.cols,
            total_mines=preset.mines,
        )

        self.mine_counter_label.config(text=f"Mines: {self.game_engine.total_mines}")
        self.timer_label.config(text="Time: 0s")

        # Destroy old grid frame and create a new one
        if self.game_frame is not None:
            self.game_frame.destroy()
        self.game_frame = GridFrame(
            self.root,
            self.game_engine,
            self.game_engine.grid.rows,
            self.game_engine.grid.cols,
        )
        self.game_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
