import numpy as np
from string import ascii_uppercase


class Hungarian:
    def __init__(self, M: np.ndarray) -> None:
        assert M.shape[0] == M.shape[1], "Matrix must be square!"
        self.size = M.shape[0]
        self.persons = [i for i in range(1, self.size + 1)]
        self.jobs = list(ascii_uppercase)[:self.size]
        self.original = M
        self.M = M.copy()
        self.Z = 0
        self.independent_indexes = []

    def process_zero(self, index: tuple[int, int], independent_indexes: set, crossed_indexes: set) -> None:
        # Process a single zero
        independent_indexes.add(index)

        for ind in range(self.size):
            if self.M[ind, index[1]] == 0 and ind != index[0] and ind not in {i[0] for i in independent_indexes}:
                crossed_indexes.add((ind, index[1]))

            if self.M[index[0], ind] == 0 and ind != index[1] and ind not in {i[1] for i in independent_indexes}:
                crossed_indexes.add((index[0], ind))

    def assign_jobs(self, independent_indexes: set) -> None:
        # Assign the jobs based on the final matrix
        for p, j in sorted(independent_indexes, key=lambda x: x[0]):
            print(f" Person {self.persons[p]
                             } should work on job {self.jobs[j]}")
            self.Z += self.original[p, j]

    def print_solution(self) -> None:
        print("\nFinal matrix:")
        print(self.M)
        print("\nJob schedule:")
        self.assign_jobs(self.independent_indexes)
        print("\nZ =", self.Z)

    def solve(self) -> None:
        print(self.M)

        # Subtract the minimum element from each element row-wise
        self.M -= self.M.min(axis=1, keepdims=True)

        # Mark the columns that don't contain 0
        marked_col_indexes = np.where(~(self.M == 0).any(axis=0))[0]
        self.M[:, marked_col_indexes] -= self.M[:,
                                                marked_col_indexes].min(axis=0, keepdims=True)

        while True:
            independent_indexes = set()
            crossed_indexes = set()
            all_indexes = set(range(self.size))

            processed_rows = set()
            unprocessed_rows = all_indexes - processed_rows

            # Find independent zeros and mark their corresponding zeros
            flag = True

            while True:
                rows_to_remove = set()

                for row in unprocessed_rows.copy():
                    zero_cols = np.where(self.M[row, :] == 0)[0]
                    uncrossed_zero_cols = [col for col in zero_cols if (
                        row, col) not in crossed_indexes]

                    if flag and len(uncrossed_zero_cols) == 1:
                        self.process_zero(
                            (row, uncrossed_zero_cols[0]), independent_indexes, crossed_indexes)
                        rows_to_remove.add(row)
                    elif not flag and len(uncrossed_zero_cols) != 0:
                        self.process_zero(
                            (row, uncrossed_zero_cols[0]), independent_indexes, crossed_indexes)
                        rows_to_remove.add(row)
                        flag = True
                        break

                unprocessed_rows -= rows_to_remove
                rows_to_remove = set()
                flag = False

                zero_indices = np.argwhere(self.M == 0)
                uncrossed_zero_indices = [(row, col) for row, col in zero_indices if
                                          (row, col) not in independent_indexes and (row, col) not in crossed_indexes]

                if len(uncrossed_zero_indices) == 0:
                    break

            independent_row_indexes = {index[0]
                                       for index in independent_indexes}
            independent_col_indexes = {index[1]
                                       for index in independent_indexes}

            if all_indexes == independent_col_indexes:
                self.independent_indexes = independent_indexes
                break  # Exit the loop if all columns have independent zeros

            marked_row_indexes = all_indexes - independent_row_indexes
            crossed_col_indexes = set()

            for row in marked_row_indexes:
                for i in range(self.size):
                    if self.M[row, i] == 0:
                        crossed_col_indexes.add(i)

            for col in crossed_col_indexes:
                independent_rows = {
                    index[0] for index in independent_indexes if index[1] == col}
                for r in range(self.size):
                    if self.M[r, col] == 0 and r in independent_rows:
                        marked_row_indexes.add(r)

            crossed_row_indexes = all_indexes - marked_row_indexes
            regular_row_indexes = np.array(
                list(all_indexes - crossed_row_indexes))
            regular_col_indexes = np.array(
                list(all_indexes - crossed_col_indexes))

            min_el = min(self.M[i, j]
                         for i in regular_row_indexes for j in regular_col_indexes)

            self.M[np.ix_(list(regular_row_indexes), list(
                regular_col_indexes))] -= min_el
            self.M[np.ix_(list(crossed_row_indexes), list(
                crossed_col_indexes))] += min_el
