class: center, middle

# Python f-strings
## String interpolation & formatting
(and what changed in Python 3.12)

???
- Goal: introduce f-strings, show how they compare to older approaches, and highlight the Python 3.12 improvements.
- Audience assumption: you already write Python, but want cleaner string formatting (and fewer interpolation headaches).

---

# Why f-strings?

## Concise string interpolation
Embed values directly with `{...}`

## Readable
The “template” and the variables live in one place

## Fast
Typically faster than `%` and `.format()`

## Powerful formatting
Supports Python’s format mini-language

???
- Emphasize: f-strings arrived in Python 3.6 (PEP 498).
- Mention alternatives: `%` operator and `str.format()`.
- Note: f-strings evaluate at runtime, so names must be in scope.

---

# What is an f-string?

An f-string is a string literal **prefixed with `f` or `F`**:

```python
name = "Avery"
age = 29
msg = f"{name} is {age} years old"
```

- Anything inside `{}` is a Python expression
- That expression is evaluated at runtime and inserted into the string

???
- Call out: it’s not just variables—expressions, function calls, and more can go inside `{}`.
- Common failure mode: syntax errors from braces or invalid expressions.

---

# Before Python 3.6: your options

1) The modulo operator (`%`)  
2) The `str.format()` method

We’ll do a quick refresher so the f-string advantages are obvious.

???
- This sets context: f-strings didn’t appear in a vacuum.
- The point isn’t “never use old tools,” but “know the tradeoffs.”

---

# `%` operator: quick & classic

```python
name = "Avery"
msg = "Hello, %s" % name
```

- Uses **conversion specifiers** like `%s`, `%d`, `%.2f`
- Multiple values typically passed as a tuple:

```python
msg = "%s is %s" % ("Avery", 29)
```

???
- Explain: left operand is the format string; right operand is value(s).
- `%s` turns the input into a string; `%.2f` formats a float to 2 decimals.

---

# `%` formatting examples (and gotchas)

Formatting examples:

```python
price = 12.5
print("Total: %.2f" % price)   # 12.50
print("[%5s]" % 7)             # right-aligned width 5
```

Gotcha: tuples can be confusing:

```python
data = ("x", "y")
print("data=%s" % data)        # may be interpreted as multiple args in some cases
```

Workaround pattern you may see:

```python
print("data=%s" % (data,))
```

???
- The “single-item tuple” trick is a classic readability killer.
- Also mention: `%` has limited formatting compared to the mini-language used by `format()` and f-strings.

---

# `str.format()`: more flexible, mini-language support

Replacement fields use `{}`:

```python
name = "Avery"
age = 29
msg = "{} is {}".format(name, age)
```

Reordering with indices:

```python
msg = "{1}, {0}".format("first", "second")
```

Readable keyword arguments:

```python
msg = "{name} is {age}".format(name="Avery", age=29)
```

???
- Highlight: `.format()` is a big step up from `%` for clarity and capabilities.
- Still more verbose than f-strings because the “template” and arguments are separated.

---

# `.format()` with dicts + formatting

Dictionary interpolation:

```python
person = {"name": "Avery", "age": 29}
msg = "{name} is {age}".format(**person)
```

Format specifiers (mini-language):

```python
print("{:.2f}".format(12.5))       # 12.50
print("{:=^30}".format("title"))   # =======title========
```

???
- The mini-language is the key: alignment, padding, precision, types, etc.
- This same mini-language is what f-strings reuse (so you don’t lose power by switching).

---

# F-strings: interpolation feels “native”

Basic interpolation:

```python
name = "Avery"
age = 29
msg = f"{name} is {age}"
```

No operator, no method call—just write the expression where you want it.

Important: variables must be in scope when the f-string runs.

???
- Reinforce: evaluation happens at runtime.
- If you build f-strings at import time, make sure names exist then.

---

# F-strings can embed expressions

You can embed “almost any” Python expression:

```python
print(f"2 * 21 = {2 * 21}")
```

Method calls:

```python
name = "Avery"
print(f"Shouting: {name.upper()}")
```

