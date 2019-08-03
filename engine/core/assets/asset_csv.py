import os
import csv
import glob
import codecs
import sys

from io import StringIO

from ...base.error import Error
from ...base.data import Table, Record
from ..caches import TextFileCache

class CSVError(Error):
    def __init__(self, name, path, *args):
        Error.__init__(self, name)
        self.path = path
        self.ctx = args

    def __str__(self):
        return f"{self.__class__.__name__}<{self.name}>{self.ctx}: {self.path}"

class CSVRecord(Record):
    pass

class CSVData(Table):
    @classmethod
    def find_line_index(cls, file_path, record):
        temp = StringIO()
        csv.writer(temp).writerow(record.fields)
        finding_line = temp.getvalue().splitlines()[0]

        cache = TextFileCache.get(file_path)
        for idx, line in enumerate(cache.lines):
            if line == finding_line:
                return idx

        return -1

    def __init__(self, file_text, file_path='', **kwargs):
        reader = csv.reader(StringIO(file_text))
        name = os.path.splitext(os.path.basename(file_path))[0]

        try:
            heads = [head.strip() for head in next(reader)]
        except StopIteration:
            raise CSVError("NO_HEADS", file_path)

        records = [CSVRecord(record, table=self, row=row) for row, record in enumerate(reader)
            if len(record) > 0 and (record[0] or any(record))]

        Table.__init__(self, name, heads, records, **kwargs)
        self.path = file_path

class CSVFile(CSVData):
    def __init__(self, file_path, *args, **kwargs):
        cache = TextFileCache.get(file_path)
        CSVData.__init__(self, cache.text, file_path, **kwargs)

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
    csv_data = CSVData("id,name\n1,a\n2,b\n")
    print(csv_data)
    print(csv_data.records)