# Skill: Implement Story (Minesweeper)

## Purpose
A reusable, step-by-step workflow for implementing a specific Minesweeper story using Python and Tkinter. It ensures strict alignment with requirements, manages dependencies, and produces clean, modular, and testable code in the `implementation/` directory.

## Inputs Required
1. **Story File**: e.g., `stories/STORY-XXX-<title>.md`
2. **Requirements**: `minesweeper.md`
3. **Story List**: `stories/storylist.md`

---

## Workflow

### Phase 1: Context Ingestion
1. Read the **Story File** to extract:
   - `Acceptance Criteria` (must be checked at the end)
   - `Tasks` (actionable steps to execute)
   - `Dependencies` (other stories that must be implemented first)
2. Read `minesweeper.md` to understand:
   - Overall architecture (backend vs frontend separation)
   - Technical constraints (Python 3.x, Tkinter, 2D arrays/lists)
   - Non-functional requirements (performance, code quality, visual standards)
3. Read `stories/storylist.md` to understand:
   - Execution phase context
   - Dependency graph relationships
   - Current status of related stories

### Phase 2: Dependency & Scope Analysis
1. Check `implementation/` directory:
   - If it exists, scan for previously implemented stories.
   - If it doesn't exist, treat as a fresh start.
2. Verify all `Dependencies` are marked as `Completed` or have scaffolded code in `implementation/`.
   - If a dependency is missing, create a minimal stub for it first, then proceed.
3. Define the exact scope for this story. Do not implement features outside the current story's tasks unless explicitly required by a dependency.

### Phase 3: Implementation Planning
1. Map story tasks to specific files within `implementation/`.
   - **Backend** (`implementation/src/core/`): Game logic, grid, state management, algorithms.
   - **Frontend** (`implementation/src/ui/`): Tkinter widgets, layouts, event bindings, rendering.
   - **Config** (`implementation/src/config/`): Difficulty presets, constants, paths.
   - **Tests** (`implementation/tests/`): Unit/integration tests for new logic.
   - **Root** (`implementation/`): `main.py`, `requirements.txt`, `README.md`, `.gitignore`.
2. Draft a file tree for the story before writing code.
3. Identify shared components vs. story-specific components.

### Phase 4: Code Generation
Execute tasks sequentially. For each task:
1. Write Python code following Tkinter best practices and the project's architectural rules.
2. Add comments linking back to the story ID and task ID (e.g., `# STORY-005-T1: Left-click handler`).
3. Implement incrementally, ensuring each file is syntactically valid before moving to the next.
4. Update `implementation/README.md` with a changelog of what was added in this story.

### Phase 5: Verification
1. Cross-check the generated code against every `Acceptance Criteria` item.
2. Run static analysis (e.g., `flake8`, `mypy`) if available.
3. Verify Tkinter event bindings, grid rendering, and state transitions.
4. Mark tasks as `Completed` in the story file.
5. Update `storylist.md` status for this story to `Completed`.

---

## Implementation Rules

### 📂 Directory Structure
```
implementation/
├── src/
│   ├── core/          # Game logic, Grid, Cell, GameEngine
│   ├── ui/            # Tkinter widgets, MainWindow, GridFrame, HUD
│   ├── config/        # Constants, Difficulty presets, Paths
│   └── utils/         # Helpers, formatters, validators
├── tests/             # Unit & integration tests
├── assets/            # Icons, images (if any)
├── main.py            # Entry point
├── requirements.txt   # Dependencies (tkinter is stdlib)
└── README.md          # Setup & run instructions
```

### 🐍 Python & Tkinter Guidelines
- **OOP Structure**: Use classes for UI components (`tk.Frame`, `tk.Tk`) and game logic (`Game`, `Grid`, `Cell`).
- **Event Binding**: Use `bind()` for keyboard/mouse events. Avoid `after()` loops for UI updates; use Tkinter's event loop.
- **Layout**: Prefer `grid()` for the board (consistent sizing) and `pack()` for HUD/controls.
- **State Management**: Keep game state in `src/core/`. UI should only read state and render. Avoid tight coupling.
- **Type Hints**: Use `typing` module for function signatures.
- **Docstrings**: Every class and public method must have a docstring explaining purpose, params, and returns.
- **Error Handling**: Gracefully handle invalid inputs, out-of-bounds clicks, and Tkinter exceptions.
- **Performance**: Use list comprehensions for grid generation. Avoid heavy string operations in the render loop.

### 🎨 Visual & UX Standards (from `minesweeper.md`)
- Number colors: `1=Blue, 2=Green, 3=Red, 4=DarkBlue, 5=Brown, 6=Cyan, 7=Black, 8=Gray`
- Cell states must be visually distinct (Hidden, Revealed, Flagged, Mine).
- Grid must resize dynamically without breaking layout.
- Timer and Mine Counter must update in real-time.
- First click safety must be enforced before grid rendering.

---

## Output Expectations
- Clean, PEP-8 compliant Python code.
- Fully functional Tkinter UI that matches the story's scope.
- Tests covering core logic (grid generation, flood fill, win/loss conditions).
- Updated documentation (`README.md`, story files, storylist).
- No hardcoded paths; use `pathlib` or relative imports.
- Clear separation of concerns between `core/` and `ui/`.

---

## Execution Prompt Template
When using this skill, provide the following context to the AI/developer:
```
STORY: <path-to-story.md>
REQUIREMENTS: minesweeper.md
STORYLIST: stories/storylist.md
CURRENT STATUS: <e.g., Fresh start / Story 005 in progress>
TARGET DIR: implementation/
```
Follow the workflow phases strictly. Do not skip dependency checks. Validate against acceptance criteria before concluding.
