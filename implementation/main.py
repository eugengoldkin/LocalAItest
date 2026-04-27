"""Minesweeper - Entry point.

STORY-001-T5: Write README.md with setup and run instructions.
Creates and runs the main application window.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the implementation directory is in the Python path
_project_root = Path(__file__).resolve().parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.ui.main_window import MainWindow


def main() -> None:
    """Start the Minesweeper application.

    STORY-001-T5: Entry point for the project.
    """
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
