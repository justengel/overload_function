import sys
import types
from .overload import overload_function, get_arg_type, match


class OverloadModule(types.ModuleType):
    """Custom callable module.
    This can be called by the following example.
    Example:
        ..code-block :: python
            >>> import overload_function
            >>> class Example(object):
            >>>     x = 0
            >>>
            >>>     def __init__(self, x=0):
            >>>         self.x = x
            >>>
            >>>     @overload_function
            >>>     def str_x(self, x:int):
            >>>         print("int argument given")
            >>>         return str(x)
            >>>
            >>>     @str_x.overload
            >>>     def str_x(self, x:str):
            >>>         print("str argument given")
            >>>         return x
            >>>
            >>> ex = Example()
            >>> ex.x = 5
            >>> print(ex.str_x(ex.x), ex.str_x("123"))

    This class module is implemented so you don't have to call

    ..code-block :: python
        >>> import overload_function
        >>> overload_function.overload_function

    """
    overload_function = overload_function

    def __call__(self, *args, **kwargs):
        return self.overload_function(*args, **kwargs)


# Make this module callable
sys.modules[__name__] = OverloadModule(__name__)
