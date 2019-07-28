import os

from ..base.pattern import Singleton, Factory

class TableFactory(Singleton, Factory):
    def __init__(self):
        Singleton.__init__(self)
        Factory.__init__(self)
        self.create_dir = None

    def register_file(self, ext, create_file):
        Factory.register(self, ext, create_file)

    def register_directory(self, create_dir):
        self.create_dir = create_dir

    def create(self, path):
        if os.path.isdir(path):
            return self.create_dir(path)
        else:
            ext = os.path.splitext(path)[1]
            return Factory.create(self, ext, path)
