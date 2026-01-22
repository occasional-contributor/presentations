class: center, middle

# Visitor Pattern in Python

## Separating behaviour from data

### A Practical Guide with Multiple Implementation Strategies

---

# What is the Visitor Pattern?

### Definition

The Visitor pattern allows you to **add operations** to a class hierarchy **without changing the classes** themselves.

It uses a technique called **Double Dispatch** to route a specific operation to a specific type.

### Why?

- **Decoupling** separates data structures from algorithms.
- **Cleaner Code** avoids scattering `if`/`elif` `isinstance(...)` checks.
- **Extensibility** follows the **Open/Closed Principle**.

---

# The Problem: Shapes

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
We have a collection of shape objects.

We need to perform several unrelated operations on them:

- Compute area
- Compute perimeter
- Render SVG

### Challenge
How do we add these without polluting the Shape classes?
]
]
---

# Trivial Approach: Methods Inside Shapes

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
### Why is this a problem?

- **Tight Coupling**
  - Logic is inside data classes.
- **Modification Risk**
  - Adding a new shape requires adding new code to every operation.
  - Adding a new operation requires modifying every shape class.
- Violates the **Open/Closed Principle**
  - Classes are **open** for extension but **closed** for modifications.
]
]

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
### Pros
- **Universally supported**
  - works on any Python version.
- **Simple**
  - Very straightforward; no imports required.
  - No external libraries or advanced features.

### Cons
- **Scattering**
  - Each operation must implement its own chain of `isinstance` checks.
- **Duplication**
  - Common patterns copy‑pasted across functions.
- **Harder to extend**
  - Adding a new shape means editing *every* operation.
]
]

---

# Alternative 2: `functools.singledispatch`

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
### Pros
- **Clean**
  - Simple syntax for a small number of operations.
  - Keeps **operation logic** separate from shapes.
- **Extensible**
  - Register new types without modifying shapes.

### Cons
- **Limited**
  - Only supports *single* dispatch; not suitable for multi‑argument dispatch.
- **Functions only**
  - Requires all operations to be **functions**; shape classes cannot be extended to add new operations.
- **IDE Support**
  - Poor IDE support for type checking in older Python versions.
]
]

---

# Alternative 3: `typing.overload`

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
### Pros
- **Safety**
  - Gives static type checkers precise signatures.
- **Simple**
  - Keeps a single implementation; no boilerplate visitor classes.
- **IDE Support**
  - Works well with `mypy` or IDE autocompletion.

### Cons
- **Not a Runtime Solution**
  - `@overload` only affects type checking.
  - Runtime dispatch still needs `isinstance` checks.
- **Manual dispatch**
  - No automatic registration; you must write the dispatch logic manually.
- **Duplication and drift risk**
  - Adding a new shape requires updating the overload list **and** the conditional block.
]
]

---

# Alternative 4: Combining `singledispatch` and `overload`

.columns[
.column[
```python
@typing.overload
def area(shape: Circle) -> float: ...

@typing.overload
def area(shape: Square) -> float: ...

@typing.overload
def area(shape: Triangle) -> float: ...

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
### Pros
- **Best of both worlds**
  - Runtime extensibility with static tooling
  - `singledispatch` supplies runtime dispatch, while `overload` supplies static type checking.
- **Separation of concerns**
  - Keeps operation logic separate from shapes.

### Cons
- **Duplication and drift risk**
  - Need to maintain functions and typing overloads
- **IDE Support**
  - Poor IDE support for type checking in older Python versions.
- **Limited**
  - Only supports *single* dispatch; not suitable for multi‑argument dispatch.
]
]

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
### Pros
- **Readable**
  - Clean, declarative syntax.
- **Powerful**
  - Can match structure, values, and types simultaneously.

### Cons
- **Version lock**
  - Requires Python `3.10+`.
- **Explicit**
  - Pattern matching is syntactic sugar
  - At runtime it still performs attribute checks.
]
]

---

# Alternative 6: The Visitor Pattern

.columns[
.column[
```python
import abc


class ShapeVisitor(abc.ABC):
    @abc.abstractmethod
    def visit_circle(self, s: Circle): ...

    @abc.abstractmethod
    def visit_square(self, s: Square): ...

    @abc.abstractmethod
    def visit_triangle(self, s: Triangle): ...

class AreaVisitor(ShapeVisitor):
    def visit_circle(self, s: Circle):
        return 3.14159 * s.radius ** 2

    def visit_square(self, s: Square):
        return s.side ** 2

    def visit_triangle(self, s: Triangle):
        p = (s.a + s.b + s.c) / 2
        return (
            p * (p-s.a) * (p-s.b) * (p-s.c)
        ) ** 0.5
```
]
.column[
```py
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

shapes = (
    Circle(1),
    Square(2),
    Triangle(3,4,5),
)
area_visitor = AreaVisitor()

for shape in shapes:
    print(shape.accept(area_visitor))
```
]
.column[
### Pros
- Easy to add new operations
- Keeps node classes "data-focused"
- Groups operation-specific logic together
- Double-dispatch avoids `isinstance` chains

### Cons
- Hard to add new node types (the big trade-off)
- Boilerplate and ceremony
- Visitor interface churn
- More coupling than it first appears
]
]

---

# Comparison Table

| Approach                   | Extensibility |                                                                                                                                                           |
| :------------------------- | :------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Methods in Shapes          | Low           | Universally supported<br/>Easy for small projects, but adding new operations requires modifying every shape class, which quickly becomes unmanageable.    |
| `isinstance`               | Low           | Universally supported<br/>Simple, but leads to duplicated logic and poor scalability as both new shapes and operations require changes everywhere.        |
| `typing.overload`          | Low           | Improves type safety and IDE support, but still relies on manual dispatch and updating overloads for new shapes.                                          |
| `functools.singledispatch` | High          | Clean separation of operations from data, extensible for new shapes and operations, but limited to single-argument dispatch.                              |
| Pattern Matching           | Medium        | Highly readable and flexible, but only available in recent Python versions and can become unwieldy with many patterns.                                    |
| Visitor Pattern            | High          | Best for extensibility, allowing new shapes and operations with minimal changes, though it introduces more boilerplate and requires discipline in design. |

.footnote[Pick the method that balances readability, maintainability, and compatibility.]

---

# Take‑away

* The Visitor pattern is a powerful tool when you have **many data structures** and **many operations** that need to evolve independently.
* Python offers several idiomatic ways to achieve similar goals (`singledispatch`, `overload`, pattern matching, and `isinstance`).
* Choose the approach that best fits your codebase’s complexity and your team’s familiarity.
* Remember: **Keep data and behaviour separate** to keep your code maintainable.