Even comprehensions:

```python
print(f"Powers: {[2**n for n in range(6)]}")
```

???
- This is where f-strings start to feel like a superpower.
- Caution: just because you can embed complex logic doesn’t mean you should—watch readability.

---

# Formatting with f-strings (mini-language)

Under the hood, formatting uses `.__format__()` and the format mini-language.

Same formatting you’d do in `.format()`, but tighter:

```python
total = 12.5
print(f"Total: {total:.2f}")
```

Alignment / fill:

```python
title = "Report"
print(f"{title:=^30}")
```

Dynamic specifiers are possible too:

```python
width = 10
n = 42
print(f"{n:0{width}d}")   # zero-pad to `width`
```

???
- The colon `:` introduces the format specifier: `{expr:spec}`.
- Dynamic formatting is a nice trick for tabular outputs.

---

# Choosing an object representation: `!s` vs `!r`

f-strings support two helpful conversion flags:

| Flag | Meaning                             |
| ---- | ----------------------------------- |
| `!s` | use `.__str__()` (user-friendly)    |
| `!r` | use `.__repr__()` (developer/debug) |

Example:

```python
value = {"a": 1}
print(f"{value!s}")
print(f"{value!r}")
```

???
- In many built-in types, `str()` and `repr()` look similar; in custom classes they can differ a lot.
- Useful when building logs/debug output or diagnostics.

---

# Self-documenting expressions (debugging)

Python supports “show me the name and value” with `=` inside `{}`:

```python
count = 3
print(f"{count=}")
# count=3
```

Whitespace is optional, but preserved:

```python
count = 3
print(f"{count = }")
# count = 3
```

???
- Great for quick debugging prints without manually typing labels.
- This is especially nice when dumping multiple values: `f"{x=}, {y=}, {state=}"`.

---

# Performance: f-strings are usually faster

General guidance:

- f-strings tend to be faster than `%` and `.format()`
- `.format()` is often slowest (extra function/method calls)

If you benchmark with `timeit`, you’ll typically see f-strings come out ahead.

???
- Don’t oversell micro-optimizations—readability is usually the bigger win.
- But in hot paths (tight loops), f-strings can help.

---

# Python 3.12+: big f-string upgrades

Python 3.12 replaced the old f-string parser with a new implementation (PEG-based).

Notable improvements:
- Nested expressions are easier
- Backslashes allowed in expressions
- You can reuse quotation marks inside expressions
- Comments and line breaks in `{...}`
- Better error messages for f-string mistakes

???
- This is a “quality of life” release for f-strings.
- If someone was burned by f-string limitations in 3.11, 3.12 is worth revisiting.

---

# Quotes: reusing delimiters (fixed in 3.12)

A common pain: quoting inside `{...}`.

Typical workaround (mix quotes):

```python
person = {"name": "Avery"}

print(f"Hello {person['name']}")
# Hello Avery

print(f"Hello {person["name"]}")

>>> f"Hello, {person["name"]}!"
  File "<input>", line 1
    f"Hello, {person["name"]}!"
                      ^^^^
SyntaxError: f-string: unmatched '['
```

In Python 3.12, reusing quotes inside expressions is supported, reducing awkward cases where older versions raised `SyntaxError`.

???
- Mention the “natural limit” pre-3.12: nesting levels were constrained by available string delimiters.
- In 3.12, reusing quotes removes that practical limit and makes nesting less fragile.

---

# Backslashes (3.12)

Before 3.12, backslashes inside `{...}` caused syntax errors in many cases.

Python 3.12 lifts that limitation so escape sequences can appear within expressions.

```python
>>> words = ["Hello", "World!", "I", "am", "a", "Pythonista!"]

>>> f"{'\n'.join(words)}"  # Before py3.12
  File "<input>", line 1
    f"{'\n'.join(words)}"
                        ^
SyntaxError: f-string expression part cannot include a backslash

>>> print(f"{'\n'.join(words)}")  # py3.12+
Hello
World!
I
am
a
Pythonista!
```

