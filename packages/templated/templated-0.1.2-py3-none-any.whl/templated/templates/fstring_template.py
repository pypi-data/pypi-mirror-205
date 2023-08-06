from functools import cached_property
import re
from templated.templates.base_template import BaseTemplate


class FStringTemplate(BaseTemplate):
    format = BaseTemplate.Format.FSTRING
    _template: str

    def __init__(self, template: str):
        super().__init__(template)
        self._template = template

    @cached_property
    def vars(self) -> list[str]:
        var_names = re.findall(r"{([^{}]*)}", self._template_source)
        return list(set(var_names))

    def _render(self, **kwargs) -> str:
        return self._template.format(**kwargs)
