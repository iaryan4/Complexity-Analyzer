# Test Case 1: Constant Time
def constant_example():
    x = 10
    y = 20
    return x + y

# Test Case 2: Linear Time
def linear_example(n):
    total = 0
    for i in range(n):
        total += i
    return total

# Test Case 3: Quadratic Time (Nested Loops)
def quadratic_example(n):
    for i in range(n):
        for j in range(n):
            print(i, j)

# Test Case 4: Deeply Nested
def deep_nested_example(n):
    for i in range(n):
        while True:
            for j in range(n):
                 print("Deep")
            break
