class Scheme:
    def __init__(self, name, field_names, field_types, pk_names=[], flags=[]):
        self.__name = name
        self.__field_names = field_names
        self.__field_types = field_types
        self.__pk_names = pk_names
        self.__flags = flags

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.__name}>({', '.join(f'{key}={value}' for key, value in zip(self.__field_names, self.__field_types))})"

    @property
    def name(self):
        return self.__name

    @property
    def field_names(self):
        return self.__field_names

    @property
    def field_types(self):
        return self.__field_types

    @property
    def pk_names(self):
        return self.__pk_names

    @property
    def flags(self):
        return self.__flags

    def get_key_indices(self, key_names):
        return [self.__field_names.index(key_name) for key_name in key_names]

    def filter_field_indices(self, total_names):
        return [total_names.index(field_name) for field_name in self.__field_names]

class Table:
    def __init__(self, name, heads, records, scheme=None):
        self.__name = name
        self.__heads = heads
        self.__records = records
        self.__scheme = scheme

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.__name}>({','.join(self.__heads)})"

    def bind(self, scheme):
        self.__scheme = scheme

    @property
    def name(self):
        return self.__name

    @property
    def heads(self):
        return self.__heads

    @property
    def records(self):
        return self.__records

    @property
    def scheme(self):
        return self.__scheme

class Record:
    def __init__(self, fields, table=None, row=None, src=None):
        self.__fields = fields
        self.__table = table
        self.__row = row 
        self.__src = src

    def __repr__(self):
        tail = f":{self.__src.__table.name}:{self.__src.row}" if self.__src else ''
        return f"{self.__class__.__name__}({self.__fields}){tail}"

    def bind_table(self, table, row):
        self.__table = table
        self.__row = row

    def bind_source(self, src):
        self.__src = src

    @property
    def fields(self):
        return self.__fields

    @property
    def table(self):
        return self.__table

    @property
    def row(self):
        return self.__row

    @property
    def src(self):
        return self.__src

if __name__ == '__main__':
    scheme = Scheme('Example', ['id', 'name'], [int, str])
    print(scheme)

    table = Table('Example', ['id', 'name'], [Record([1, 'a']), Record([2, 'b'])])
    print(table)
    print(table.records)