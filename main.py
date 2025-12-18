import sys
import os
from analyzer.analyzer import AnalyzerV2
from analyzer.advisor import generate_v2_advice

def main():
    file_path = ""
    if len(sys.argv) < 2:
        # Interactive mode
        try:
            file_path = input("Enter the path of the code file: ").strip()
            # Handle quotes
            if file_path.startswith('"') and file_path.endswith('"'):
                file_path = file_path[1:-1]
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            return
    else:
        file_path = sys.argv[1]

    if not file_path:
        print("Error: No file path provided.")
        return
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    print(f"\n======== Analysis Report: {os.path.basename(file_path)} ========\n")

    analyzer = AnalyzerV2()
    result = analyzer.analyze(source_code)
    
    if "error" in result:
        print(result["error"])
        return

    # --- Unified Output Section ---
    print(f"Time Complexity : {result['overall_time']}")
    print(f"Space Complexity: {result['overall_space']}")
    print("-" * 50)
    
    print("\n[Breakdown by Function]")
    functions = result.get("functions", {})
    if not functions:
        print("  (No functions detected - analyzing code globally)")
        for log in result.get("global_log", []):
            print(f"  - {log}")
            
    for func_name, details in functions.items():
        print(f"\n🔹 Function: {func_name} | Time: {details['time']} | Space: {details['space']}")
        for log in details['breakdown']:
            print(f"  {log}")

    print("\n[Advisory & Optimization]")
    advice = generate_v2_advice(result)
    if not advice:
        print("  ✅ No critical conceptual issues detected.")
    else:
        for tip in advice:
            print(f"  {tip}")
            
    print("\n=======================================================")

if __name__ == "__main__":
    main()
