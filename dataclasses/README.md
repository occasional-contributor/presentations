class: center, middle

# An Introduction to Python Data Classes

???

*   Welcome everyone. Today, we're diving into a really useful feature in Python 3.7+ called Data Classes.
*   Our goal is to understand what they are, why they're beneficial, and how to use them effectively.
*   This presentation draws heavily from the excellent article on Real Python, so credit where it's due!
*   Let's get started.

---

## The "Old" Way: Boilerplate Blues

.columns[
.column[
Before Python 3.7, if you wanted a class primarily to store data, you'd write a lot of repetitive code.

This is verbose for such a simple concept.
]
.column[
```python
class Point:
    def __init__(
        self,
        x: float,
        y: float,
    ):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def __eq__(
        self,
        other,
    ):
        if not isinstance(other, Point):
            return NotImplemented

        return (self.x, self.y) == (other.x, other.y)

# And maybe __lt__, __le__, __gt__, __ge__ for ordering...
# And __hash__ if you want it in a set or dict key...
```
]
]

???

*   Let's start by looking at a common scenario. We often need classes that are essentially containers for data.
*   Think of a `Point` class, an `Employee` record, or a `Configuration` object.
*   Traditionally, you'd have to manually implement `__init__` to assign attributes.
*   Then, for good practice and usability, you'd add `__repr__` for a helpful string representation.
*   And `__eq__` for comparing instances.
*   If you need ordering, that's more dunder methods. If you need it to be hashable, that's `__hash__`.
*   It adds up quickly, and it's all pretty standard stuff – boilerplate.

---

## Quick Detour: Demystifying Dunder Methods

Before we see how `@dataclass` is magic, let's talk about `dunder` methods.

*   **"Dunder" = Double Underscore.** Names like
    *   `__init__`
    *   `__repr__`
    *   `__eq__`
*   These are **special methods** in Python
*   You don't typically call them directly (e.g., `my_object.__init__()`)
*   Instead, Python calls them **implicitly** in response to certain operations or built-in functions
    *   `x + y` might call `x.__add__(y)`
    *   `str(obj)` calls `obj.__str__()`
    *   `obj1 == obj2` calls `obj1.__eq__(obj2)`

They are the hooks that let your objects integrate with Python's core mechanics.

???

*   Alright, before we fully appreciate the magic of data classes, let's take a very quick detour to understand a fundamental concept in Python: dunder methods.
*   You've probably seen them – methods with names starting and ending with double underscores. "Dunder" is just a colloquial term for "double underscore."
*   These aren't methods you'd normally call directly from your code like `my_object.do_something()`.
*   Instead, they are special hooks that Python itself uses. When you perform an operation like adding two objects, or converting an object to a string, or comparing objects, Python looks for and calls the corresponding dunder method on your objects.
*   They are key to Python's data model, allowing your custom classes to behave like built-in types.

---

## Common Dunder Methods (from our "Old Way" example)

Let's revisit the dunders from our manual `Point` class:

*   `__init__(self, ...)`
    *   The **initializer** (often called constructor)
    *   Called when you create an instance: `Point(x, y)`
    *   Sets up the initial state of the object
*   `__repr__(self)`
    *   The "official" **string representation**
    *   Should be unambiguous, ideally allowing recreation of the object: `eval(repr(obj)) == obj`
    *   Called by `repr()` function, and shown in the interactive console if `__str__` isn't defined
    *   Primarily for developers
*   `__eq__(self, other)`
    *   Defines behavior for the **equality operator (`==`)**
    *   `point1 == point2` calls `point1.__eq__(point2)`

Others include `__str__` (user-friendly string), `__lt__` (ordering), `__hash__` (hashability for sets/dict keys).

???

*   Now, let's connect this to the `Point` class we saw earlier, the one we wrote manually.
*   `__init__` is probably the most common dunder method you'll write. It's what gets called when you instantiate your class, responsible for setting up its attributes.
*   `__repr__` is crucial for debugging and logging. It should provide a clear, unambiguous string representation of the object. The convention is that, if possible, `eval(repr(my_object))` should give you an equivalent object back. This is super handy for developers.
*   `__eq__` is what makes the `==` operator work for your custom objects. Without it, Python would just compare object identities (are they the exact same object in memory?), which is usually not what you want for value objects like our `Point`.
*   There are many other dunder methods. `__str__` is for a more human-readable string representation (what `print()` uses by default). `__lt__`, `__gt__` etc., are for ordering. `__hash__` is vital if you want to use your objects as keys in dictionaries or store them in sets.

