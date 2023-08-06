import sys
from types import ModuleType

from templated.function import Function
from templated.templates.__old_template import Template


class Templated(ModuleType):
    def __call__(self, *args, **kwargs):
        return Function(*args, **kwargs)


sys.modules[__name__].__class__ = Templated


__all__ = ["Function", "Template", "__call__"]
