class: center, middle

# Visitor Pattern in Python

## Separating behaviour from data

### A Practical Guide with Multiple Implementation Strategies

<!--???

Welcome everyone.
Today we will learn how the Visitor pattern solves a common design problem in Python.
We will look at a trivial example and explore several Python‑idiomatic ways to solve the same problem, including the Visitor pattern itself.

-->

---

# What is the Visitor Pattern?

## Definition

The Visitor pattern lets you add operations to a class hierarchy without changing the classes themselves.

You *visit* objects, and the visitor decides what to do.

## Why?

When you have a set of unrelated operations that need to work on many types, you avoid scattering `if/elif` checks or modifying each type.

This pattern decouples *data structures* from *behaviors*.

---

# The Problem - Shapes

.columns[
.column[
```py
class Circle:
    def __init__(self, radius: float):
        self.radius = radius

class Square:
    def __init__(self, side: float):
        self.side = side

class Triangle:
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c
```
]
.column[
We have a collection of shape objects and we want to perform several unrelated operations on them:

- Compute the area
- Compute the perimeter
- Render the shape
]
]

---

# Naive Approach: Methods Inside Shapes

.columns[
.column[
```py
class Circle:
    ...
    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Square:
    ...
    def area(self):
        return self.side ** 2

    def perimeter(self):
        return 4 * self.side

class Triangle:
    ...
    def area(self):
        p = (self.a + self.b + self.c) / 2
        return (p * (p-self.a) * (p-self.b) * (p-self.c)) ** 0.5

    def perimeter(self):
        return self.a + self.b + self.c
```
]
.column[
## Why is this a problem?

- Adding a new shape requires adding new code to every operation.
- Adding a new operation requires modifying every shape class.
- Violates the **Open Close Principle**
  - Classes are **open** for extension but **closed** for modifications.
]
]

<!--???

- Each shape knows how to compute its own metrics.
- Easy for small projects, but bloats the classes.
- Adding a new operation (e.g., render) forces changes in all classes.
-->

---

# Alternative 1: Classic `isinstance` Conditionals

.columns[
.column[
```python
def area(shape):
    if isinstance(shape, Circle):
        return 3.14159 * shape.radius ** 2

    if isinstance(shape, Square):
        return shape.side ** 2

    if isinstance(shape, Triangle):
        p = (shape.a + shape.b + shape.c) / 2
        return (p * (p-shape.a) * (p-shape.b) * (p-shape.c)) ** 0.5
```
]
.column[
## Pros
- *Universally supported*; works on any Python version.
- Very straightforward; no imports required.
- No external libraries or advanced features.

## Cons
- **Scattering**: Each operation must implement its own chain of `isinstance` checks.
- **Duplication**: Common patterns copy‑pasted across functions.
- **Harder to extend**: Adding a new shape means editing *every* operation.
]
]

<!--???

- The most straightforward but least extensible.
- Every new operation requires rewriting the conditional chain.
- Shows the motivation for a more scalable solution.
-->

---

# Alternative 2: `typing.overload`

.columns[
.column[
```python
import typing

@typing.overload
def area(shape: Circle) -> float: ...

@typing.overload
def area(shape: Square) -> float: ...

@typing.overload
def area(shape: Triangle) -> float: ...

def area(shape):
    if isinstance(shape, Circle):
        return 3.14159 * shape.radius ** 2

    if isinstance(shape, Square):
        return shape.side ** 2

    if isinstance(shape, Triangle):
        p = (shape.a + shape.b + shape.c) / 2
        return (p * (p-shape.a) * (p-shape.b) * (p-shape.c)) ** 0.5
```
]
.column[
## Pros
- Gives static type checkers precise signatures.
- Keeps a single implementation; no boilerplate visitor classes.
- Works well with `mypy` or IDE autocompletion.

## Cons
- Runtime dispatch still needs `isinstance` checks.
- No automatic registration; you must write the dispatch logic manually.
- Less explicit than Visitor or singledispatch.
]
]

<!--???

- `@overload` only affects type checking; the implementation remains a single function.
- Good for IDE hints but still requires `isinstance` checks.
- Adding a new shape requires updating the overload list **and** the conditional block.
-->

---

# Alternative 3: `functools.singledispatch`

.columns[
.column[
```python
import functools

@functools.singledispatch
def area(shape):
    raise NotImplementedError(f"area not implemented for {type(shape)}")

@area.register
def _(shape: Circle):
    return 3.14159 * shape.radius ** 2

@area.register
def _(shape: Square):
    return shape.side ** 2

@area.register
def _(shape: Triangle):
    p = (shape.a + shape.b + shape.c) / 2
    return (p * (p-shape.a) * (p-shape.b) * (p-shape.c)) ** 0.5
```
]
.column[
## Pros
- *Simple syntax* for a small number of operations.
- Keeps **operation logic** separate from shapes.
- Extensible: register new types without modifying shapes.

## Cons
- Only supports *single* dispatch; not suitable for multi‑argument dispatch.
- Requires all operations to be **functions**; shape classes cannot be extended to add new operations.
- Poor IDE support for type checking in older Python versions.
]
]

<!--???

- `singledispatch` dispatches based on the *first* argument’s type.
- New shapes: just add a new `@area.register`.
- New operations: create a new function (`perimeter`) with its own dispatch.
-->

