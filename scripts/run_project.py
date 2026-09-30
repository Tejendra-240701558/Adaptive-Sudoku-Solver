"""
Run the complete Adaptive Sudoku Solver evaluation.

This script runs:

1. Automated tests
2. Eight-puzzle benchmark
3. Benchmark analysis
4. P7 live demonstration

Run from the project root:

    .\.venv\Scripts\python.exe scripts\run_project.py
"""

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command, title):

    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

    result = subprocess.run(
        command,
        cwd=ROOT,
        env={
            **os.environ,
            "PYTHONPATH": str(ROOT)
        }
    )

    if result.returncode != 0:

        print(
            f"\nCommand failed with exit code "
            f"{result.returncode}."
        )

        sys.exit(result.returncode)


def main():

    python = sys.executable

    # --------------------------------------------------------
    # 1. Tests
    # --------------------------------------------------------

    run(
        [python, "-m", "pytest"],
        "1. AUTOMATED TESTS"
    )

    # --------------------------------------------------------
    # 2. Eight-puzzle benchmark
    # --------------------------------------------------------

    run(
        [python, "benchmarks/run_benchmark.py"],
        "2. EIGHT-PUZZLE BENCHMARK"
    )

    # --------------------------------------------------------
    # 3. Benchmark analysis
    # --------------------------------------------------------

    run(
        [python, "benchmarks/analyze_results.py"],
        "3. BENCHMARK ANALYSIS"
    )

    # --------------------------------------------------------
    # 4. P7 demonstration
    # --------------------------------------------------------

    run(
        [python, "main.py"],
        "4. P7 LIVE DEMONSTRATION"
    )

    print("\n" + "=" * 72)
    print("PROJECT RUN COMPLETED")
    print("=" * 72)

    print(
        "Use the benchmark analysis for the overall results."
    )

    print(
        "Use the P7 demonstration for the adaptive-switching presentation."
    )

    print("=" * 72)


if __name__ == "__main__":
    main()
