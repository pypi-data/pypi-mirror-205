import random

from inverse.src.abstract_data import id_ekle
from inverse.src.sp_matrix_ops import save_on_begin, save_pickle


def save_on_begin_rand(n):
    for i in range(n):
        numbers = list(random.randint(0, 100) for _ in range(n))
        numbers += id_ekle(i, n)
        print(numbers)
        save_pickle("name" + str(i), numbers)


def test_save_on_begin_rand():
    # save_on_begin_rand(10)
    print("test")


def test_main2():
    # test_siralar()
    ...
