import numpy as np

from string import ascii_uppercase


class Hungarian:
    def __init__(self, M) -> None:
        assert M.shape[0] == M.shape[1], "Matrix must be square!"
        self.len = M.shape[0]
        self.row_names = [i for i in range(1, self.len + 1)]
        self.col_names = list(ascii_uppercase)[:self.len]
        self.M = M

    def solve(self):
        print(self.M)

        # Subtract the minimum element from each element row-wise
        self.M -= self.M.min(axis=1, keepdims=True)

        # Mark the columns that don't contain 0
        marked_col_indexes = np.where(~(M == 0).any(axis=0))[0]
        # print(marked_col_indexes)
        self.M[:, marked_col_indexes] -= self.M[:,
                                                marked_col_indexes].min(axis=0, keepdims=True)

        # Find independent zeros and mark their corresponding zeros
        
        i = 1

        for i in range(4):
            print(i)
            print(self.M)
            independent_indexes = set()
            crossed_indexes = set()
            zero_indices = np.argwhere(self.M == 0)
            for row, col in zero_indices:
                if (row, col) not in independent_indexes and (row, col) not in crossed_indexes:
                    independent_indexes.add((row, col))
                    crossed_indexes.update((row, c) for c in np.where(self.M[row, :] == 0)[
                        0] if (row, c) not in independent_indexes)
                    crossed_indexes.update((r, col) for r in np.where(self.M[:, col] == 0)[
                        0] if (r, col) not in independent_indexes)

            print("Independent zeros", independent_indexes)
            print("Crossed zeros", crossed_indexes)

            # Mark the rows where there aren't any independent zeros
            all_indexes = set(range(self.len))
            independent_row_indexes = set(index[0]
                                          for index in independent_indexes)

            independent_col_indexes = set(
                index[1] for index in independent_indexes)

            print("all", all_indexes)
            print("independent col", independent_col_indexes)
            if all_indexes == independent_col_indexes:
                print("")
                break  # Exit the loop if all columns have independent zeros

            marked_row_indexes = all_indexes - independent_row_indexes

            print("Marked row indexes", marked_row_indexes)  # Correct

            # Cross all of the columns that contain zero in marked rows
            crossed_col_indexes = set()  # Use a set to avoid duplicates
            for row in marked_row_indexes:
                for i in range(self.len):
                    if self.M[row, i] == 0:
                        crossed_col_indexes.add(i)

            # crossed_col_indexes = list(crossed_col_indexes)
            print("Crossed columns", crossed_col_indexes)  # Correct

            # Mark all of the rows that don't contain independent zero in the crossed column
            for col in crossed_col_indexes:
                independent_rows = {index[0]
                                    for index in independent_indexes if index[1] == col}
                for r in range(self.len):
                    if self.M[r, col] == 0 and r in independent_rows:
                        marked_row_indexes.add(r)

            print("Marked rows", marked_row_indexes)
            crossed_row_indexes = all_indexes - marked_row_indexes
            print("Crossed rows", crossed_row_indexes)
            print("Crossed columns", crossed_col_indexes)

            regular_row_indexes = np.array(
                list(all_indexes - crossed_row_indexes))
            regular_col_indexes = np.array(
                list(all_indexes - crossed_col_indexes))

            min_el = min(self.M[i, j]
                         for i in regular_row_indexes for j in regular_col_indexes)
            print("Minimum element:", min_el)

            self.M[np.ix_(list(regular_row_indexes), list(
                regular_col_indexes))] -= min_el
            self.M[np.ix_(list(crossed_row_indexes), list(
                crossed_col_indexes))] += min_el

            print(self.M)


M = np.array([
    [10, 4, 6, 10, 12],
    [11, 7, 7, 9, 14],
    [13, 8, 12, 14, 15],
    [14, 16, 13, 17, 1],
    [17, 11, 17, 20, 19]
])

hungarian = Hungarian(M)
hungarian.solve()
