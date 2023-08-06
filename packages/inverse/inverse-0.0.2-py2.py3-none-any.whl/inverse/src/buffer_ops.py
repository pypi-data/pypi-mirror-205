import numpy as np
from .db_ops import DB_class_Opt
from .partition import get_table_name_treshold, table_name_format, column_name_format, table_name_format_reverse
from .inverse_typings import *


def get_table_names_from_tuple(liste: list_tuple, threshold: int) -> list_tuple:
    new_set = []
    for i in liste:
        num = get_table_name_treshold(i, threshold)
        if num not in new_set:
            new_set.append(num)
    return tuple(new_set)


class Buffer:
    def __init__(self, bigmatrix):
        self.buffer_data = {}
        self.bigmatrix = bigmatrix
        self.threshold = self.bigmatrix.threshold
        self.name = self.bigmatrix.name
        self.columns = []
        self.columns_tables_dict = {}

    def buffer_to_matrix(self) -> npar:
        def get(name: str):
            keyname = self.columns_tables_dict[name]
            return self.buffer_data[keyname][name]

        keys = tuple(self.columns_tables_dict.keys())
        rows = (x for x in keys if x not in ("index", "level_0"))
        # print(tuple(rows))
        liste = tuple(map(get, rows))
        # liste = tuple(x for x in liste if x)
        return np.array(liste)

    def get_current_matrix(self) -> npar:
        n = self.bigmatrix.n
        new_set = get_table_names_from_tuple(tuple(x for x in range(n)), self.threshold)
        self.load_buffer(new_set)
        matrix = self.buffer_to_matrix()
        return matrix

    def buffer_get_current_key_nums(self) -> tuple:
        keys = tuple(self.buffer_data.keys())
        result = tuple(map(table_name_format_reverse, keys))

        return result

    def buffer_key_format(self, say: int) -> str:
        return table_name_format(self.name, say)

    def load_buffer(self, diff_set: list_tuple) -> None:
        """burada desteleri yükleyecek"""
        # if diff_set == ("0",):
        #     return
        # print("loading", diff_set)

        for set_say in diff_set:
            # num = get_table_name_treshold(say, self.threshold)
            table_name = table_name_format(self.name, set_say)
            buffer_key = self.buffer_key_format(set_say)
            try:
                df_gelen = DB_class_Opt.read_db(table_name)
                for column in tuple(df_gelen.columns):
                    self.columns_tables_dict[column] = buffer_key
                self.buffer_data[buffer_key] = df_gelen

            except:
                print("load_buffer prob. table_name", table_name)
                # return False

    def save_buffer(self) -> None:
        for table_name in tuple(self.buffer_data.keys()):
            try:
                DB_class_Opt.write_db(table_name, self.buffer_data[table_name])
            except:
                print("bunu bulamadım save_buffer ", table_name)

    def empty_buffer(self, tuple_set=()) -> None:
        self.save_buffer()
        if tuple_set:
            for item in tuple_set:
                self.buffer_data.pop(item)
        else:
            self.buffer_data = {}

    def refresh_buffer(self, new_set: list_tuple) -> None:
        old_set = self.buffer_get_current_key_nums()
        diff_set_garbage = tuple(x for x in old_set if x not in new_set)
        diff_set_load = tuple(x for x in new_set if x not in old_set)

        # print("old_set", old_set)
        # print("diff_set_garbage", diff_set_garbage)
        # print("diff_set_load", diff_set_load)
        # print("new_set", new_set)
        # exit()
        # if not old_set :
        #     diff_set_load = new_set
        self.empty_buffer(diff_set_garbage)
        self.load_buffer(diff_set_load)

    def load_column_names_with_set(self, column_tuple: list_tuple) -> None:
        column_tuple = tuple(set(column_tuple))

        # print("load_column_names_with_set column_tuple", column_tuple)
        new_set = get_table_names_from_tuple(column_tuple, self.threshold)
        # print("load_column_names_with_set new_set", new_set)

        self.refresh_buffer(new_set)

    def setItem(self, num: int, i: int, data: list_tuple) -> None:
        buffer_key = self.buffer_key_format(num)
        df = self.buffer_data[buffer_key]
        keyname = column_name_format(i)
        df[keyname] = data
        self.buffer_data[buffer_key] = df

    def get_column(self, i: int) -> pddf:
        column = column_name_format(i)
        keyName = self.columns_tables_dict[column]
        return self.buffer_data[keyName]

    def get_cell(self, j: int, i: int) -> int_float:
        column = column_name_format(j)
        df = self.get_column(j)
        return tuple(df[column])[i]

    def get_row(self, i: int) -> tuple:
        column = column_name_format(i)
        keyName = self.columns_tables_dict[column]
        return tuple(self.buffer_data[keyName][column])

    def set_row(self, i: int, data: list_tuple) -> None:
        num = get_table_name_treshold(i, self.threshold)
        self.setItem(num, i, data)

    def final_save(self) -> None:
        # print("final save operation")
        self.save_buffer()
        self.buffer_data = {}
