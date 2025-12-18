def generate_v2_advice(analysis_result):
    advice_list = []
    
    overall_time = analysis_result.get("overall_time", "O(1)")
    overall_space = analysis_result.get("overall_space", "O(1)")
    
    # 1. High-level advice
    if "n^2" in overall_time or "n^3" in overall_time:
        advice_list.append(f"⚠️  High Time Complexity {overall_time}: Nested loops detected.")
        advice_list.append("   - Suggest using Hash Maps (Dict/Set) to reduce O(n) lookups to O(1) inside loops.")
        advice_list.append("   - Check if sorting (O(n log n)) allows you to use Two Pointers or Binary Search.")

    if "n" in overall_space:
        advice_list.append(f"⚠️  Space Complexity {overall_space}: Significant memory usage detected.")
        advice_list.append("   - Check if you are creating new lists inside loops.")
        advice_list.append("   - Consider using generators (yield) if you don't need to store all items at once.")

    # 2. Function-specific warnings
    functions = analysis_result.get("functions", {})
    for func_name, details in functions.items():
        time = details['time']
        space = details['space']
        breakdown = details['breakdown']
        
        # Recursion check in breakdown
        if any("Recursive" in line for line in breakdown):
            advice_list.append(f"ℹ️  Recursion detected in '{func_name}'. Ensure base cases are efficient to avoid StackOverflow.")
            if "n^2" in time:
                advice_list.append(f"   - Recursive function '{func_name}' has high complexity. Consider Memoization (caching) or Iterative approach.")

    return advice_list
