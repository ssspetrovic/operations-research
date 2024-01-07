import numpy as np
from numpy.linalg import matrix_rank
from numpy.linalg import LinAlgError

from itertools import combinations


class Simplex:
    def validate_matrix(self, A: np.ndarray, b: np.ndarray, C: np.ndarray, target: str) -> AssertionError | None:
        assert target in [
            'max', 'min'], "Only min and max problems can be solved!"
        assert A.shape[0] == b.shape[0], "A row length must be equal to b row length!"
        assert A.shape[1] == C.shape[1], "A column length must be equal to C column length!"

    def check_singularity(self, matrix: np.ndarray) -> ValueError | None:
        if matrix_rank(matrix) < matrix.shape[0]:
            raise ValueError("Matrix cannot be singular!")

    def __init__(self, A: np.ndarray, b: np.ndarray, C: np.ndarray, target: str) -> None:
        self.validate_matrix(A, b, C, target)
        self.A = A
        self.b = b
        self.C = C
        self.target = target
        self.B_indexes = []
        self.N_indexes = []

    def is_finished(self, differences: np.ndarray) -> bool:
        return np.all(differences >= 0) if self.target == 'max' else np.all(differences <= 0)

    def solve(self, limit: int = 10) -> None:
        b = self.b

        # Creating the identity matrix with the dimensions of A
        I = np.eye(self.A.shape[0])
        O = np.zeros((1, len(b)))
        A = np.hstack((self.A, I))
        C = np.hstack((self.C, O))

        (m, n) = A.shape

        self.check_singularity(A)
        B_inv = None
        try:
            self.B_indexes = [*range(n - m, n)]
            self.N_indexes = [i for i in range(
                n) if i not in self.B_indexes]
            B_inv = np.linalg.inv(A[:, self.B_indexes])
            X_b = B_inv @ b
            if (X_b < 0).any():
                B_inv = None
        except LinAlgError:  # if the matrix cannot be inverted, move on
            pass

        if B_inv is None:
            combs = list(combinations([*range(n)], len(b)))

            for comb in combs:
                self.B_indexes = list(comb)
                self.N_indexes = [i for i in range(
                    n) if i not in self.B_indexes]

                try:
                    B_inv = np.linalg.inv(A[:, self.B_indexes])
                    X_b = B_inv @ b

                    if (X_b < 0).any():
                        break
                except LinAlgError:  # if the matrix cannot be inverted, move on
                    pass

        it_no = 1

        omega = C[:, self.B_indexes] @ B_inv
        b_ = B_inv @ b
        Z = C[:, self.B_indexes] @ b_

        while it_no < limit:
            # Z_j = omega * a_j
            differences = omega @ A[:, self.N_indexes] - \
                C[:, self.N_indexes]  # Z_j - C_j

            if self.is_finished(differences):
                self.Z = Z[0][0]
                self.solution = tuple(b_.flatten())
                self.it_no = it_no
                break

            # k-index is the new base index
            k = np.argmin(differences) if self.target == 'max' else np.argmax(
                differences)
            k_difference = differences[:, k]
            k = self.N_indexes[k]

            # Y_k = B^(-1) a_k
            Y_k = B_inv @ A[:, k]
            Y_k = Y_k.reshape(B_inv.shape[0], 1)
            # min from b_ / Yk
            np.seterr(divide='ignore', invalid='ignore')
            quotient = b_ / Y_k
            # Also represents the index of the new non base index
            pivot_row = np.argmin([val for val in quotient if val >= 0])

            non_pivot_rows = [i for i in range(
                B_inv.shape[0]) if i != pivot_row]

            e_p = Y_k[pivot_row][0]
            e_r = B_inv[pivot_row, :]
            # e_c = Y_k[row][0]

            # This line handles all of the non-pivot row elements of B_inv
            B_inv[non_pivot_rows, :] -= [e_r * Y_k[row]
                                         [0] / e_p for row in non_pivot_rows]

            b_[non_pivot_rows] -= b_[pivot_row] * Y_k[non_pivot_rows] / e_p

            # Updating omega values accordingly
            omega[0] -= B_inv[pivot_row] * k_difference / e_p

            # Updating C_B * b_ value
            Z -= b_[pivot_row] * k_difference / e_p

            # This line handles the pivot row elements
            B_inv[pivot_row] = B_inv[pivot_row] / e_p
            b_[pivot_row] = b_[pivot_row] / e_p

            tmp = self.N_indexes[k]
            self.N_indexes[k] = self.B_indexes[pivot_row]
            self.B_indexes[pivot_row] = tmp
            self.N_indexes.sort()

            it_no += 1

    def print_solution(self) -> None:
        print(f"Number of iterations: {self.it_no}")
        print(f"Z = {self.Z}")
        print("\nBase variables:")
        for i in range(len(self.B_indexes)):
            print(f" X{self.B_indexes[i]} = {self.solution[i]}")

        print("\nNon-base variables:")
        for i in range(len(self.N_indexes)):
            print(f" X{self.N_indexes[i]} =", end='')
        print(' 0')


tests = []

A = np.array([
    [0.5, 2, 1],
    [1, 2, 4]
])

b = np.array([
    [24],
    [60]
])

C = np.array([
    [6, 14, 13]
])

target = 'max'
tests.append({'target': target, 'A': A, 'b': b, 'C': C})

A = np.array([
    [1, 0, 1],
    [0, 2, 0],
    [3, 2, 0, ]
])

b = np.array([
    [4],
    [12],
    [18]
])

C = np.array([
    [3, 5, 0]
])

target = 'max'
tests.append({'target': target, 'A': A, 'b': b, 'C': C})


A = np.array([
    [1,  1,  1, 1, 1, 1],
    [2, -1, -2, 1, 0, 0],
    [0,  0,  1, 1, 2, 1]
])

b = np.array([
    [6],
    [4],
    [4]
])

C = np.array([
    [-1, -2, 1, -1, -4, 2]
])

target = 'min'
tests.append({'target': target, 'A': A, 'b': b, 'C': C})

for i, test in enumerate(tests):
    print(f"\n============== Running test {
          i + 1} - {test['target'].upper()} ==============")
    simplex = Simplex(test['A'], test['b'], test['C'], test['target'])
    simplex.solve()
    simplex.print_solution()
