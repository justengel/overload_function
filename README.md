# Override Function

This allows python to override functions like C++. It uses function argument type annotations to do this.

## Example - Simple

```python
import override_function


class Test(object):
    def __init__(self, x=0):
        self.x = x
        self.int_test = None
        self.bool_test = None

    @override_function
    def set_x(self, x: int):
        self.int_test = True
        self.x = x

    @set_x.override
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
from override_function import override_function


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
    @override_function
    def __init__(self, s: str="", x: int=0, b: bool=False, p: Point=Point()):
        self.s = s
        self.x = x
        self.b = b
        self.p = p

    @__init__.override
    def __init__(self, x: int=0, b: bool=False, s: str="", p: Point=Point()):
        self.s = s
        self.x = x
        self.b = b
        self.p = p

    @__init__.override
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

# Override x first
t2 = Test(1, True, "Hello World!", Point(1, 1))
assert t2.s == "Hello World!"
assert t2.x == 1
assert t2.b is True
assert t2.p == Point(1, 1)

# Override p first
t3 = Test(Point(1, 1), 1, True, "Hello World!")
assert t3.s == "Hello World!"
assert t3.x == 1
assert t3.b is True
assert t3.p == Point(1, 1)
```


## Example - function
```python
import override_function


t1 = []
t2 = []

@override_function
def run1(x: int=0, y: int=0):
    t1.append((x, y))

@run1.override
def run1(x: str="1", y: str="1"):
    t2.append((int(x), int(y)))

run1(2, 2)
assert t1 == [(2, 2)]

run1("3", "3")
assert t2 == [(3, 3)]
```