---

## Why Dunders Matter & The Data Class Link

Implementing these dunder methods correctly is what makes your Python classes:

*   **Pythonic:** They behave as expected within the Python ecosystem.
*   **Usable:** They work with built-in functions (`len()`, `str()`, `sorted()`) and operators.
*   **Robust:** Well-defined equality, representation, etc.

**The Challenge:** Writing them manually for simple data-holding classes is repetitive (as we saw!).

**This is *exactly* where `@dataclass` shines!**
It automatically generates many of these common dunder methods for you, based on your field definitions.

???
*   So, why is it important to get these dunder methods right?
*   Because they are fundamental to making your classes "Pythonic." They allow your objects to integrate seamlessly with the rest of the language and behave like built-in types.
*   When you define `__eq__`, your objects can be compared with `==`. When you define ordering methods, they can be sorted. When you define `__str__` and `__repr__`, they can be printed and inspected meaningfully.
*   The problem, as highlighted by our "Old Way" example, is that for classes that are mainly just holding data, writing `__init__`, `__repr__`, `__eq__`, and potentially others, is a lot of boilerplate code. It's necessary, but it's repetitive and error-prone.
*   And *this* is the core problem that data classes solve. The `@dataclass` decorator looks at the fields you declare and says, "Ah, you probably want a standard `__init__`, a good `__repr__`, a sensible `__eq__`, etc." and it generates them for you, following best practices.
*   So, data classes aren't doing something entirely new; they're automating the creation of these essential dunder methods in a smart way. Now, let's see how they do it!

---

## Enter: `@dataclass`

.columns[
.column[
Python 3.7 introduced the `dataclasses` module and the `@dataclass` decorator.

It automatically generates methods like `__init__()`, `__repr__()`, `__eq__()`, and more!
]
.column[
```python
@dataclass
class Point:
    x: float
    y: float


p1 = Point(1.5, 2.5)
p2 = Point(1.5, 2.5)
p3 = Point(3.0, 4.0)

print(p1)        # Output: Point(x=1.5, y=2.5)
print(p1 == p2)  # Output: True
print(p1 == p3)  # Output: False
```
]
]

???

*   So, how do data classes solve this? With a simple decorator: `@dataclass`.
*   You import it from the `dataclasses` module.
*   Notice the key difference: we just declare the fields with type hints. No `__init__`, no `__repr__`, no `__eq__` written by us.
*   The `@dataclass` decorator inspects these type-hinted field declarations and generates those common methods for us.
*   Look at the example. We define `Point` with just `x: float` and `y: float`.
*   Instantiating it works as expected. The `print(p1)` output shows a helpful `__repr__` was generated.
*   Comparisons with `==` work correctly because `__eq__` was also generated.
*   Much cleaner, right?

---

## What Does `@dataclass` Provide by Default?

When you use `@dataclass` without any arguments, you get:

*   *`__init__(self, field1, field2, ...)`*
    *   Initializes attributes
*   *`__repr__(self)`*
    *   Provides a string representation (e.g., *`ClassName(field1=value1, ...)`*)
*   *`__eq__(self, other)`*
    *   Compares instances based on their fields
*   *`__lt__(self, other)`*, *`__le__(self, other)`*, *`__gt__(self, other)`*, *`__ge__(self, other)`*
    *   If *`order=True`* (default is *`False`*)
*   *`__hash__(self)`*
    *   If *`eq=True`* and *`frozen=True`* (more on this later)

Type annotations are **mandatory** for defining fields.

???

*   Let's be specific about what `@dataclass` gives you "out of the box."
*   The `__init__` method is created to accept arguments for each field you define, in the order you define them.
*   `__repr__` gives you that nice, readable string.
*   `__eq__` allows you to compare two instances of your data class field by field.
*   By default, comparison methods for ordering (`<`, `<=`, `>`, `>=`) are *not* generated. You need to explicitly ask for them with `order=True`. We'll see how.
*   A `__hash__` method can also be generated, which is crucial if you want to use instances as dictionary keys or put them in sets. This has specific conditions we'll touch upon.
*   And a critical point: data classes *rely* on type hints to identify fields. So, `x: float` is not just good practice; it's how the data class knows `x` is a field.

---

## Customizing Behavior: Decorator Arguments

