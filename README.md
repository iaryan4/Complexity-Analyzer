# Static Time & Space Complexity Analyzer for Python

## Project Overview
This project is an in-depth static analysis tool designed to estimate both the **Time** and **Space** complexity of Python code. By parsing the source code into an **Abstract Syntax Tree (AST)**, the analyzer infers algorithmic complexity without executing the code. It is built to provide explainable feedback on loop structures, nesting, and recursion, serving as an educational utility for understanding algorithmic performance.

## Key Features
- **Static AST-Based Analysis**: Analyzes code structure without running it, ensuring safety and speed.
- **Loop Bound Detection**: Distinguishes between constant (`range(10)`), linear (`range(n)`), and polynomial (`range(n*n)`) bounds.
- **Nesting vs. Sequential Logic**: Correctly computes combined complexity by multiplying nested loops and adding sequential ones.
- **Recursion Detection**: Identifies recursive functions and estimates stack space complexity.
- **Per-Function Breakdown**: Reports time and space complexity for each function independently.
- **Explainable Reasoning**: Provides line-by-line logs explaining *why* a certain complexity was calculated.
- **Optimization Advice**: Provides tailored suggestions for identified bottlenecks (e.g., suggesting hash maps for nested lookups).

## Project Structure
- **`main.py`**: The CLI entry point that handles user input and orchestrates the analysis.
- **`analyzer/analyzer.py`**: The core logic containing the AST visitor and complexity inference engine.
- **`analyzer/advisor.py`**: The module responsible for generating optimization advice based on analysis results.
- **`v2_checks.py`**: A comprehensive test suite demonstrating various complexity patterns (loops, recursion, space).

## How It Works (High-Level)
1.  **Parse**: The Python source code is parsed into an Abstract Syntax Tree (AST).
2.  **Traverse**: The tool visits nodes in the AST to identify control flow structures (loops, function calls, assignments).
3.  **Build**: It constructs a complexity profile for each function, tracking loop nesting depth and variable allocations.
4.  **Aggregate**: Complexities are aggregated—multiplying for nesting and adding for sequential blocks—to determine the dominant term (Big-O).
5.  **Report**: The final estimated worst-case complexity is reported along with a breakdown of contributing factors.

## How to Run
Navigate to the project directory in your terminal:

```bash
cd d:\CODE\Python\Projects\ComplexityAnalyzer
```

Run the analyzer on a Python file:

```bash
python main.py <target_file.py>
```

*You can also run `python main.py` without arguments to enter interactive mode.*

## Example Output

> **Note:** All complexity estimates are heuristic-based static approximations.

```text
======== Analysis Report ========

Time Complexity : O(n^2)
Space Complexity: O(n)
--------------------------------------------------

[Breakdown by Function]
🔹 Function: partial_sum | Time: O(n^2) | Space: O(1)
  Loop at line 12: For loop with linear (n) bound
  Loop at line 13: Nested for loop with linear (n) bound
   -> Loop contributes O(n^2) to total

[Advisory & Optimization]
  ⚠️  High Time Complexity O(n^2): Nested loops detected.
  ℹ️  Suggestion: Consider if data can be pre-sorted or hashed.
```

## Limitations
- **Static Analysis**: Cannot determine runtime-dependent bounds (e.g., `while condition:`) with certainty.
- **Unknown Variables**: Assumes `range(variable)` contributes `O(n)` if the variable is not a known constant.
- **Recursion Depth**: Approximates recursion depth as linear `O(n)` unless base cases are trivial; does not solve recurrence relations.
- **Not Compiler-Grade**: Does not account for Python internal optimizations, amortized costs, or advanced machine-level specifics.

## Why This Tool Exists
Understanding algorithmic complexity is a core skill in software engineering, yet it is often disconnected from everyday coding practice. This tool was built to help programmers quickly analyze the time and space complexity of their Python code using static analysis, without executing it. By providing explainable estimates and optimization hints, the tool aims to make performance reasoning more accessible and practical during development.