Also improved:
- line breaks inside `{...}` (like parentheses)

---

# Inline comments (3.12)

With Python 3.12, inline comments are supported.

```python
>>> employee = {
...     "name": "John Doe",
...     "age": 35,
...     "job": "Python Developer",
... }
```
```python
>>> # Before Python 3.12
>>> f"""Storing employee's data: {
...     employee['name'].upper()  # Always uppercase name before storing
... }"""
  File "<stdin>", line 3
    }"""
        ^
SyntaxError: f-string expression part cannot include '#'
```
```python
>>> # Python 3.12+
>>> f"""Storing employee's data: {
...     employee['name'].upper()  # Always uppercase name before storing
... }"""
"Storing employee's data: JOHN DOE"
```

---

## Better error messages (3.12)

```python
>>> # pre-Python 3.12
>>> f"{42 + }"
  File "<stdin>", line 1
    (42 + )
          ^
SyntaxError: f-string: invalid syntax
```
```python
>>> # Python 3.12
>>> f"{42 + }"
  File "<stdin>", line 1
    f"{42 + }"
          ^
SyntaxError: f-string: expecting '=', or '!', or ':', or '}'
```

---

# When f-strings are *not* the best tool

F-strings are awesome, but not universal:

1. Dictionary interpolation can get cluttered
2. Logging prefers lazy formatting
3. SQL queries should not use string interpolation
4. Internationalization/localization often favors templates + `.format()`

Let’s look at each quickly.

???
- Key theme: readability and correctness/safety beat “modern syntax” every time.
- It’s not “f-strings everywhere,” it’s “pick the right tool.”

---

# Dictionary interpolation: readability tradeoff

This works, but can look busy:

```python
person = {"name": "Avery", "age": 29}
msg = f"{person['name']} is {person['age']}"
```

Often cleaner with `.format(**dict)`:

```python
msg = "{name} is {age}".format(**person)
```

Or `%` with named fields:

```python
msg = "%(name)s is %(age)s" % person
```

???
- With lots of keys, f-strings can become a wall of `person[...]`.
- `.format(**person)` reads like a template and keeps the placeholders simple.

---

# Logging: f-strings defeat lazy evaluation

Python’s `logging` module can defer formatting until the message is actually emitted.

Preferred pattern:

```python
import logging
logging.debug("User id: %s", user_id)
```

Avoid (eager formatting even if debug is disabled):

```python
logging.debug(f"User id: {user_id}")
logging.debug("User id: {}".format(user_id))
```

???
- This can be a real performance issue inside loops.
- The logger decides whether to interpolate based on level; f-strings compute immediately.

---

# SQL queries: don’t interpolate (SQL injection risk)

Bad (string interpolation of parameters):

```python
query = f"SELECT * FROM users WHERE role = '{role}'"
```

Good: use parameterized queries (example pattern):

```python
query = "SELECT * FROM users WHERE role = %s"
cursor.execute(query, (role,))
```

???
- The key is: pass parameters separately so the driver/database can handle escaping and typing.
- This applies regardless of whether you’d use `%`, `.format()`, or f-strings—avoid them all for dynamic SQL.

---

# Internationalization/localization (i18n/l10n)

When you need translatable string templates, `.format()` is often a better fit:

- You can store templates per language
- Then fill in values at runtime with consistent placeholder names

Conceptually:

```python
template = "{name} has {count} messages"
msg = template.format(name=name, count=count)
```

???
- Translators usually want stable placeholders, not embedded Python expressions.
- Template strings can live outside code (resource files), which fits `.format()` well.

---

# Wrap-up

- f-strings (Python 3.6+) = readable, concise, fast
- Same formatting power as `.format()` (mini-language)
- Python 3.12 removes major limitations (quotes, backslashes, comments, nesting, errors)
- Still use the right tool for logging, SQL, i18n, and some dict-heavy templates

???

- Encourage: adopt f-strings as default for application strings and user-facing messages.
- Remember exceptions: logging, SQL, and localization are the big ones.
- Q&A prompt: “Where in your codebase would f-strings simplify things the most?”
