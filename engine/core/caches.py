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

import sys
import codecs

from ..base.error import Error

class TextFileError(Error):
    def __init__(self, name, file_path, memo):
        Error.__init__(self, name)
        self.file_path = file_path
        self.memo = memo

class TextFileCache(FileCache):
    _def_enc = sys.getfilesystemencoding()

    @classmethod
    def set_default_encoding(cls, enc):
        cls._def_enc = enc

    def __init__(self, key):
        FileCache.__init__(self, key)
        try:
            self.__text = self.convert_text(self.data) 
            self.__error = None
        except UnicodeDecodeError as exc:
            self.__text = ""
            self.__error = TextFileError("WRONG_ENCODING", key, str(exc))

        self.__lines = None

    @classmethod
    def convert_text(cls, data):
        if data.startswith(codecs.BOM_UTF8):
            return data[len(codecs.BOM_UTF8):].decode('utf-8')
        else:
            return data.decode(cls._def_enc)

    @property
    def path(self):
        return self.key

    @property
    def error(self):
        return self.__error

    @property
    def text(self):
        return self.__text

    @property
    def lines(self):
        if self.__lines is None:
            self.__lines = self.__text.splitlines()

        return self.__lines

        return self.__lines


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