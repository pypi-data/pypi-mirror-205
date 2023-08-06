from typing import Protocol
from numba import njit
import numpy as np

from .abstract_data import id_ekle
from .abstract_data2 import DBDataOpt
from .buffer_ops import Buffer
from .tuple_for_buffer import get_tuple_for_buffer
from .sp_matrix_ops import combine_row_op, divide_pivot


class MatrixCreator(Protocol):
    ...


class BigMatrix:
    def __init__(self, name: str, n: int, threshold: int):
        self.name = name
        self.n = n
        self.db_rep = DBDataOpt(threshold=threshold, name=self.name)
        self.threshold = threshold
        # post init
        self.buffer = Buffer(self)

    def get_current_matrix(self):
        return self.buffer.get_current_matrix()

    def display(self):
        print("I am a big matrix")

    def check(self):
        print("I am a big matrix")

    def inverse(self):
        print("I am a big matrix")
        inverse_mat = self.sp_inverse()
        return self

    def save_on_begin_rand(self, matrix: np.array):
        self.db_rep.save_on_begin_rand(matrix)

    def sp_inverse(self) -> np.array:
        """TODO"""

        for sira in get_tuple_for_buffer(self.n, self.threshold):
            sira = tuple(x for x in sira if x < self.n)
            x, *y = sira
            self.buffer.load_column_names_with_set(sira)
            # print("now x " , x , sira )
            for i in [x]:
                # print("Sıradaki satır numarası : ", i, "*" * 10)
                row = tuple(self.buffer.get_row(i))
                pivot = row[i]
                row = divide_pivot(row, pivot)
                self.buffer.set_row(i, row)
                for j in y:
                    if i != j:
                        number_j = self.buffer.get_cell(j, i)
                        number_i = self.buffer.get_cell(i, i)
                        if number_i != 0:
                            factor = number_j / number_i
                        else:
                            factor = 0
                        row_J = self.buffer.get_row(j)
                        row_i = self.buffer.get_row(i)
                        nrow = combine_row_op(row_J, row_i, factor)
                        self.buffer.set_row(j, nrow)
            self.buffer.final_save()
        inv_matrix = self.buffer.get_current_matrix()
        self.id_and_inv = inv_matrix
        return inv_matrix[:, self.n:]


class BigMatrixConverter:
    def __init__(self, name):
        self.name = name

    def convert_small_to_bigmatrix(self,
                                   matrix: np.array,
                                   threshold: int) -> BigMatrix:
        big_matrix = BigMatrix(self.name, len(matrix), threshold)
        big_matrix.db_rep.save_on_begin_rand(matrix)
        return big_matrix
