from __future__ import annotations

from enum import Enum
from functools import cache, cached_property
import re
from typing import Literal
from exports import export
import jinja2


@export
class Template:
    class Format(Enum):
        JINJA2 = "Jinja2"
        FSTRING = "f-string"

    _template_source: str
    _template: str | jinja2.Template

    def __init__(self, template: str | jinja2.Template, format: Template.Format = None):
        """
        Initializes a Template object.

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
        if isinstance(template, Template):
            self.__dict__ = template.__dict__
            return

        self._template_source = template

        # override format if specified
        if format is not None:
            self.format = format
        # must test double braces before single braces
        elif re.search(r"{{.*?}}", template):
            self.format = Template.Format.JINJA2
        elif re.match(r"{.*?}", template):
            self.format = Template.Format.FSTRING
        # if no braces, default to fstring
        else:
            self.format = Template.Format.FSTRING
            # raise ValueError(f"Invalid template format: {self}. Must be either an fstring or a Jinja2.Template")

        match self.format:
            case Template.Format.JINJA2:
                self._template = jinja2.Template(template)
            case Template.Format.FSTRING:
                self._template = template
            case _:
                raise ValueError(f"Invalid template format: {self.format}")

    @cached_property
    def vars(self) -> list[str]:
        """
        Gets the variables used in a template string.

        Returns:
            list[str]: A list of variable names used in the template.

        Raises:
            ValueError: If the format of the template is invalid.

        Example:
            >>> from templated import Template
            >>> t = Template("Hello, {{name}}!")
            >>> print(t.vars)
            ['name']
        """
        match self.format:
            case Template.Format.JINJA2:
                var_names = re.findall(r"{{([^{}]+)}}", self._template_source)
            case Template.Format.FSTRING:
                var_names = re.findall(r"{([^{}]*)}", self._template_source)
            case _:
                raise ValueError(
                    f"Invalid template format: {self.format}. Must be either an fstring or a Jinja2.Template"
                )

        # Remove duplicates and return variable names
        return list(set(var_names))

    @cache
    def render(self, **kwargs) -> str:
        """
        Renders the template with the specified keyword arguments.

        Args:
            **kwargs: The keyword arguments to use for rendering the template.

        Returns:
            str: The rendered template string.

        Raises:
            ValueError: If the format of the template is invalid.

        Example:
            >>> from templated import Template
            >>> t = Template("Hello, {{name}}!")
            >>> print(t.render(name="world"))
            Hello, world!
        """
        match self.format:
            case Template.Format.JINJA2:
                return self._template.render(**kwargs)
            case Template.Format.FSTRING:
                return self._template.format(**kwargs)
            case _:
                raise ValueError(
                    f"Invalid template format: {self.format}. Must be either an fstring or a Jinja2.Template"
                )
