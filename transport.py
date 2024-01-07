import numpy as np


class Transport:
    def __init__(self, M, S, D):
        # Check if the dimensions and supplies/demands are balanced
        assert M.shape[0] == S.shape[0], "Supply size must be equal to the size of rows."
        assert M.shape[1] == D.shape[0], "Demand size must be equal to the size of columns."
        assert sum(S) == sum(D), "Balanced problems only."

        # Initialize data and solution matrices
        self.M = M.copy()
        self.S = S.copy()
        self.D = D.copy()
        self.row_size = M.shape[0]
        self.col_size = M.shape[1]
        self.A = np.zeros((self.row_size, self.col_size))

    def copy_data(self):
        # Create copies of the original data matrices
        M = self.M.copy()
        S = self.S.copy()
        D = self.D.copy()
        self.A = np.zeros((self.row_size, self.col_size)
                          )  # Reset the solution matrix
        return M, S, D

    def calculate_z(self):
        # Calculate and return the total cost Z
        return np.sum(self.A * M)

    def print_solution(self):
        # Print the final solution matrix and the total cost Z
        print("\nFinal matrix: ")
        print(self.A)
        print("\nZ =", self.calculate_z())
        print()

    def get_min_index(self, M) -> tuple[int, int]:
        # Get the index of the minimum value in the given matrix
        min_index = np.argmin(M)
        return np.unravel_index(min_index, M.shape)

    def solve_north_west(self):
        # North-West Corner Rule method for initial solution
        M, S, D = self.copy_data()

        print("Initial matrix:")
        print(M)

        for i in range(self.row_size):
            for j in range(self.col_size):
                if self.S[i] == 0:
                    break

                self.A[i, j] = min(S[i], D[j])
                S[i] -= self.A[i, j]
                D[j] -= self.A[i, j]

    def solve_lowest_cost(self):
        # Lowest Cost method for initial solution
        M, S, D = self.copy_data()

        print("Initial matrix:")
        print(M)

        unprocessed_rows = list(range(self.row_size))
        unprocessed_cols = list(range(self.col_size))

        while unprocessed_rows and unprocessed_cols:
            # Find the minimum index in the submatrix of unprocessed rows and columns
            i, j = self.get_min_index(
                M[np.ix_(unprocessed_rows, unprocessed_cols)])
            i, j = unprocessed_rows[i], unprocessed_cols[j]

            # Perform the allocation
            self.A[i, j] = min(S[i], D[j])
            S[i] -= self.A[i, j]
            D[j] -= self.A[i, j]

            # Remove the row or column if the supply or demand has been exhausted
            unprocessed_rows = [r for r in unprocessed_rows if S[r] != 0]
            unprocessed_cols = [c for c in unprocessed_cols if D[c] != 0]

    def solve_vogel(self):
        # Vogel's Approximation method for initial solution
        M, S, D = self.copy_data()

        print("Initial matrix:")
        print(M)

        unprocessed_rows = list(range(self.row_size))
        unprocessed_cols = list(range(self.col_size))

        while unprocessed_rows and unprocessed_cols:
            # Calculate the differences between the two smallest costs in each row and column
            Vi = np.abs(np.diff(np.sort(M[unprocessed_rows, :], axis=1)[
                        :, :2], axis=1)).flatten()
            Vj = np.abs(np.diff(np.sort(M[:, unprocessed_cols], axis=0)[
                        :2, :], axis=0)).flatten()

            # Find the maximum difference
            max_diff = max(max(Vi), max(Vj))

            # Perform the allocation
            if max_diff in Vi:
                i = np.argmax(Vi)
                j = np.argmin(M[unprocessed_rows[i], unprocessed_cols])
            else:
                j = np.argmax(Vj)
                i = np.argmin(M[unprocessed_rows, unprocessed_cols[j]])

            # Map the indices back to their original values
            i, j = unprocessed_rows[i], unprocessed_cols[j]

            self.A[i, j] = min(S[i], D[j])
            S[i] -= self.A[i, j]
            D[j] -= self.A[i, j]

            # Remove the row or column if the supply or demand has been exhausted
            unprocessed_rows = [r for r in unprocessed_rows if S[r] != 0]
            unprocessed_cols = [c for c in unprocessed_cols if D[c] != 0]


# Example usage
M = np.array([
    [10, 12, 0],
    [8, 4, 3],
    [6, 9, 4],
    [7, 8, 5]
])

S = np.array([20, 30, 20, 10])
D = np.array([10, 40, 30])

transport = Transport(M, S, D)

print("*" * 35)
print("Testing North-West corner method")
print("*" * 35)
transport.solve_north_west()
transport.print_solution()

print("*" * 35)
print("Testing Lowest Cost method")
print("*" * 35)
transport.solve_lowest_cost()
transport.print_solution()

print("*" * 35)
print("Testing Vogel method")
print("*" * 35)
transport.solve_vogel()
transport.print_solution()
