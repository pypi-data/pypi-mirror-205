from functools import cached_property
import re
import jinja2
from jinja2 import Environment, meta
from templated.templates.base_template import BaseTemplate


class JinjaTemplate(BaseTemplate):
    format = BaseTemplate.Format.JINJA2
    _template: jinja2.Template

    def __init__(self, template: str):
        super().__init__(template)
        self._template = jinja2.Template(template)

    @cached_property
    def vars(self) -> list[str]:
        env = Environment()  # You can pass any other options to the environment
        parsed_content = env.parse(self._template_source)
        variables = meta.find_undeclared_variables(parsed_content)
        return list(set(variables))

    def _render(self, **kwargs) -> str:
        return self._template.render(**kwargs)
