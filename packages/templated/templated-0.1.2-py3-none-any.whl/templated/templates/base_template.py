from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from functools import cache, cached_property
import re

import jinja2


class BaseTemplate(ABC):
    class Format(Enum):
        JINJA2 = "Jinja2"
        FSTRING = "f-string"

    format = None

    _template_source: str
    _template: str

    def __init__(self, template: str):
        self._template_source = template

    @abstractmethod
    def _render(self, **kwargs) -> str:
        pass

    @property
    @abstractmethod
    def vars(self) -> list[str]:
        pass

    @classmethod
    def create_template(
        cls, template: str | jinja2.Template, format: BaseTemplate.Format = None
    ):
        """
        Creates a Template object. Determines the format of the template automatically (or manually if specified)

        Args:
            template (str | jinja2.Template): The template to use for the object.
            format (Template.Format, optional): The format of the template. Defaults to None.

        Example:
            >>> print("This is an example")
            This is an example
            >>> from templated import Template
            >>> t = Template("Hello, {{name}}!")
            >>> print(t.render(name="world"))
            Hello, world!
        """
        from templated.templates.fstring_template import FStringTemplate
        from templated.templates.jinja_template import JinjaTemplate

        # override format if specified
        if format is BaseTemplate.Format.JINJA2:
            return JinjaTemplate(template)
        elif format is BaseTemplate.Format.FSTRING:
            return FStringTemplate(template)
        # must test double braces before single braces
        elif isinstance(template, str) and re.search(r"{{.*?}}", template):
            return JinjaTemplate(template)
        elif isinstance(template, str) and re.match(r"{.*?}", template):
            return FStringTemplate(template)
        # If Jinja2 template, then its obviously a Jinja2 template
        elif isinstance(template, jinja2.Template):
            return JinjaTemplate(template)
        # if no braces, default to fstring
        elif isinstance(template, str):
            return FStringTemplate(template)
        else:
            raise ValueError(
                f"Invalid template format for {template}. Must be either an fstring or a Jinja2.Template or a Jinja2.Template string"
            )

    def render(self, **kwargs) -> str:
        return self._render(**kwargs)
