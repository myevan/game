from ..base.pattern import Cache

class FileCache(Cache):
    def __init__(self, key):
        Cache.__init__(self, key)
        self.__data = open(key, 'rb').read()

    def get_path(self):
        return self.get_key()

    def get_data(self):
        return self.__data


from .factories import TableFactory

class TableCache(Cache):
    def __init__(self, key):
        Cache.__init__(self, key)
        self.__table = TableFactory.get().create(path=key)

    def get_path(self):
        return self.get_key()

    def get_table(self):
        return self.__table