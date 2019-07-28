from jinja2 import Template

from ...base.data import Scheme
from ...core.caches import FileCache

class FieldWarpper:
    PREFIX_TO_C_TYPES = {
        'i8': 'int8_t',
        'i16': 'int16_t',
        'i32': 'int32_t',
        'i64': 'int64_t',
        'u8': 'uint8_t',
        'u16': 'uint16_t',
        'u32': 'uint32_t',
        'u64': 'uint64_t',
        'f32': 'float',
        'sz': 'char',
    }

    def __init__(self, scheme, idx):
        self.name = scheme.field_names[idx]
        self.type = scheme.field_types[idx]

    @property
    def pascal_name(self):
        return ''.join(token[0].upper() + token[1:] for token in self.name.split('_'))

    @property
    def c_type_ret(self):
        c_type = self.PREFIX_TO_C_TYPES[self.type.prefix]
        return f"const {c_type}*" if self.type.prefix == 'sz' else c_type

    @property
    def c_type_decl(self):
        c_type = self.PREFIX_TO_C_TYPES[self.type.prefix]
        return c_type

    @property
    def c_type_array(self):
        return f"[{self.type.count}]" if self.type.count else ""

    @property
    def c_type_prefix(self):
        return self.type.prefix

class SchemeWrapper:
    def __init__(self, scheme):
        self.name = scheme.name
        self.flags = '|'.join(scheme.flags)
        self.fields = [FieldWarpper(scheme, index) for index in range(len(scheme.field_names))]

class Application:
    def run(self, schemes, template_path, dst_scheme_path):
        dst_name = os.path.splitext(os.path.basename(dst_scheme_path))[0]

        template_cache = FileCache.get(template_path)
        template = Template(template_cache.get_data().decode('utf-8'))
        out_text = template.render(
            schemes=[SchemeWrapper(scheme) for scheme in schemes], 
            out_name=dst_name)

        open(dst_scheme_path, 'wb').write(out_text.encode('utf-8'))

    def gen_py_schemes(self, src_scheme_path):
        import engine
        ns = dict(engine=engine)
        exec(open(src_scheme_path).read(), ns)
        bases = [value for key, value in ns.items() 
            if type(value) is engine.core.data.DeclMeta and value != engine.protocol.Base]

        for base in bases:
            yield Scheme(base.__name__, base.get_field_names(), base.get_field_types())

if __name__ == '__main__':
    import click
    import os

    package_dir_path = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    template_dir_path = os.path.join(package_dir_path, 'templates')

    @click.command()
    @click.option('--dst-template-path', type=str, default=os.path.join(template_dir_path, 'template.h'))
    @click.option('--dst-scheme-path', type=str, default='examples/scheme.h')
    @click.option('--src-scheme-path', type=str, default='examples/scheme.py')
    def run(dst_template_path, dst_scheme_path, src_scheme_path):
        app = Application()
        schemes = list(app.gen_py_schemes(src_scheme_path))
        app.run(schemes, dst_template_path, dst_scheme_path)

    run()