import ast

class ComplexityTerm:
    """Represents a complexity term like O(1), O(n), O(n^2)."""
    def __init__(self, power=0, log_power=0):
        self.power = power
        self.log_power = log_power

    def __add__(self, other):
        # When adding complexities (sequential), take the max
        if self.power > other.power:
            return self
        elif other.power > self.power:
            return other
        else:
            return ComplexityTerm(self.power, max(self.log_power, other.log_power))

    def __mul__(self, other):
        # When multiplying (nesting), add the powers
        return ComplexityTerm(self.power + other.power, self.log_power + other.log_power)

    def __str__(self):
        if self.power == 0 and self.log_power == 0:
            return "O(1)"
        parts = []
        if self.power == 1:
            parts.append("n")
        elif self.power > 1:
            parts.append(f"n^{self.power}")
        
        if self.log_power == 1:
            parts.append("log n")
        elif self.log_power > 1:
            parts.append(f"(log n)^{self.log_power}")
            
        return "O(" + (" * ".join(parts) if parts else "1") + ")"

class FunctionAnalysis:
    def __init__(self, name):
        self.name = name
        self.time_complexity = ComplexityTerm(0) # Start at O(1)
        self.space_complexity = ComplexityTerm(0) # Start at O(1)
        self.breakdown = []
        self.is_recursive = False

class AnalyzerV2(ast.NodeVisitor):
    def __init__(self):
        self.functions = {} # name -> FunctionAnalysis
        self.current_function = None
        self.loop_stack = [] # Stack of loop complexities
        self.recursion_stack = set() # For detecting recursion
        self.global_breakdown = [] # Code outside functions

    def _get_current_context(self):
        if self.current_function:
            return self.current_function
        return None 

    def _log(self, message, nesting_level=0):
        ctx = self._get_current_context()
        indent = "  " * nesting_level
        msg = f"{indent}{message}"
        if ctx:
            ctx.breakdown.append(msg)
        else:
            self.global_breakdown.append(msg)

    def visit_FunctionDef(self, node):
        func_analysis = FunctionAnalysis(node.name)
        self.functions[node.name] = func_analysis
        self.current_function = func_analysis
        
        self.recursion_stack.add(node.name)
        
        # Analyze body
        self.generic_visit(node)
        
        # Check for recursion impact
        if func_analysis.is_recursive:
            func_analysis.time_complexity = func_analysis.time_complexity * ComplexityTerm(1) # Multiply by N for recursion depth
            func_analysis.space_complexity = func_analysis.space_complexity + ComplexityTerm(1) # Stack space
            self._log(f"Recursive function detected -> Multiplied complexity by O(n) (Stack Depth)")

        self.recursion_stack.remove(node.name)
        self.current_function = None

    def visit_Call(self, node):
        # Detect recursion
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if self.current_function and func_name == self.current_function.name:
                self.current_function.is_recursive = True
                self._log(f"Recursive call to '{func_name}' detected")
        self.generic_visit(node)

    def _analyze_loop_bound(self, node):
        """Heuristic to determine loop bound complexity."""
        # Defaults to O(n)
        bound = ComplexityTerm(1)
        desc = "linear (n)"

        if isinstance(node, ast.For):
            # Check range() calls
            if isinstance(node.iter, ast.Call) and isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                args = node.iter.args
                if len(args) > 0:
                    arg = args[-1] # Stop value
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, int):
                        bound = ComplexityTerm(0) # O(1)
                        desc = "constant"
                    elif isinstance(arg, ast.BinOp) and isinstance(arg.op, ast.Pow):
                        bound = ComplexityTerm(2) # Assume n^2
                        desc = "quadratic (n^2)"
        
        return bound, desc

    def visit_For(self, node):
        self._handle_loop(node, "For")

    def visit_While(self, node):
        self._handle_loop(node, "While")

    def _handle_loop(self, node, loop_type):
        bound_complexity, bound_desc = self._analyze_loop_bound(node)
        
        ctx = self._get_current_context()
        current_nesting = len(self.loop_stack)
        
        self._log(f"Loop at line {node.lineno}: {loop_type} loop with {bound_desc} bound", current_nesting)
        
        self.loop_stack.append(bound_complexity)
        
        # Visit children to find nested loops or operations
        self.generic_visit(node)
        
        # Calculate impact
        # The loop itself adds its bound * max(children complexity)
        # But for this simple analyzer, we are just tracking max nesting mostly.
        # Implemented logic: Any loop adds its power to the "current structure" complexity.
        
        self.loop_stack.pop()
        
        # Add this loop's contribution to the function's total time complexity
        # If we are nesting, the total power is sum of all stack powers.
        # But we need to update the function's max complexity.
        
        # Calculate the complexity of THIS loop chain
        chain_complexity = bound_complexity
        for parent in self.loop_stack:
            chain_complexity = chain_complexity * parent
            
        if ctx:
            ctx.time_complexity = ctx.time_complexity + chain_complexity
            self._log(f" -> Loop contributes {chain_complexity} to total", current_nesting)

    def visit_Assign(self, node):
        # Space complexity heuristics
        # list assignment or multiplication
        if isinstance(node.value, ast.List) or isinstance(node.value, ast.ListComp):
            self._add_space(ComplexityTerm(1), f"Line {node.lineno}: List allocation")
        
        # dict/set
        if isinstance(node.value, ast.Dict) or isinstance(node.value, ast.Set):
             self._add_space(ComplexityTerm(1), f"Line {node.lineno}: Dictionary/Set allocation")
             
        # Multiplcation like [0] * n
        if isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.Mult):
            # Check if one side is a list
            if isinstance(node.value.left, ast.List) or isinstance(node.value.right, ast.List):
                 self._add_space(ComplexityTerm(1), f"Line {node.lineno}: List multiplication allocation")

        self.generic_visit(node)

    def _add_space(self, complexity, reason):
        ctx = self._get_current_context()
        if ctx:
            ctx.space_complexity = ctx.space_complexity + complexity
            self._log(f"Space detection: {reason} -> {complexity}", len(self.loop_stack))

    def analyze(self, source_code):
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            return {"error": f"Syntax Error: {e}"}
            
        self.visit(tree)
        
        # If no functions, treat global breakdown as main
        results = {}
        if not self.functions:
            # Create a dummy main function results
            # Note: This simple generic visitor might not capture top-level efficiently without FunctionDef
            # But we visited everything.
            pass
            
        for name, analysis in self.functions.items():
            results[name] = {
                "time": str(analysis.time_complexity),
                "space": str(analysis.space_complexity),
                "breakdown": analysis.breakdown
            }
            
        # Overall max
        # Simple heuristic: Take the max of all functions
        overall_time = ComplexityTerm(0)
        overall_space = ComplexityTerm(0)
        for name, analysis in self.functions.items():
            overall_time = overall_time + analysis.time_complexity
            overall_space = overall_space + analysis.space_complexity
            
        return {
            "functions": results,
            "overall_time": str(overall_time),
            "overall_space": str(overall_space),
            "global_log": self.global_breakdown
        }
