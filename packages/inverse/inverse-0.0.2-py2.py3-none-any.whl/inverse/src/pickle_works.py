from pathlib import Path
import os
import pickle

from .inverse_typings import *

pickle_folder = "./pickles2"
pickle_folder_path = Path(pickle_folder)
if not pickle_folder_path.is_dir():
    os.makedirs(pickle_folder_path)


class Pickles:
    @staticmethod
    def name_format(key: str) -> Path:
        return pickle_folder_path / f"{key}.pickle"

    @staticmethod
    def check_pickle(key: str) -> bool:
        return Pickles.name_format(key).is_file()

    @staticmethod
    def read_pickle(key: str) -> list_tuple:
        new_data = False
        with open(Pickles.name_format(key), 'rb') as f:
            new_data = pickle.load(f)
        return new_data

    @staticmethod
    def save_pickle(key: str, data: list_tuple) -> None:
        with open(Pickles.name_format(key), 'wb') as f:
            pickle.dump(data, f)
