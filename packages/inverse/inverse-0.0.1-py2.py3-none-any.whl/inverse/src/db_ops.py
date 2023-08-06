#   Sermet.Pekin 2023
#   matrix ops
#   bkz README.md.
import math
import shutil
from pathlib import Path
import pandas as pd
import sqlite3
from dataclasses import dataclass
from .partition import get_name_from_i, get_table_name_treshold
from .inverse_typings import *

import os


@dataclass
class APP_SQL:
    SQL_DOMAIN = "db"
    DB_NAME = "test_big_matrix.db"
    DB_NAME_TEMP = "test_big_matrix-TEMP.db"
    DB_NAME_Backup = "test_big_matrix-Backup.db"

    def __init__(self):

        self.create_folder()

    def create_folder(self):
        db_folder = Path() / APP_SQL.SQL_DOMAIN
        if not db_folder.is_dir():
            os.makedirs(db_folder)

    def paste(self, *args, sep="/"):
        return sep.join(args)

    def firstly_backup_db(self) -> None:
        file_name_source = Path() / APP_SQL.SQL_DOMAIN / APP_SQL.DB_NAME
        file_name_dest = Path() / APP_SQL.SQL_DOMAIN / APP_SQL.DB_NAME_Backup
        try:
            shutil.copy(file_name_source, file_name_dest)
        except:
            print("Backup failed")
            raise NotImplementedError

    def finally_rename(self, test: bool) -> None:
        file_name_source = Path() / APP_SQL.SQL_DOMAIN / APP_SQL.DB_NAME_TEMP
        file_name_dest = Path() / APP_SQL.SQL_DOMAIN / APP_SQL.DB_NAME
        try:
            if not test:
                shutil.copy(file_name_source, file_name_dest)
            else:
                print("TESTING ", file_name_source, file_name_dest)
        except Exception as exc:
            print(exc)

    def get_conn(self) -> sqlite3.Connection:
        s = self.paste(APP_SQL.SQL_DOMAIN, APP_SQL.DB_NAME)
        conn = sqlite3.connect(s)
        return conn

    def add_table(self, name: str, df: pddf) -> None:
        with self.get_conn() as conn:
            df.to_sql(name, conn, if_exists='replace')

    def read_table(self, name: str) -> pddf:
        with self.get_conn() as conn:
            result = pd.read_sql(f'SELECT * FROM {name}', conn)
        return result

    def get_table_names(self) -> tuple:
        with self.get_conn() as conn:
            sql_query = f"""SELECT name FROM sqlite_master
              WHERE type='table';"""
            cursor = conn.cursor()
            cursor.execute(sql_query)
            names = cursor.fetchall()
        return tuple(map(lambda x: x[0], names))

    def extract_elements(self, element):
        return element[0]


app_sql = APP_SQL()


class DB_class_Opt(Protocol):
    @staticmethod
    def read_db(name: str) -> pddf:
        df = app_sql.read_table(name)
        return df

    @staticmethod
    def write_db(name: str, df: pddf) -> None:
        if "level_0" in tuple(df.columns):
            df = df.drop(['level_0'], axis=1)
        app_sql.add_table(name, df)

    @staticmethod
    def merge(df, columns, buffer):
        new_df = df
        for column in columns:
            new_df[column] = buffer[column]
        return new_df

    @staticmethod
    def update_db(keys, buffer):
        ...


class DB_class(Protocol):
    """ Birden fazla satır tek bir tablo olarak kaydedilecek"""

    @staticmethod
    def update_df(name, buffer):
        ...

    @staticmethod
    def read_db(name):
        df = app_sql.read_table(name)
        return tuple(df["0"])

    @staticmethod
    def write_db(name, data):
        df = pd.DataFrame(data)
        app_sql.add_table(name, df)


def add_db_quick(name, df):
    app_sql.add_table(name, df)


def firstly_backup_db():
    app_sql.firstly_backup_db()


def finally_rename_db_file(test):
    app_sql.finally_rename(test)


def notest_sql():
    app_sql = APP_SQL()
    # df = pd.DataFrame({'id': [100, 101, 102, 103], 'name': ['Tom', 'Jerry', 'Sooty', 'Sweep']})
    # app_sql.add_table("name", df)
    # df2 = app_sql.read_table("name")
    # print(df2)
    # names = app_sql.get_table_names()
    # print(names)
    #
    # write_db("test1", (8, 2, 3, 4))
    # gelen = read_db("test1")
    # print(gelen)
    #
    # names = app_sql.get_table_names()
    # print(names)
# notest_sql()
# print(type(names))
# names = tuple(map(lambda x: x[0], names))
