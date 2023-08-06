from .inverse_typings import *

bulk_ = []
big_bulk = []


def number_gen(n) -> Iterable:
    for i in range(n):
        yield i


def number_gen_x(n) -> Iterable:
    x = 0
    while x < n:
        yield x
        x += 1


def get_tuple_for_buffer(n: int, threshold: int) -> tuple:
    big_list = []
    liste = []
    for x in number_gen_x(n + 1):
        if liste:
            big_list.append(liste)
        liste = [x]
        for y in number_gen(n):
            _, *new_items = liste
            if not new_items or max(new_items) < y:
                liste.append(y)
            if len(liste) > threshold:
                big_list.append(liste)
                liste = [x]
    return tuple(big_list)
