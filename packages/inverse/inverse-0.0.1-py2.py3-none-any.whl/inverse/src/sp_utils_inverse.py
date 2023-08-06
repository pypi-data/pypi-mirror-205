
#filename:sp_utils_inverse.py
#folder:
#   Sermet.Pekin 2023
#   matrix ops
#   bkz README.md.
import random
import numpy as np
def key_format(r, name="name"):
    return f"{name}_{r}"
def memory_test(n, row=10):
    # numbers = list(random.randint(0, 100) for _ in range(n))
    big_numbers = []
    for i in range(row):
        # numbers = list(round(random.uniform(0, 1000000), 2) for _ in range(n))
        numbers = list(random.randint(0, 1_000_000) for _ in range(n))
        print(len(numbers))
        big_numbers.append(numbers)
    print(len(big_numbers))
    b = np.array(big_numbers)
    return b
def close_enough(sayi, buna, eps):
    return abs(sayi - buna) < eps
def inverse(mat):
    from scipy import linalg
    return linalg.inv(mat, overwrite_a=True)
    # return np.linalg.inv(mat)
class NotIdentity(BaseException):
    """Not an Identity Matrix"""
def close_identity_optimized(n, eps, data_source):
    # aug_matrix = np.column_stack((matrix, np.identity(n)))
    for i in range(n):
        pivot = data_source.get_row(i)[i]
        if close_enough(pivot, 1, eps):
            # aug_matrix[i] = aug_matrix[i] / pivot
            ...
        else:
            raise NotIdentity
        for j in range(n):
            if i != j:
                number = data_source.get_row(i)[j]
                if close_enough(number, 0, eps):
                    ...
                else:
                    raise NotIdentity
    print("Evet Bu bir Identity matrix")
    return True
def not_raise(dont_raise):
    if dont_raise:
        print("Not Identity matrix")
        return True
    else:
        raise NotIdentity
def close_identity(matrix, eps):
    n = len(matrix)
    # aug_matrix = np.column_stack((matrix, np.identity(n)))
    for i in range(n):
        pivot = matrix[i][i]
        if close_enough(pivot, 1, eps):
            # aug_matrix[i] = aug_matrix[i] / pivot
            ...
        else:
            not_raise(True)
            return False
        for j in range(n):
            if i != j:
                number = matrix[i][j]
                if close_enough(number, 0, eps):
                    ...
                else:
                    not_raise(True)
                    return False
    print("Evet Bu bir Identity matrix")
    return True
