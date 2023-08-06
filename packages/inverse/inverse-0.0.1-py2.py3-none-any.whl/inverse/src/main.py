
import numpy as np
from .check_result import inverse_check
from .matrix_converters import BigMatrixConverter
from .randomMatrix import get_rand_matrix_int_seed, get_rand_matrix_int_noseed
from .sp_matrix_ops import display_matrix_ozet
from .sp_utils_inverse import close_identity
from .sure import tic, toc
def get_matrix_for_test(n):
    return get_rand_matrix_int_seed(n)
    # return get_rand_matrix_int_noseed(n)
def main():
    n = 10 #                   100 : 16sn ,10:1sn
    threshold = 500
    matrix = get_matrix_for_test(n)
    print(matrix)
    matrix_check = inverse_check(matrix)
    converter = BigMatrixConverter("test")
    big_matrix = converter.convert_small_to_bigmatrix(matrix, threshold=threshold)  # class bigMatrix
    tic()
    inv_big_matrix = big_matrix.sp_inverse()  # class bigMatrix
    toc()
    display_matrix_ozet(inv_big_matrix, "inv_big_matrix")
    display_matrix_ozet(inv_big_matrix, "inv_big_matrix main")
    display_matrix_ozet(matrix_check, "matrix_check")
    sonuc = np.matmul(matrix, inv_big_matrix)
    sonuc2 = np.matmul(matrix, matrix_check)
    display_matrix_ozet(sonuc, "sonuc A * A(-1)")
    display_matrix_ozet(sonuc2, "sonuc2 matrix_check A * A(-1)")
    eps = 0.0001
    kontrol = close_identity(matrix=sonuc, eps=eps)
    kontrol2 = close_identity(matrix=sonuc2, eps=eps)
    # inv_big_matrix.display()
    # inv_big_matrix.check()
if __name__ == "__main__":
    main()


def a2():
    tic()
    n = 60
    threshold = 500
    matrix = get_matrix_for_test(n)
    
    toc()