.columns[
.column[
The `@dataclass` decorator accepts several boolean arguments to customize behavior:

*   `init`
    *   Generate `__init__` (default `True`)
*   `repr`
    *   Generate `__repr__` (default `True`)
*   `eq`
    *   Generate `__eq__` (default `True`)
*   `order`
    *   Generate `__lt__`, `__le__`, `__gt__`, `__ge__` (default `False`)
    *   If `True`, fields are compared in the order they are defined.
*   `unsafe_hash`
    *   Controls `__hash__` generation (default `False`)
    *   If `False` (default): `__hash__` is generated based on `eq` and `frozen`.
    *   If `True`: `__hash__` is generated even if it's not strictly "safe" (e.g., mutable).
    *   If `None`: `__hash__` is set to `None` (like in Python 3 for mutable classes).
*   `frozen`
    *   If `True`, instances are immutable (default `False`)
    *   Assigning to fields after creation raises `FrozenInstanceError`.
    *   Makes instances hashable if `eq=True`.
]
.column[
```python
@dataclass(
    order=True,
    frozen=True,
)
class ImmutablePoint:
    x: float
    y: float

p1 = ImmutablePoint(1, 2)
p2 = ImmutablePoint(0, 3)
# p1.x = 5  # This would raise FrozenInstanceError
print(p1 < p2) # Potentially True or False, based on x then y
# hash(p1)  # This works!
```
]
]

???

*   You're not stuck with the defaults. `@dataclass` is flexible.
*   You can tell it *not* to generate `__init__`, `__repr__`, or `__eq__` if you want to provide your own custom versions.
*   `order=True` is how you get those rich comparison methods. The comparison is done lexicographically, field by field, in the order they're defined in the class.
*   `frozen=True` is a big one. It makes your data class instances immutable. Once created, their attributes cannot be changed. This is great for data integrity and also allows instances to be hashable by default (if `eq` is also true). Trying to change an attribute on a frozen instance will raise a `FrozenInstanceError`.
*   `unsafe_hash` gives you more control over `__hash__` generation, but the default behavior (tied to `eq` and `frozen`) is usually what you want.
*   In the example, `ImmutablePoint` will be ordered and immutable. You can try to sort lists of these points, and they can be used as dictionary keys.

---

## Default Values and `default_factory`

.columns[
.column[
Fields can have default values, just like function arguments.

**Important:** For mutable default values (like lists or dicts), use `field(default_factory=...)`.

If you used `tags: list[str] = []`, all instances would share the *same* list.
]
.column[
```python
@dataclass
class InventoryItem:
    name: str
    unit_price: float
    quantity_on_hand: int = 0  # Simple default
    tags: list[str] = field(default_factory=list)  # For mutable defaults

# Usage
item1 = InventoryItem("Pen", 1.00)
print(item1)  # quantity_on_hand=0, tags=[]

item2 = InventoryItem("Pencil", 0.50, 100, ["writing", "school"])
print(item2)  # quantity_on_hand=100, tags=['writing', 'school']
```
]
]

???

*   Just like function parameters, your data class fields can have default values.
*   For simple, immutable types (integers, strings, tuples), you can assign a default directly: `quantity_on_hand: int = 0`.
*   Now, a very important point: mutable defaults. If a field is, say, a list, and you want it to default to an empty list for each new instance, you *must* use `default_factory`.
*   The `field()` function from the `dataclasses` module is used for more advanced field configurations, including `default_factory`.
*   `default_factory=list` tells the data class to call `list()` (which creates a new empty list) every time a new instance is created without that field specified.
*   If you were to write `tags: list[str] = []`, that empty list `[]` is created *once* when the class is defined. All instances would then share that single list object, which is almost never what you want. Changes to `item1.tags` would affect `item2.tags`. `default_factory` avoids this common Python pitfall.

---

## `__post_init__`

.columns[
.column[
Sometimes, you need to do more setup after the default `__init__` has run.

Use `__post_init__(self)` for this. It's called automatically after `__init__`.

Fields used only in `__post_init__` can be marked with `field(init=False)`.
]
.column[
```python
@dataclass
class Circle:
    x: float
    y: float
    radius: float
    area: float = field(init=False)  # Not an __init__ parameter

    def __post_init__(self):
        if self.radius < 0:
            raise ValueError("Radius cannot be negative")

        self.area = math.pi * self.radius ** 2

c = Circle(0, 0, 5)
print(c)  # Circle(x=0.0, y=0.0, radius=5.0, area=78.539...)
# c_invalid = Circle(0,0,-1) # Raises ValueError
```
]
]

???

