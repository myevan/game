import os
import csv
import glob
import codecs
import sys

from io import StringIO

from ...base.error import Error
from ...base.data import Table, Record

class CSVError(Error):
    def __init__(self, name, path, *args):
        Error.__init__(self, name)
        self.path = path
        self.args = args

    def __str__(self):
        return f"{self.__class__.__name__}<{self.name}>{self.args}: {self.path}"

class CSVCellError(CSVError):
    def __init__(self, name, path, row, col, value, memo):
        CSVError.__init__(self, name, path)
        self.row = row
        self.col = col
        self.value = value
        self.memo = memo

    def __str__(self):
        return f"{self.__class__.__name__}<{self.name}>([{self.row}][{self.col}]='{self.value}', '{self.memo}'):{self.path}"

class CSVRecord(Record):
    pass

class CSVData(Table):
    __def_enc = sys.getfilesystemencoding()

    @classmethod
    def set_default_encoding(cls, enc):
        cls.__def_enc = enc

    def __init__(self, file_data, file_path='', **kwargs):
        if file_data.startswith(codecs.BOM_UTF8):
            file_text = file_data[len(codecs.BOM_UTF8):].decode('utf-8')
        else:
            file_text  = file_data.decode(self.__def_enc)

        reader = csv.reader(StringIO(file_text))
        name = os.path.splitext(os.path.basename(file_path))[0]

        try:
            heads = next(reader)
        except StopIteration:
            raise CSVError("NO_HEADS", file_path)

        records = [CSVRecord(record, table=self, row=row) for row, record in enumerate(reader)
            if len(record) > 0 and (record[0] or any(record))]

        Table.__init__(self, name, heads, records, **kwargs)
        self.path = file_path

class CSVFile(CSVData):
    def __init__(self, file_path, *args, **kwargs):
        file_data = open(file_path, 'rb').read()
        CSVData.__init__(self, file_data, file_path, **kwargs)

class CSVDirectory(Table):
    def __init__(self, dir_path):
        csv_files = [CSVFile(file_path) for file_path in sorted(glob.glob(os.path.join(dir_path, '*.csv')))]
        Table.__init__(self, os.path.basename(dir_path), csv_files[0].heads, self.__gen_records(csv_files))
        self.path = dir_path
        self.csv_files = csv_files

    @classmethod
    def __gen_records(cls, csv_files):
        for csv_file in csv_files:
            for csv_record in csv_file.records:
                yield csv_record

from ..factories import TableFactory
TableFactory.get().register_directory(CSVDirectory)
TableFactory.get().register_file('.csv', CSVFile)

if __name__ == '__main__':
    csv_data = CSVData(b"id,name\n1,a\n2,b\n")
    print(csv_data)
    print(csv_data.records)