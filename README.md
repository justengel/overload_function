# Overload Function

This allows python to overload functions like C++. It uses function argument type annotations to do this.

## Example - Simple

```python
import overload_function


class Test(object):
    def __init__(self, x=0):
        self.x = x
        self.int_test = None
        self.bool_test = None

    @overload_function
    def set_x(self, x: int):
        self.int_test = True
        self.x = x

    @set_x.overload
    def set_x(self, x: bool):
        self.bool_test = True
        self.x = 0

t = Test()

assert t.x == 0

value = 2
t.set_x(value)
assert t.x == value
assert t.int_test

value = False
t.set_x(value)
assert t.x == 0
assert t.bool_test
```


## Example - advanced
```python
from overload_function import overload_function


class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, obj):
        try:
            return self.x == obj.x and self.y == obj.y
        except:
            return False

class Test(object):
    @overload_function
    def __init__(self, s: str="", x: int=0, b: bool=False, p: Point=Point()):
        self.s = s
        self.x = x
        self.b = b
        self.p = p

    @__init__.overload
    def __init__(self, x: int=0, b: bool=False, s: str="", p: Point=Point()):
        self.s = s
        self.x = x
        self.b = b
        self.p = p

    @__init__.overload
    def __init__(self, p: Point=Point(), x: int=0, b: bool=False, s: str=""):
        self.s = s
        self.x = x
        self.b = b
        self.p = p

t1 = Test("Hello World!", 1, True, Point(1, 1))
assert t1.s == "Hello World!"
assert t1.x == 1
assert t1.b is True
assert t1.p == Point(1, 1)

# Overload x first
t2 = Test(1, True, "Hello World!", Point(1, 1))
assert t2.s == "Hello World!"
assert t2.x == 1
assert t2.b is True
assert t2.p == Point(1, 1)

# Overload p first
t3 = Test(Point(1, 1), 1, True, "Hello World!")
assert t3.s == "Hello World!"
assert t3.x == 1
assert t3.b is True
assert t3.p == Point(1, 1)
```


## Example - function
```python
import overload_function


t1 = []
t2 = []

@overload_function
def run1(x: int=0, y: int=0):
    t1.append((x, y))

@run1.overload
def run1(x: str="1", y: str="1"):
    t2.append((int(x), int(y)))

run1(2, 2)
assert t1 == [(2, 2)]

run1("3", "3")
assert t2 == [(3, 3)]
```


## Example - custom match function
```python
import overload_function

def match_on_overloader(given_args, given_kwargs, func, spec_arg_names, spec_annotations, spec_defaults):
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
    try:
        idx = spec_arg_names.index("overloader")
        overloader_val = spec_defaults[idx]
        if overloader_val == given_kwargs["overloader"]:
            return float("inf")
    except:
        pass
    return 0
    # return overload_function.match(given_args, given_kwargs,
    #                                func, spec_arg_names, spec_annotations, spec_defaults)


class Test(object):
    @overload_function(match_func=match_on_overloader)
    def __init__(self, s:str="", x:int=0, b:bool=False, overloader:None="first"):
        self.s = s
        self.x = x
        self.b = b
        print("overloader", overloader)

    @__init__.overload
    def __init__(self, x:int=0, b:bool=False, s:str="", overloader:None="second"):
        self.s = s
        self.x = x
        self.b = b
        print("overloader", overloader)

    @__init__.overload
    def __init__(self,  b:bool=False, x:int=0, s:str="", overloader:None="third"):
        self.s = s
        self.x = x
        self.b = b
        print("overloader", overloader)


t = Test(1, 2, 3, overloader="third")
assert t.s == 3
assert t.x == 2
assert t.b == 1

t = Test(1, 2, 3, overloader="first")
assert t.s == 1
assert t.x == 2
assert t.b == 3

t = Test(1, 2, 3, overloader="second")
assert t.s == 3
assert t.x == 1
assert t.b == 2

t = Test(1, 2, 3)  # Will used the first function set (overloader=="first")
assert t.s == 1
assert t.x == 2
assert t.b == 3
```
