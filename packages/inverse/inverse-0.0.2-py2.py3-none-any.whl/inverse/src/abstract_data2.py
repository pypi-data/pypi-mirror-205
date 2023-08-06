from .abstract_data import id_ekle, DataAbstract
from .db_ops import DB_class_Opt
from .partition import table_name_format

from .inverse_typings import *


class DBDataOpt(DataAbstract):
    buffer: dict = {}

    def __init__(self, threshold: int, name="test"):
        self.threshold = threshold
        self.name = name
        self.db_option = DB_class_Opt

    def key_format(self, r: int, name=False) -> str:
        if not name:
            name = self.name
        return f"{name}_{r}"

    def transpose_list(self, big_list: list_tuple, say: int) -> pddf:
        def get_name(index):
            return f"column_{self.threshold * (say) + index}"

        column_names = list(map(get_name, range(0, self.threshold)))

        df_t = pd.DataFrame(big_list).transpose()

        if len(df_t.columns) < self.threshold:
            column_names = column_names[0:  len(df_t.columns)]
        df_t.columns = column_names
        return df_t

    def save_part(self, say: int, big_list: list_tuple) -> None:

        self.db_option.write_db(table_name_format(self.name, say)
                                , self.transpose_list(big_list, say))

    def save_on_begin_rand(self, matrix: npar) -> None:

        say = -1
        big_list = []
        for i in range(len(matrix)):
            numbers = list(matrix[i])  # list(random.randint(0, 100) for _ in range(n))
            numbers += id_ekle(i, len(matrix))
            if len(big_list) == self.threshold:
                say += 1
                self.save_part(say, big_list)
                big_list = [numbers]
            else:
                big_list.append(numbers)
        if big_list:
            say += 1
            self.save_part(say, big_list)


def get_test_row(i):
    matrix = [[9, 17, 12], [2, 19, 12], [26, 8, 12]]
    return matrix[i]