*   What if you need to calculate a field based on other fields, or perform some validation after the instance is initialized? That's where `__post_init__` comes in.
*   If you define a method named `__post_init__` in your data class, it will be automatically called by the generated `__init__` method, right after all the fields have been assigned.
*   In this `Circle` example, we want to calculate the `area`. `area` isn't something you'd typically pass to the constructor; it's derived.
*   So, we mark `area: float = field(init=False)`. This tells the data class: "area is a field, but don't include it as a parameter in the `__init__` method you generate, and don't expect it to be passed during instantiation."
*   Then, in `__post_init__`, we calculate `self.area`. We also add a validation check for the radius.
*   This is a clean way to separate the basic initialization (handled by `@dataclass`) from more complex setup or validation logic.

---

## Inheritance

.columns[
.column[
Data classes support inheritance.

Field ordering: base class fields come first, then derived class fields.

Be careful if overriding fields with defaults in subclasses.
]
.column[
```python
@dataclass
class Position:
    name: str
    lon: float
    lat: float

@dataclass
class Capital(Position):
    country: str

# Capital inherits name, lon, lat from Position
# The __init__ for Capital will be:
# __init__(self, name: str, lon: float, lat: float, country: str)
cap = Capital("Paris", 2.3522, 48.8566, "France")
print(cap)
# Output: Capital(name='Paris', lon=2.3522, lat=48.8566, country='France')
```
]
]

???

*   Data classes play well with inheritance. You can create a base data class and then have other data classes inherit from it.
*   Fields from the base class are included in the derived class.
*   The generated `__init__` method for the derived class will include all fields from the base class(es) followed by fields specific to the derived class. The order matters.
*   In this example, `Capital` inherits `name`, `lon`, and `lat` from `Position` and adds its own `country` field.
*   The `__repr__` and other generated methods will also correctly include all fields.
*   One thing to be mindful of, as with regular class inheritance, is how default values on fields interact when you override fields in subclasses. The rules are generally intuitive but worth testing for complex scenarios.

---

## Fine-Grained Field Control with `field()`

.columns[
.column[
We saw `default_factory` and `init=False`. `field()` offers more:
*   `field(default=...)`
    *   Specify a default value.
*   `field(default_factory=...)`
    *   Specify a factory for default values (for mutable types).
*   `field(init=False)`
    *   Exclude from `__init__` parameters.
    *   Value must be set elsewhere (e.g., `__post_init__`).
*   `field(repr=False)`
    *   Exclude from the generated `__repr__` string.
*   `field(compare=False)`
    *   Exclude from comparison methods (`__eq__`, `__lt__`, etc.).
*   `field(hash=None|True|False)`
    *   Override class-level `unsafe_hash` for this field's inclusion in `__hash__`.
*   `field(metadata=...)`
    *   A dictionary for custom data, not used by `dataclasses` itself but available for your tools/libraries.
]
.column[
```python
@dataclass
class User:
    user_id: int
    username: str
    password_hash: str = field(  # Don't show or compare
        repr=False,
        compare=False,
    )
    is_active: bool = field(default=True)

u = User(1, "jane_doe", "a_very_secret_hash")
print(u)  # User(user_id=1, username='jane_doe', is_active=True)
# password_hash is not shown!
```
]
]

???

*   The `field()` function is your go-to for detailed control over individual fields.
*   We've already seen `default_factory` and `init=False`.
*   `repr=False` is useful for fields you don't want to appear in the string representation, like sensitive data (e.g., a password hash) or very long fields.
*   `compare=False` means that field will be ignored when comparing two instances for equality or order. This is useful if some fields are just metadata or don't define the "identity" of the object.
*   `hash` lets you specify if a particular field should be included in hash calculations, overriding the class-level `unsafe_hash` setting for that field.
*   `metadata` is a neat feature for library authors or advanced use cases. You can attach arbitrary information to a field that your own code or other tools can then inspect. Data classes themselves don't use it.
*   The `User` example shows how `password_hash` is hidden from the `repr` output, which is good practice.

---

## When to Use Data Classes?

*   When your class is primarily a **container for data**.
*   To **reduce boilerplate** for common dunder methods.
*   When you want **readable and self-documenting** field definitions via type hints.
*   For simple, immutable objects (`frozen=True`).
*   Quickly defining structures for things like API responses, configuration, simple records.

## When *Maybe* Not?

*   When your class has a lot of **behavior (methods)** and data is secondary.
    *   Traditional classes might still be clearer.
*   If you need extreme flexibility not covered by `dataclass` options (though `attrs` library might be an alternative then).

