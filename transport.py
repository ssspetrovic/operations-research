import numpy as np


class Transport:
    def __init__(self, M, S, D):
        assert M.shape[0] == S.shape[0], "Supply size must be equal to the size of rows."
        assert M.shape[1] == D.shape[0], "Demand size must be equal to the size of columns."
        assert sum(S) == sum(D), "Balanced problems only."
        self.M = M
        self.S = S
        self.D = D
        self.row_size = M.shape[0]
        self.col_size = M.shape[1]
        self.A = np.zeros((self.row_size, self.col_size))

    def calculate_z(self):
        Z = 0
        for i in range(self.row_size):
            for j in range(self.col_size):
                if self.A[i, j] != 0:
                    Z += self.A[i, j] * self.M[i, j]
        return Z

    def print_solution(self):
        print("\nFinal matrix: ")
        print(self.A)
        print("\nZ =", self.calculate_z())

    def solve_north_west(self):
        print(self.M)

        for i in range(self.row_size):
            for j in range(self.col_size):
                if self.S[i] == 0:
                    break

                self.A[i, j] = self.D[j] if self.S[i] - \
                    self.D[j] >= 0 else self.S[i]

                self.S[i] -= self.A[i, j]
                self.D[j] -= self.A[i, j]

    def solve_lowest_cost(self):
        pass

    def solve_vogel(self):
        pass


M = np.array([
    [10, 12, 20],
    [8, 4, 3],
    [6, 9, 4],
    [7, 8, 5]
])

S = np.array([20, 30, 20, 10])
D = np.array([10, 40, 30])

nw = Transport(M, S, D)
nw.solve_north_west()
nw.print_solution()