---

# Alternative 4: Combining `singledispatch` and `overload`

.columns[
.column[
```python
@functools.singledispatch
def area(shape):
    raise NotImplementedError(f"area not implemented for {type(shape)}")

@area.register
def _(shape: Circle):
    return 3.14159 * shape.radius ** 2

@area.register
def _(shape: Square):
    return shape.side ** 2

@area.register
def _(shape: Triangle):
    p = (shape.a + shape.b + shape.c) / 2
    return (p * (p-shape.a) * (p-shape.b) * (p-shape.c)) ** 0.5
```
]
.column[
```py
# Type hints for static analysis
@typing.overload
def area(shape: Circle) -> float: ...

@typing.overload
def area(shape: Square) -> float: ...

@typing.overload
def area(shape: Triangle) -> float: ...
```
]
]

<!--???

- `singledispatch` supplies runtime dispatch, while `overload` supplies static type checking.
- Keeps both runtime and static concerns clean.
- Still requires separate functions for each operation.
- 
-->

---

# Alternative 5: Structural Typing with Pattern Matching

.columns[
.column[
```python
def area(shape):
    match shape:
        case Circle(radius=r):
            return 3.14159 * r ** 2

        case Square(side=s):
            return s ** 2

        case Triangle(a=a, b=b, c=c):
            p = (a + b + c) / 2
            return (p * (p-a) * (p-b) * (p-c)) ** 0.5
```
]
.column[
## Pros
- Very readable; looks like a `switch` on object shape.
- No duplication of type checks.
- Can pattern‑match on *tuples* or *dicts* too.

## Cons
- Requires Python `3.10+`.
- Pattern matching is syntactic sugar; at runtime it still performs attribute checks.
- Not as explicit about the operation’s intent as Visitor.
]
]

<!--???

- Uses Python 3.10 structural pattern matching (`match`).
- No explicit typing; the patterns are *structural*.
- Adding a new shape: just add a new pattern.
- Still uses a single function; pattern matching does the dispatching.
-->

---

# Alternative 6: The Visitor Pattern

.columns[
.column[
```python
import abc


# Visitor interface

class ShapeVisitor(abc.ABC):
    def visit_circle(self, shape: Circle): ...
    def visit_square(self, shape: Square): ...
    def visit_triangle(self, shape: Triangle): ...


# Concrete visitor: Area

class AreaVisitor(ShapeVisitor):
    def visit_circle(self, shape: Circle):
        return 3.14159 * shape.radius ** 2

    def visit_square(self, shape: Square):
        return shape.side ** 2

    def visit_triangle(self, shape: Triangle):
        p = (shape.a + shape.b + shape.c) / 2
        return (p * (p-shape.a) * (p-shape.b) * (p-shape.c)) ** 0.5
```
]
.column[
```py
# Shapes accept a visitor

class Circle:
    ...
    def accept(self, visitor: ShapeVisitor):
        return visitor.visit_circle(self)

class Square:
    ...
    def accept(self, visitor: ShapeVisitor):
        return visitor.visit_square(self)

class Triangle:
    ...
    def accept(self, visitor: ShapeVisitor):
        return visitor.visit_triangle(self)

# Usage

area_visitor = AreaVisitor()

for shape in (Circle(1), Square(2), Triangle(3,4,5)):
    print(shape.accept(area_visitor))
```
]
]

<!--???

- Separates *operations* (`AreaVisitor`) from *data* (`Shape` classes).
- Adding a new operation → create a new visitor class.
- Adding a new shape → add a new `accept` method and a new visitor method.
- Keeps the shape classes lean and highly reusable.
-->

---

# Comparison Table

| Approach          | Extensibility |                                                                                                                                                           |
| :---------------- | :------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Methods in Shapes | Low           | Universally supported<br/>Easy for small projects, but adding new operations requires modifying every shape class, which quickly becomes unmanageable.    |
| `isinstance`      | Low           | Universally supported<br/>Simple, but leads to duplicated logic and poor scalability as both new shapes and operations require changes everywhere.        |
| `overload`        | Low           | Improves type safety and IDE support, but still relies on manual dispatch and updating overloads for new shapes.                                          |
| `singledispatch`  | High          | Clean separation of operations from data, extensible for new shapes and operations, but limited to single-argument dispatch.                              |
| Pattern Matching  | Medium        | Highly readable and flexible, but only available in recent Python versions and can become unwieldy with many patterns.                                    |
| Visitor Pattern   | High          | Best for extensibility, allowing new shapes and operations with minimal changes, though it introduces more boilerplate and requires discipline in design. |

Pick the method that balances readability, maintainability, and compatibility.

<!--

- The Visitor pattern gives both clean extensibility for shapes and operations.
- Trade‑offs: extra boilerplate vs. clear separation of concerns.

-->

---

# Take‑away

* The Visitor pattern is a powerful tool when you have **many data structures** and **many operations** that need to evolve independently.
* Python offers several idiomatic ways to achieve similar goals (`singledispatch`, `overload`, pattern matching, and `isinstance`).
* Choose the approach that best fits your codebase’s complexity and your team’s familiarity.
* Remember: **Keep data and behaviour separate** to keep your code maintainable.
