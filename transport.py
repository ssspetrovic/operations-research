import numpy as np


class Transport:
    def __init__(self, M, S, D):
        assert M.shape[0] == S.shape[0], "Supply size must be equal to the size of rows."
        assert M.shape[1] == D.shape[0], "Demand size must be equal to the size of columns."
        assert sum(S) == sum(D), "Balanced problems only."
        self.M = M.copy()
        self.S = S.copy()
        self.D = D.copy()
        self.row_size = M.shape[0]
        self.col_size = M.shape[1]
        self.A = np.zeros((self.row_size, self.col_size))

    def calculate_z(self):
        return np.sum(self.A * M)

    def print_solution(self):
        print("\nFinal matrix: ")
        print(self.A)
        print("\nZ =", self.calculate_z())
        print()

    def get_min_index(self, M) -> tuple[int, int]:
        min_index = np.argmin(M)
        return np.unravel_index(min_index, M.shape)

    def solve_north_west(self):
        M = self.M.copy()
        S = self.S.copy()
        D = self.D.copy()
        self.A = np.zeros((self.row_size, self.col_size))

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
        M = self.M.copy()
        S = self.S.copy()
        D = self.D.copy()
        self.A = np.zeros((self.row_size, self.col_size))

        print(M)

        unprocessed_rows = list(range(self.row_size))
        unprocessed_cols = list(range(self.col_size))

        while unprocessed_rows and unprocessed_cols:
            i, j = self.get_min_index(
                M[np.ix_(unprocessed_rows, unprocessed_cols)])
            i, j = unprocessed_rows[i], unprocessed_cols[j]

            self.A[i, j] = min(S[i], D[j])
            S[i] -= self.A[i, j]
            D[j] -= self.A[i, j]

            if S[i] == 0:
                unprocessed_rows.remove(i)

            if D[j] == 0:
                unprocessed_cols.remove(j)

    def solve_vogel(self):
        pass


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

