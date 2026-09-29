from pathlib import Path


# Project root = folder containing this script
PROJECT_ROOT = Path(__file__).resolve().parent


# ============================================================
# FOLDERS
# ============================================================

folders = [
    "src",
    "datasets",
    "tests",
    "benchmarks",
    "results",
    "results/graphs",
    "results/tables",
]


# ============================================================
# SOURCE FILES
# ============================================================

src_files = [
    "src/__init__.py",
    "src/sudoku.py",
    "src/validator.py",
    "src/candidates.py",
    "src/constraint_propagation.py",
    "src/backtracking.py",
    "src/mrv.py",
    "src/min_conflicts.py",
    "src/metrics.py",
    "src/analyzer.py",
    "src/adaptive_solver.py",
    "src/strategy_switcher.py",
    "src/verifier.py",
]


# ============================================================
# TEST FILES
# ============================================================

test_files = [
    "tests/__init__.py",
    "tests/test_validator.py",
    "tests/test_candidates.py",
    "tests/test_solvers.py",
    "tests/test_adaptive.py",
]


# ============================================================
# ROOT FILES
# ============================================================

root_files = [
    "main.py",
    "README.md",
    ".gitignore",
]


# ============================================================
# FILE CONTENT
# ============================================================

file_contents = {

    ".gitignore": """\
.venv/
__pycache__/
*.pyc
.vscode/
.idea/
.pytest_cache/
*.log
""",

    "README.md": """\
# Adaptive Sudoku Solver

An AI-based Sudoku solver that dynamically selects and switches
between multiple solving strategies based on puzzle characteristics
and solving progress.

## Main Strategies

- Constraint Propagation
- MRV + Backtracking
- Min-Conflicts

## Project Goal

To investigate whether adaptive strategy selection can improve
Sudoku-solving efficiency compared with fixed solving strategies.
""",

    "main.py": """\
def main():
    print("Adaptive Sudoku Solver")


if __name__ == "__main__":
    main()
""",

    "src/__init__.py": "",

    "src/sudoku.py": """\
\"\"\"Sudoku grid representation and basic Sudoku operations.\"\"\"
""",

    "src/validator.py": """\
\"\"\"Sudoku input validation.\"\"\"
""",

    "src/candidates.py": """\
\"\"\"Candidate value generation for Sudoku cells.\"\"\"
""",

    "src/constraint_propagation.py": """\
\"\"\"Constraint propagation Sudoku solver.\"\"\"
""",

    "src/backtracking.py": """\
\"\"\"Basic backtracking Sudoku solver.\"\"\"
""",

    "src/mrv.py": """\
\"\"\"Minimum Remaining Values heuristic.\"\"\"
""",

    "src/min_conflicts.py": """\
\"\"\"Min-Conflicts local-search Sudoku solver.\"\"\"
""",

    "src/metrics.py": """\
\"\"\"Performance metrics and solver statistics.\"\"\"
""",

    "src/analyzer.py": """\
\"\"\"Sudoku puzzle analysis and computational profiling.\"\"\"
""",

    "src/adaptive_solver.py": """\
\"\"\"Adaptive strategy-selection Sudoku solver.\"\"\"
""",

    "src/strategy_switcher.py": """\
\"\"\"Strategy switching and progress evaluation.\"\"\"
""",

    "src/verifier.py": """\
\"\"\"Final Sudoku solution verification.\"\"\"
""",

    "tests/__init__.py": "",

    "tests/test_validator.py": """\
\"\"\"Tests for Sudoku validation.\"\"\"
""",

    "tests/test_candidates.py": """\
\"\"\"Tests for candidate generation.\"\"\"
""",

    "tests/test_solvers.py": """\
\"\"\"Tests for Sudoku solving strategies.\"\"\"
""",

    "tests/test_adaptive.py": """\
\"\"\"Tests for the adaptive Sudoku solver.\"\"\"
""",
}


# ============================================================
# CREATE FOLDERS
# ============================================================

print("\\nCreating project folders...")

for folder in folders:
    path = PROJECT_ROOT / folder
    path.mkdir(parents=True, exist_ok=True)
    print(f"[OK] {folder}")


# ============================================================
# CREATE FILES
# ============================================================

all_files = src_files + test_files + root_files

print("\\nCreating project files...")

for file in all_files:
    path = PROJECT_ROOT / file

    # Create parent directory if necessary
    path.parent.mkdir(parents=True, exist_ok=True)

    # Do NOT overwrite existing files
    if path.exists():
        print(f"[SKIP] {file} already exists")
        continue

    content = file_contents.get(file, "")
    path.write_text(content, encoding="utf-8")

    print(f"[OK] {file}")


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("PROJECT STRUCTURE CREATED SUCCESSFULLY")
print("=" * 60)

print(f"\nProject location:")
print(PROJECT_ROOT)

print("\nNext step:")
print("Start implementing src/sudoku.py")