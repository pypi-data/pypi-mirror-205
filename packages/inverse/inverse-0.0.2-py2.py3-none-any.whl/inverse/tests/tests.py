from inverse.src.tuple_for_buffer import get_tuple_for_buffer
from inverse import *


def test_main():
    n = 10  # 100 : 16sn ,10:1sn
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


def test_siralar(capsys):
    n = 12
    threshold = 5
    siralar = get_tuple_for_buffer(n, threshold)
    with capsys.disabled():
        print(siralar)
# ntest_siralar()
