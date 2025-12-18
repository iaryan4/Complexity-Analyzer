# Time Complexity Analyzer Walkthrough

I have built a static analysis tool that estimates the time complexity of Python code, explains the reasoning, and offers optimization advice.

## What's Included
- **`main.py`**: The CLI entry point.
- **`analyzer/analyzer.py`**: The core logic that traverses the Abstract Syntax Tree (AST) to count loop nesting.
- **`analyzer/advisor.py`**: A module that suggests optimizations (e.g., using sets instead of lists for lookups).
- **`check_complexity.py`**: A sample file with mixed complexities (O(1), O(n), O(n^2), O(n^3)) for testing.

## How to Run It

1.  **Open a terminal** in `d:\CODE\Python\Projects\TimeComplexityAnalyzer`.
2.  **Run the analyzer**:
    *   **Option A (Interactive):** Run `python main.py` and paste the file path when prompted.
    *   **Option B (Command Line):** Run `python main.py <path_to_file>`

```bash
python main.py
# Enter the path of the code file: check_complexity.py
```

## Example Output

When running against the provided test file, you will see output similar to this:

```text
--- Analyzing d:\CODE\Python\Projects\TimeComplexityAnalyzer\check_complexity.py ---

Estimated Time Complexity: O(n^3)
Reason: Deeply nested loops detected (Depth 3).

[Detailed Trace]
  - Line 10: Enters nested loop (Depth 1)
  - Line 16: Enters nested loop (Depth 1)
  - Line 17: Enters nested loop (Depth 2)
  - Line 22: Enters nested loop (Depth 1)
  - Line 23: Enters nested while loop (Depth 2)
  - Line 24: Enters nested loop (Depth 3)

[Optimization Advice]
  - High complexity detected due to nested loops. Consider if you can linearize the logic.
  -    - If searching, consider using a hash map (Dictionary/Set) for O(1) lookups.
  -    - If sorting, standard Timsort is O(n log n), which is better than O(n^2).
  - Line 24: Deeply nested loop (Depth 3). This is a major performance bottleneck.
```

## How it Works
The tool uses Python's `ast` library to parse the code without running it. It tracks:`For` and `While` nodes to determine nesting depth.
- **Depth 0**: O(1)
- **Depth 1**: O(n)
- **Depth 2**: O(n^2)
- **Depth 3+**: O(n^k)

> [!NOTE]
> As this is a static analyzer, it provides an *estimate* based on structure. It may not catch runtime-specific optimizations or complex recursion patterns that don't rely on standard loops.
