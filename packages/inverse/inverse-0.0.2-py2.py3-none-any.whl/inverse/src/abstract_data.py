#   Sermet.Pekin 2023
#   matrix ops
#   bkz README.md.
import random
import numpy as np

from .inverse_typings import *
from .pickle_file import read_pickle, save_pickle
from abc import ABC, abstractmethod


def id_ekle(i: int, n: int):
    liste = list(0 for x in range(n))
    liste[i] = 1
    return liste


class DataAbstract():
    buffer: dict = {}

    @abstractmethod
    def __init__(self, threshold: int, name="test"):
        """"""

    @abstractmethod
    def key_format(self, r: int, name=False) -> str:
        """"""

    @abstractmethod
    def transpose_list(self, big_list: list_tuple, say: int) -> pddf:
        """"""

    @abstractmethod
    def save_part(self, say: int, big_list: list_tuple) -> None:
        """ save_part """

    @abstractmethod
    def save_on_begin_rand(self, matrix: npar) -> None:
        """save_on_begin_rand"""


class DataAbstract22(ABC):
    @abstractmethod
    def get_original_matrix(self, n):
        ...

    @abstractmethod
    def get_current_matrix(self, n):
        ...

    @abstractmethod
    def get_row(self, r: int, stable=False):
        ...

    @abstractmethod
    def set_row(self, i: int, data, name="name"):
        ...

    @abstractmethod
    def get_cell(self, r: int, c: int):
        ...

    @abstractmethod
    def save_on_begin_rand(self, n):
        ...


class PickleData(DataAbstract):
    def get_original_matrix(self, n) -> npar:
        rows = []
        for i in range(n):
            row = read_pickle("name_original" + str(i))
            rows.append(row)
        array = np.array(rows)
        return array[:, :n]

    def get_current_matrix(self, n: int) -> npar:
        if n > 50:
            print("n çok büyük olduğu için matrixe dönüştürmüyorum.")
            print("satır satır okumak için bkz. get_row(i) ")
            return
        rows = []
        for i in range(n):
            row = self.get_row(i)
            rows.append(row)
        array = np.array(rows)
        return array[:, n:]

    def get_row(self, r: int, stable=False):
        return read_pickle("name" + str(r))

    def set_row(self, i: int, data, name="name"):
        save_pickle(name + str(i), data)

    def get_cell(self, r: int, c: int):
        row = self.get_row(r)
        return row[c]

    def save_on_begin_rand(self, n):
        for i in range(n):
            numbers = list(random.randint(0, 100) for _ in range(n))
            numbers += id_ekle(i, n)
            # print(numbers)
            self.set_row(i, numbers)
            if n < 100:
                self.set_row(i, numbers, "name_original")
