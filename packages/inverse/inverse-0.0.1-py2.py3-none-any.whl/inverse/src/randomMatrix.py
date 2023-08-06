import numpy as np
from typing import Protocol
import random
from .pickle_works import Pickles
from .inverse_typings import *


class RandomMatrix():
    def __init__(self, NumberType=int, seed=None):
        self.number_type = self.type_converter(NumberType)
        self.seed = seed
        self.products = {}

    def type_converter(self, type_) -> str:
        obj = {int: "int", float: "float"}
        return obj[type_]

    def serialize(self, number_type: any, rows: int, cols: int, low: int_float, high: int_float) -> str:
        key = f"{number_type}{rows}{cols}{low}{high}"
        return key

    def check_products(self):
        # self.products
        ...

    def route(self) -> Callable:
        default = self.create_random_matrix_int
        # return default
        obj = {"int": self.create_random_matrix_int, "float": None}
        fnc = obj.get(self.number_type, default)
        return fnc

    def get(self, rows: int, cols: int, low: int_float, high: int_float) -> npar:
        if self.seed:
            print("seeding", self.seed)
            key = self.serialize(self.number_type, rows, cols, low, high)
            # matrix = self.products.get(key, None)
            if Pickles.check_pickle(key):
                print("returning cache")
                return Pickles.read_pickle(key)
        fnc = self.route()
        return fnc(rows, cols, low, high)

    def create_random_matrix_int(self,
                                 rows: int, cols: int,
                                 low: int_float, high: int_float) -> npar:
        # Create a random matrix with the given dimensions
        # matrix = np.random.rand(rows, cols)
        # matrix = np.random.randint(rows, cols )
        matrix = np.random.randint(low=low, high=high, size=(rows, cols))
        matrix = np.array(matrix)
        # dtype = np.int8
        key = self.serialize(self.number_type, rows, cols, low, high)
        Pickles.save_pickle(key, matrix)
        # self.products[key ] = matrix
        return matrix


def get_rand_matrix_int_seed(n: int) -> npar:
    random_matrix_int = RandomMatrix(int, seed=True)
    matrix = random_matrix_int.get(n, n, 0, 100)
    # print(matrix)
    return matrix


def get_rand_matrix_int_noseed(n: int) -> npar:
    random_matrix_int = RandomMatrix(int, seed=False)
    matrix = random_matrix_int.get(n, n, 0, 100)
    # print(matrix)
    return matrix
