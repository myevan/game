#pragma once

#include <stdint.h>
{% for scheme in schemes %}
class {{ scheme.name }}
{
public:
    {% for field in scheme.fields %}{{ field.c_type_ret }} Get{{ field.pascal_name }}() const;
    {% endfor %} 
private:
    {% for field in scheme.fields %}{{ field.c_type_decl }} m_{{ field.c_type_prefix }}{{ field.pascal_name }}{{ field.c_type_array }};
    {% endfor %} 
};
{% endfor %}