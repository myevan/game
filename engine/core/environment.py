import os

from engine.base.pattern import Singleton

class Environment(Singleton):
    def __init__(self):
        this_dir_path = os.path.dirname(os.path.realpath(__file__))
        engine_dir_path = os.path.dirname(this_dir_path)
        self.__engine_dir_path = engine_dir_path
        self.__main_dir_path = ""

    def set_main_file_path(self, main_file_path):
        self.__main_dir_path = os.path.dirname(os.path.realpath(main_file_path))

    @property
    def engine_dir_path(self):
        return self.__engine_dir_path

    @property
    def main_dir_path(self):
        return self.__main_dir_path
