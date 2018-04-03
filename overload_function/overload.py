import inspect
import collections


__all__ = ['overload_function', 'get_arg_type', 'match']


def get_arg_type(args, kwargs, idx, varname):
    try:
        return type(kwargs[varname])
    except (KeyError, ValueError, TypeError):
        try:
            return type(args[idx])
        except (IndexError, ValueError, TypeError):
            return None


def match(given_args, given_kwargs, func, spec_arg_names, spec_annotations, spec_defaults):
    """Compare arguments and return a weight for how much you want to use this function.

    Args:
        given_args (tuple): Arguments given to the function call.
        given_kwargs (dict): Keyword arguments given to the function call.
        func (function): Function that you are checking arguments for
        spec_arg_names (list): List of argument names in order found with inspect.getfullargspec.
        spec_annotations (dict): Dictionary of spec argument names and type annotations to try and match.
        spec_defaults (tuple): Default values that match the spec_arg_names.

    Returns:
        weight (int): Integer that dictates how likely this function is to be the correct function. The highest
            number will be used in deciding which function should be called.
    """
    weight = sum([1 for j, varname in enumerate(spec_arg_names)
                  if (spec_annotations.get(varname, None) is None or
                      get_arg_type(given_args, given_kwargs, j, varname) == spec_annotations.get(varname, None))
                  ])
    return weight


class FunctionManager(object):

    match = staticmethod(match)

    def __init__(self, func=None, match_func=None):
        self.match_func = match_func
        self.funcs = []
        self.arg_spec = []

        # Set match as the default match function
        if self.match_func is None:
            self.match_func = self.match

        if func is not None:
            self.overload(func)

    def set_match_func(self, match_func):
        self.match_func = match_func
        return self

    def overload(self, func):
        """overload the current function for a set of specific inputs."""
        arg_spec = inspect.getfullargspec(func)
        self.funcs.append(func)
        self.arg_spec.append(arg_spec)
        return self

    def remove_overload(self, func):
        try:
            idx = self.funcs.index(func)
            self.funcs.pop(idx)
            self.arg_spec.pop(idx)
        except:
            pass
        return self

    def compare_args(self, *args, **kwargs):
        """Compare the arguments with each functions full argument spec and return the index of the function that
        matches the arguments best.
        """

        comp = []
        for i in range(len(self.arg_spec)):
            func = self.funcs[i]
            spec = self.arg_spec[i]
            offset = 0
            if (hasattr(func, "__self__") and func.__self__ is not None and
                    len(spec.args) > 0 and spec.args[0] == "self"):
                offset = 1
            weight = self.match_func(args, kwargs, func, spec.args[offset:], spec.annotations, spec.defaults)
            comp.append(weight)

        best_match = max(comp)
        return comp.index(best_match)

    def __call__(self, *args, **kwargs):
        """Compare the args and call the function that most closely matches the arguments."""
        if len(self.funcs) == 0 and len(args) > 0 and callable(args[0]):
            # Class was created with a match_func and no function. overload the given function
            self.overload(args[0])
            return self

        else:
            idx = self.compare_args(*args, **kwargs)
            return self.funcs[idx](*args, **kwargs)


class overload_function(FunctionManager):
    """Decorator to properly select the function manager."""

    def get_function_manager(self, instance=None):
        if instance is None:
            instance = self
        if not hasattr(instance, "__overload_functions__"):
            instance.__overload_functions__ = {}

        if self not in instance.__overload_functions__:
            mngr = FunctionManager(match_func=self.match_func)

            for func in self.funcs:
                mngr.overload(func.__get__(instance, instance.__class__))

            instance.__overload_functions__[self] = mngr

        return instance.__overload_functions__[self]

    def __get__(self, instance, owner):
        """Return the function manager to help call the correct function."""
        return self.get_function_manager(instance)