???

*   So, when should you reach for data classes?
*   The primary use case is when you're defining a class whose main job is to hold and manage data. Think of it as a structured "record."
*   They shine at cutting down on repetitive code for `__init__`, `__repr__`, `__eq__`, etc.
*   The mandatory type hints make the fields very clear and serve as good documentation.
*   They are excellent for creating immutable objects using `frozen=True`, which can lead to more robust and predictable code.
*   Think about parsing JSON from an API, representing application settings, or just simple value objects.
*   When might they *not* be the best fit?
*   If your class is less about the data it holds and more about the complex operations or logic it performs (i.e., it has many methods), a traditional class might still feel more natural. Data classes can have methods, but if methods are the *main* thing, the benefits of `@dataclass` are less pronounced.
*   If you need even more power and customization than data classes offer, the third-party `attrs` library is a fantastic, more feature-rich alternative that inspired data classes.

---

## Data Classes vs. Alternatives

.columns[
.column[
*   **Plain Classes:**
    *   Pros:
        *   Full control
    *   Cons:
        *   Verbose for data-centric classes (the problem data classes solve!)
*   **`collections.namedtuple`:**
    *   Pros:
        *   Lightweight, immutable, fields accessible by name and index
    *   Cons:
        *   Less flexible (all fields in `__init__`, no easy defaults without subclassing, no type hints enforced by default, methods are harder to add)
        *   Syntax is a bit dated
]
.column[
*   **Dictionaries:**
    *   Pros:
        *   Simple
    *   Cons:
        *   No type safety
        *   No fixed structure
        *   Attribute access via `['key']` is verbose
        *   No methods.
*   **`attrs` library (third-party):**
    *   Pros:
        *   Even more features and flexibility than `dataclasses` (converters, validators, etc.)
        *   Works on older Python versions
    *   Cons:
        *   It's a third-party dependency
        *   `dataclasses` is in the standard library (Python 3.7+), and backported to Python 3.6
]
]

Data classes hit a "sweet spot" for many common use cases in modern Python.

???

*   It's useful to compare data classes to other ways you might structure data in Python.
*   **Plain Classes:** We've seen this. Maximum control, but you write everything yourself.
*   **`namedtuple`:** These have been around for a while. They are good for simple, immutable, tuple-like objects where you can access elements by name. But they are less flexible than data classes – for instance, defining default values or adding custom methods is more cumbersome. They also don't integrate type hints as directly.
*   **Dictionaries:** Obviously very flexible, but they offer no structure, no type safety, and accessing items via string keys can be error-prone and less readable than attribute access.
*   **`attrs`:** This is a very popular and powerful third-party library. In fact, `dataclasses` was heavily inspired by `attrs`. `attrs` offers even more features, like built-in converters and validators for fields. If you need that extra power or are working on Python versions before 3.7, `attrs` is an excellent choice. The main "con" is simply that it's an external dependency, whereas `dataclasses` is part of Python's standard library.
*   Data classes provide a great balance of simplicity, power, and integration into the language for many common scenarios.

---

## Summary: Key Takeaways

*   `@dataclass` (Python 3.7+) **significantly reduces boilerplate** for classes that primarily store data.
*   Automatically generates `__init__`, `__repr__`, `__eq__`, and optionally `__lt__`, `__hash__`, etc.
*   **Type hints are essential** for defining fields.
*   Offers customization via decorator arguments (`frozen`, `order`) and `field()` options (`default_factory`, `repr=False`).
*   Supports `__post_init__` for custom initialization logic.
*   Improves code **readability and maintainability**.

**Embrace data classes for cleaner, more Pythonic data structures!**

???

*   Let's quickly recap the main benefits.
*   The biggest win is reducing boilerplate. Less code to write, less code to test, less code to maintain.
*   You get sensible implementations of essential dunder methods for free.
*   They encourage (and require) the use of type hints for fields, which is great for code clarity and static analysis.
*   You have good control over the generated methods and individual field behaviors.
*   `__post_init__` gives you an escape hatch for more complex setup.
*   Overall, they lead to code that's easier to read, understand, and work with.
*   If you're working with Python 3.7 or newer, I highly encourage you to start using data classes wherever they make sense. They're a fantastic addition to the language.

---

class: center, middle

# Questions?

## Thank You!

???

*   That concludes the overview of Python data classes.
*   I hope this has given you a good understanding of what they are and how they can help you write better Python code.
*   Are there any questions?
*   (After Q&A) Thank you all for your time!
