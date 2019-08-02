import xlrd
import os

from ...base.data import Table, Record

class XLRecord(Record):
    pass

class XLFile(Table):
    def __init__(self, file_path, *args, **kwargs):
        def gen_records(sheet):
            for row in range(1, sheet.nrows):
                values = [sheet.cell_value(row, col) for col in range(sheet.ncols)]
                if len(values) > 0 and (values[0] or any(values)):
                    yield XLRecord(values, table=self, row=row)

        name = os.path.splitext(os.path.basename(file_path))[0]

        book = xlrd.open_workbook(file_path)
        sheet = book.sheets()[0]
        heads = [sheet.cell_value(0, col) for col in range(sheet.ncols)]

        Table.__init__(self, name, heads, records=list(gen_records(sheet)), **kwargs)
        self.path = file_path
