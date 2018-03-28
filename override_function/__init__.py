import sys
import types
from .override import override_function


class OverrideModule(types.ModuleType):
    """Custom callable module.
    This can be called by the following example.
    Example:
        ..code-block :: python
            >>> import override_function
            >>> class Example(object):
            >>>     x = 0
            >>>
            >>>     def __init__(self, x=0):
            >>>         self.x = x
            >>>
            >>>     @override_function
            >>>     def str_x(self, x:int):
            >>>         print("int argument given")
            >>>         return str(x)
            >>>
            >>>     @str_x.override
            >>>     def str_x(self, x:str):
            >>>         print("str argument given")
            >>>         return x
            >>>
            >>> ex = Example()
            >>> ex.x = 5
            >>> print(ex.str_x(ex.x), ex.str_x("123"))

    This class module is implemented so you don't have to call

    ..code-block :: python
        >>> import override_function
        >>> override_function.override_function

    """
    override_function = override_function

    def __call__(self, func):
        return self.override_function(func)


# Make this module callable
sys.modules[__name__] = OverrideModule(__name__)
