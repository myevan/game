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

    def zips(self, cls):
        return [zip(self.__heads, record) for record in self.__records]

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

class Field:
    def __init__(self, value, record=None, col=None):
        self.__value = value
        self.__record = record
        self.__col = col

    def __repr__(self):
        tail = f":{self.__record.src.table.name}:{self.notation}" if self.__record and self.__record.src else ''
        return f"{self.__class__.__name__}({self.__value}){tail}"

    @property
    def value(self):
        return self.__value

    @property
    def record(self):
        return self.__record

    @property
    def col(self):
        return self.__col

    @property
    def notation(self):
        dst_heads = self.__record.table.scheme.field_names
        src_heads = self.__record.src.table.heads
        dst_head = dst_heads[self.__col]
        src_head = src_heads[self.__col]
        if dst_head == src_head:
            col = self.__col
        else:
            col = src_heads.index(dst_head)

        col += 1

        prefix = ''
        while col:
            remain = col % 26
            if remain == 0:
                remain = 26

            prefix = chr(ord('A') + remain - 1) + prefix
            col = int((col - 1) / 26)

        row = self.__record.src.row + 1 + 1 # excel base(1) + head(1)
        return f"${prefix}{row}"

class Record:
    def __init__(self, fields, table=None, row=None, src=None):
        self.__fields = fields
        self.__table = table
        self.__row = row 
        self.__src = src

    def __repr__(self):
        src = self.__src
        tail = f":{src.table.name}:{src.notation}" if src else ''
        return f"{self.__class__.__name__}({list(zip(self.__table.heads, self.__fields))}){tail}"

    def bind_table(self, table, row):
        self.__table = table
        self.__row = row

    def bind_source(self, src):
        self.__src = src

    def get_field(self, col):
        return Field(self.__fields[col], self, col)

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

    @property
    def notation(self):
        return f"${self.__row + 1 + 1}" # excel base(1) + head(1)

class Relation:
    def __init__(self, src_keys, dst_keys, src_cond="", dst_cond=""):
        self.__src_keys = src_keys
        self.__dst_keys = dst_keys
        self.__src_cond = src_cond
        self.__dst_cond = dst_cond

    @property
    def src_key(self):
        return self.__src_keys[0]

    @property
    def dst_key(self):
        return self.__dst_keys[0]

    @property
    def src_keys(self):
        return self.__src_keys

    @property
    def dst_keys(self):
        return self.__dst_keys

    @property
    def src_cond(self):
        return self.__src_cond

    @property
    def dst_cond(self):
        return self.__dst_cond

class RelationManager:
    def load(self, relations):
        self._relations = relations

    @property
    def relations(self):
        return self._relations

if __name__ == '__main__':
    scheme = Scheme('Example', ['id', 'name'], [int, str])
    print(scheme)

    table = Table('Example', ['id', 'name'], [Record([1, 'a']), Record([2, 'b'])])
    print(table)
    print(table.records)