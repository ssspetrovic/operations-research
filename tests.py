# Import necessary libraries
import numpy as np
from simplex import Simplex
from hungarian import Hungarian
from transport import Transport

# Define separators for better readability
method_separator = "=" * 30
inter_separator = "-" * 75
transport_case_separator = "*" * 27

# Simplex Method Tests
print("\n", method_separator, "Simplex Method", method_separator, "\n")

tests = [
    {
        'target': 'max',
        'A': np.array([[0.5, 2, 1], [1, 2, 4]]),
        'b': np.array([[24], [60]]),
        'C': np.array([[6, 14, 13]])
    },
    {
        'target': 'max',
        'A': np.array([[1, 0, 1], [0, 2, 0], [3, 2, 0]]),
        'b': np.array([[4], [12], [18]]),
        'C': np.array([[3, 5, 0]])
    },
    {
        'target': 'min',
        'A': np.array([[1, 1, 1, 1, 1, 1], [2, -1, -2, 1, 0, 0], [0, 0, 1, 1, 2, 1]]),
        'b': np.array([[6], [4], [4]]),
        'C': np.array([[-1, -2, 1, -1, -4, 2]])
    }
]

for i, test in enumerate(tests):
    print("\nRunning test", i + 1, "-", test['target'].upper())
    simplex = Simplex(test['A'], test['b'], test['C'], test['target'])
    simplex.solve()
    simplex.print_solution()


# Hungarian Method Tests
print("\n", method_separator, "Hungarian Method", method_separator, "\n")

matrices = [
    np.array([
        [10, 4, 6, 10, 12],
        [11, 7, 7, 9, 14],
        [13, 8, 12, 14, 15],
        [14, 16, 13, 17, 1],
        [17, 11, 17, 20, 19]
    ]),
    np.array([
        [10, 4, 6, 10, 12],
        [11, 7, 7, 9, 14],
        [13, 8, 12, 14, 15],
        [14, 16, 13, 17, 1],
        [17, 11, 17, 20, 19]
    ]) * 10
]

for i, matrix in enumerate(matrices):
    print("\nSolving matrix", i + 1)
    hungarian = Hungarian(matrix)
    hungarian.solve()
    hungarian.print_solution()
    if i != len(matrices) - 1:
        print(inter_separator)

# Transport Method Tests
print("\n", method_separator, "Transport Method", method_separator, "\n")

test_cases = [
    {
        'M': np.array([
            [10, 12, 0],
            [8, 4, 3],
            [6, 9, 4],
            [7, 8, 5]
        ]),
        'S': np.array([20, 30, 20, 10]),
        'D': np.array([10, 40, 30])
    },
    {
        'M': np.array([
            [20, 11, 15, 13],
            [17, 14, 12, 13],
            [15, 12, 18, 18]
        ]),
        'S': np.array([2, 6, 7]),
        'D': np.array([3, 3, 4, 5])
    }
]

methods = ['north_west', 'lowest_cost', 'vogel']

for i, test_case in enumerate(test_cases):
    print(transport_case_separator, f"Running Test Case {i+1}", transport_case_separator)
    transport = Transport(test_case['M'], test_case['S'], test_case['D'])
    for method in methods:
        print("\nTesting", method.replace('_', ' ').title(), "Method\n")
        getattr(transport, f"solve_{method}")()
        transport.print_solution()
        print(inter_separator)
