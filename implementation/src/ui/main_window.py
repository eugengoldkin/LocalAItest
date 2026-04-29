"""Minesweeper - Main window UI.

STORY-003: Difficulty presets selection UI (dropdown).
STORY-004: Custom difficulty input UI integration.
STORY-005: Wire GameEngine to UI components for cell interaction.
STORY-009: Timer integration (updates on first click and game end).
STORY-010: Mine counter integration (real-time updates via callback).
STORY-012: New Game button (stub for future).
STORY-008: Win/loss message dialog UI.

The main Tkinter application window.
"""

from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
from typing import Optional

from src.config.difficulty import DEFAULT_DIFFICULTY, DIFFICULTY_PRESETS
from src.core.game import GameEngine
from src.ui.custom_difficulty_dialog import (
    CustomDifficultyDialog,
    CustomDifficultyInput,
)
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
        difficulty_var: Tkinter variable for the difficulty dropdown.
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
            text="00:00",
            font=("Courier", 16),
        )
        self.timer_label.pack(side=tk.RIGHT, padx=10)

        # Game grid frame - STORY-014
        self.game_frame: Optional[GridFrame] = None

        # STORY-009: Track whether we have a scheduled timer update
        self._timer_update_id: Optional[int] = None

        self._build_ui()

    # STORY-009: Timer display helpers

    def _update_timer_display(self, elapsed_seconds: int) -> None:
        """Update the timer label with the elapsed time.

        Args:
            elapsed_seconds: Current elapsed time in seconds.
        """
        capped_time = min(elapsed_seconds, GameEngine.MAX_TIME)
        minutes = capped_time // 60
        seconds = capped_time % 60
        formatted_time = f"{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=formatted_time)

    def _schedule_timer_update(self) -> None:
        """Schedule the next timer update using Tkinter's after().

        Updates every 250ms for smooth display while the timer is running.
        """
        if self._timer_update_id is not None:
            self.root.after_cancel(self._timer_update_id)
            self._timer_update_id = None

        if self.game_engine.timer_running:
            self._timer_update_id = self.root.after(250, self._schedule_timer_update)
            self._update_timer_display(self.game_engine.get_elapsed_time())

    def _cancel_timer_update(self) -> None:
        """Cancel any scheduled timer update."""
        if self._timer_update_id is not None:
            self.root.after_cancel(self._timer_update_id)
            self._timer_update_id = None

    # STORY-010: Mine counter display helper

    def _update_mine_counter_display(self, remaining_mines: int) -> None:
        """Update the mine counter label with the remaining mines.

        Supports negative numbers when more flags are placed than mines exist.

        Args:
            remaining_mines: Number of remaining mines (total_mines - flags_placed).
        """
        self.mine_counter_label.config(text=f"Mines: {remaining_mines}")

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
        """Build the initial UI structure.

        Creates the difficulty selector, game grid frame, and packs all UI components.
        """
        # STORY-003: Difficulty selector dropdown
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            difficulty_frame,
            text="Difficulty:",
            font=("Arial", 10),
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.difficulty_var = tk.StringVar(value=self.difficulty)
        difficulty_combo = ttk.Combobox(
            difficulty_frame,
            textvariable=self.difficulty_var,
            values=list(DIFFICULTY_PRESETS.keys()) + ["Custom"],
            state="readonly",
            width=15,
        )
        difficulty_combo.pack(side=tk.LEFT, padx=(0, 10))
        difficulty_combo.bind(
            "<<ComboboxSelected>>",
            self._on_difficulty_changed,
        )

        # Create game grid frame with game engine reference
        self.game_frame = GridFrame(
            self.root,
            self.game_engine,
            self.game_engine.grid.rows,
            self.game_engine.grid.cols,
        )
        # STORY-008: Wire up game end callback
        self.game_frame.on_game_end = self._on_game_end
        # STORY-009: Wire up timer update callback
        self.game_frame.on_timer_update = self._update_timer_display
        # STORY-009: Wire up timer start/stop callbacks
        self.game_frame.on_timer_start = self._schedule_timer_update
        self.game_frame.on_timer_stop = self._cancel_timer_update
        # STORY-010: Wire up mine counter update callback
        self.game_frame.on_mine_counter_update = self._update_mine_counter_display
        self.game_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

    def _on_difficulty_changed(self, event: tk.Event) -> None:
        """Handle difficulty selection from the dropdown.

        STORY-003: When the user selects a difficulty from the combobox,
        initialize a new game with those dimensions and mine count.

        STORY-004: Handle "Custom" selection by showing the custom difficulty dialog.

        Args:
            event: The Tkinter combobox selection event.
        """
        selected = self.difficulty_var.get()
        if selected == "Custom":
            self._on_custom_difficulty()
        elif selected in DIFFICULTY_PRESETS:
            self.change_difficulty(selected)

    def _on_custom_difficulty(self) -> None:
        """Handle Custom difficulty selection.

        STORY-004: Show the custom difficulty dialog. If the user provides
        valid inputs, initialize a new game with those parameters.
        """
        dialog = CustomDifficultyDialog(self.root)
        self.root.wait_window(dialog)

        if dialog.result is not None:
            custom_input = dialog.result
            self.difficulty = "Custom"
            self.game_engine = GameEngine(
                rows=custom_input.rows,
                cols=custom_input.cols,
                total_mines=custom_input.mines,
            )
            self.mine_counter_label.config(
                text=f"Mines: {self.game_engine.total_mines}"
            )
            self.timer_label.config(text="00:00")
            self._cancel_timer_update()

            # Destroy old grid frame and create a new one
            if self.game_frame is not None:
                self.game_frame.destroy()
            self.game_frame = GridFrame(
                self.root,
                self.game_engine,
                self.game_engine.grid.rows,
                self.game_engine.grid.cols,
            )
            self.game_frame.on_game_end = self._on_game_end
            # STORY-009: Wire up timer update/start/stop callbacks
            self.game_frame.on_timer_update = self._update_timer_display
            self.game_frame.on_timer_start = self._schedule_timer_update
            self.game_frame.on_timer_stop = self._cancel_timer_update
            # STORY-010: Wire up mine counter update callback
            self.game_frame.on_mine_counter_update = self._update_mine_counter_display
            self.game_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)

    def run(self) -> None:
        """Start the Tkinter event loop."""
        self.root.mainloop()

    def destroy(self) -> None:
        """Destroy the Tkinter window and clean up resources."""
        self._cancel_timer_update()
        self.root.destroy()

    def start_new_game(self) -> None:
        """Start a new game with the current difficulty settings.

        STORY-012: New Game button resets the game state and re-renders the grid.
        STORY-009: Timer resets to 00:00 on new game.
        """
        self.game_engine.reset()
        self.mine_counter_label.config(text=f"Mines: {self.game_engine.total_mines}")
        self.timer_label.config(text="00:00")
        self._cancel_timer_update()

        # Destroy old grid frame and create a new one
        if self.game_frame is not None:
            self.game_frame.destroy()
        self.game_frame = GridFrame(
            self.root,
            self.game_engine,
            self.game_engine.grid.rows,
            self.game_engine.grid.cols,
        )
        self.game_frame.on_game_end = self._on_game_end
        # STORY-009: Wire up timer update/start/stop callbacks
        self.game_frame.on_timer_update = self._update_timer_display
        self.game_frame.on_timer_start = self._schedule_timer_update
        self.game_frame.on_timer_stop = self._cancel_timer_update
        # STORY-010: Wire up mine counter update callback
        self.game_frame.on_mine_counter_update = self._update_mine_counter_display
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
        self.timer_label.config(text="00:00")
        self._cancel_timer_update()

        # Destroy old grid frame and create a new one
        if self.game_frame is not None:
            self.game_frame.destroy()
        self.game_frame = GridFrame(
            self.root,
            self.game_engine,
            self.game_engine.grid.rows,
            self.game_engine.grid.cols,
        )
        self.game_frame.on_game_end = self._on_game_end
        # STORY-009: Wire up timer update/start/stop callbacks
        self.game_frame.on_timer_update = self._update_timer_display
        self.game_frame.on_timer_start = self._schedule_timer_update
        self.game_frame.on_timer_stop = self._cancel_timer_update
        # STORY-010: Wire up mine counter update callback
        self.game_frame.on_mine_counter_update = self._update_mine_counter_display
        self.game_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
