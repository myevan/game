#include "{{out_name}}.h"
{% for scheme in schemes %}{% for field in scheme.fields %}
{{ field.c_type_ret }} 
{{ scheme.name }}::Get{{ field.name }}() const
{
    return m_{{ field.c_type_prefix }}{{ field.name }};
}
{% endfor %} 
{% endfor %} 