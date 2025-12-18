# Test 1: Constant Loop bound -> O(1)
def constant_loop():
    x = 0
    for i in range(100): # Should be O(1)
        x += 1
    return x

# Test 2: Linear Loop bound -> O(n)
def linear_loop(n):
    x = 0
    for i in range(n): # O(n)
        x += 1
    return x

# Test 3: Quadratic loop bound -> O(n^2)
def quadratic_loop(n):
    for i in range(n*n): # O(n^2)
        print(i)

# Test 4: Nested Loops (O(n) * O(n)) -> O(n^2)
def nested_loops(n):
    count = 0
    for i in range(n):
        for j in range(n):
            count += 1

# Test 5: Recursion -> O(n) Time, O(n) Space
def factorial(n):
    if n <= 1: 
        return 1
    return n * factorial(n-1)

# Test 6: Space Complexity (List creation in loop) -> O(n)
def space_waster(n):
    result = []
    for i in range(n):
        result.append(i) # O(n) space
    return result

# Test 7: Complex Mix
def complex_algo(n):
    # O(n)
    for i in range(n):
        pass
        
    # O(n^2)
    for i in range(n):
        for j in range(n):
            pass
            
    # O(1)
    for k in range(500):
        pass
