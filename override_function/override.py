import inspect
import collections


def get_arg_type(args, kwargs, idx, varname):
    try:
        return type(kwargs[varname])
    except (KeyError, ValueError, TypeError):
        try:
            return type(args[idx])
        except (IndexError, ValueError, TypeError):
            return None


class FunctionManager(object):
    def __init__(self, func=None):
        self.funcs = []
        self.arg_spec = []

        if func is not None:
            self.override(func)

    def override(self, func):
        """override the current function for a set of specific inputs."""
        arg_spec = inspect.getfullargspec(func)
        self.funcs.append(func)
        self.arg_spec.append(arg_spec)
        return self

    def remove_override(self, func):
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
            match_points = sum([1 for j, varname in enumerate(spec.args[offset:])
                                if (spec.annotations.get(varname, None) is None or
                                    get_arg_type(args, kwargs, j, varname) == spec.annotations.get(varname, None))
                                ])
            comp.append(match_points)

        best_match = max(comp)
        return comp.index(best_match)

    def __call__(self, *args, **kwargs):
        """Compare the args and call the function that most closely matches the arguments."""
        idx = self.compare_args(*args, **kwargs)
        return self.funcs[idx](*args, **kwargs)


class override_function(FunctionManager):
    """Decorator to properly select the function manager."""

    def get_function_manager(self, instance=None):
        if instance is None:
            instance = self
        if not hasattr(instance, "__override_functions__"):
            instance.__override_functions__ = {}

        if self not in instance.__override_functions__:
            mngr = FunctionManager()

            for func in self.funcs:
                mngr.override(func.__get__(instance, instance.__class__))

            instance.__override_functions__[self] = mngr

        return instance.__override_functions__[self]

    def __get__(self, instance, owner):
        """Return the function manager to help call the correct function."""
        return self.get_function_manager(instance)
