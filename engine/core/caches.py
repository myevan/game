from ..base.pattern import Cache

class FileCache(Cache):
    def __init__(self, key):
        Cache.__init__(self, key)
        self.__data = open(key, 'rb').read()

    @property
    def path(self):
        return self.key

    @property
    def data(self):
        return self.__data


from .factories import TableFactory

class TableCache(Cache):
    def __init__(self, key):
        Cache.__init__(self, key)
        self.__table = TableFactory.get().create(path=key)

    @property
    def path(self):
        return self.key

    @property
    def table(self):
        return self.__table