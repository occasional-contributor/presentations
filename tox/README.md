name: tox-intro-presentation  
title: A Gentle Introduction to Tox  
description: Understanding Tox for Python project automation.  
class: center, middle

# A Gentle Introduction to Tox

### Your Python Project's Best Friend for Testing & Automation

???

Welcome everyone! Today, we're going to talk about a tool that, once you start using it, you'll wonder how you ever lived without it: Tox.
It's all about making your Python development life easier, especially when it comes to testing and ensuring your code works across different environments.
So, grab a coffee, and let's dive in!

---

## The "Before Tox" World: A Bit Chaotic?

Ever faced these situations?

*   "But it works on *my* machine!"
*   Manually creating and activating different virtual environments for Python 3.8, 3.9, 3.10...
*   Forgetting to run linters (like Flake8 or Black) before committing.
*   Tests passing locally, but failing in CI (Continuous Integration). Why?!
*   Ensuring your package installs correctly with its dependencies.
*   Wanting to test against different versions of a key library (e.g., Django 3.2 vs Django 4.0).

???

Let's set the stage. Think about the common headaches in Python development, especially as projects grow or when you're collaborating.
You've got different Python versions to support. Maybe your colleagues are on different operating systems.
You want to make sure your code is clean, well-formatted, and actually *works* everywhere it's supposed to.
Doing all this manually is tedious, error-prone, and frankly, no fun. We've all been there, right? That "works on my machine" is a classic for a reason!

---

## So, What Problem Does Tox Solve?

Tox aims to **standardize and automate testing in Python.**

It helps you:

1.  **Manage Virtual Environments:** Automatically creates isolated Python environments.
2.  **Test Across Configurations:** Easily test your code against:
    *   Different Python versions (e.g., 3.8, 3.9, 3.10, 3.11, 3.12).
    *   Different dependency sets (e.g., latest Django vs. older Django).
    *   Different test runners or tools (e.g., pytest, unittest, linters, documentation builders).
3.  **Ensure Reproducibility:** What runs in Tox locally should (ideally) run the same way in CI.
4.  **Package and Install Testing:** Checks if your package can be built and installed correctly.

It's like a conductor for your testing orchestra!

???

This is the core of it. Tox isn't a test runner itself; it's a *test environment manager and orchestrator*.
It handles the boring, repetitive, but crucial parts of setting up the right conditions to run your tests.
Imagine you need to support Python 3.8, 3.9, and 3.10. Tox will create three separate virtual environments, install your project and its dependencies into each, and then run your specified test commands in each one. All with a single command!
This drastically reduces the chances of surprises when your code hits different systems.

---

## The `tox.ini` File

Tox is configured using a simple INI-style file named `tox.ini` in your project's root directory.

Think of `tox.ini` as the **recipe book** for your project's testing and automation tasks.

It tells Tox:
*   Which Python versions to use.
*   What dependencies are needed for each testing environment.
*   What commands to run (e.g., run tests, lint code, build docs).

???

The heart of Tox is this `tox.ini` file. It's plain text, easy to read, and version-controllable, which is fantastic.
Once you set it up, anyone (including your CI server) can run `tox` and get the same consistent testing process.
We're going to spend a good chunk of time looking at how to read and write these files.

---

## Getting Started: Installation

If you don't have Tox, it's a simple pip install:

```bash
pip install tox
# or pipx install tox (recommended)
```

Once installed, you typically run it from your project's root directory (where `tox.ini` lives):

```bash
tox
```

.footnote[Pro-tip: `pipx install tox` keeps it out of your project venvs.]

???

Installation is straightforward. Most Python developers will be familiar with pip.
It's good practice to install it as a development dependency so that anyone cloning your project can easily set up the same testing environment.
When you run `tox` without any arguments, it will look for `tox.ini` and try to run all the environments defined in your `envlist` (we'll see that soon).

---

## Reading a `tox.ini` File: Key Sections

A `tox.ini` file is made up of sections, like `[section_name]`, followed by `key = value` pairs.

### Core Sections

.columns[
.column[
*  `[tox]`
    *   Global Tox settings.
    *   `envlist`: A comma-separated list of environments Tox should manage and run by default.
        *   Example: `envlist = py3.9, py3.10, lint`
    *   `isolated_build = True`: Modern way to build your package in isolation before testing. Highly recommended!

*  `[testenv]`
    *   Default settings for *all* test environments.
    *   Settings here can be overridden by specific environments.
    *   `deps`: Dependencies needed for testing (e.g., `pytest`, `flake8`).
    *   `commands`: The commands to execute (e.g., `pytest tests/`, `flake8 src/`).
]
.column[
*  `[testenv:name]` (e.g., `[testenv:py3.9]`, `[testenv:lint]`)
    *   Specific configuration for an environment named "name".
    *   It inherits from `[testenv]` and can override settings or add new ones.
    *   Often used to specify a particular Python interpreter via `basepython`.
        *   Example: `basepython = python3.9` for `[testenv:py3.9]`
]
]

???

Alright, let's start dissecting a `tox.ini`.
The `[tox]` section is like the global control panel. The `envlist` is super important – it tells Tox what environments you care about when you just type `tox`. `isolated_build` is a good practice ensuring your package builds cleanly before anything else happens.
The `[testenv]` section is your template. Define common stuff here.
Then, for each item in your `envlist` (like `py39` or `lint`), you'll usually have a corresponding `[testenv:py39]` or `[testenv:lint]` section. This is where you customize things for that specific environment, like telling `py39` to use the `python3.9` interpreter.

---

## Example 1: A Basic `tox.ini`

Let's say your project structure is:

```
my_project/
├── src/
│   └── my_package/
│       └── __init__.py
│       └── module.py
├── tests/
│   └── test_module.py
├── tox.ini
└── pyproject.toml
```

A simple `tox.ini` might look like this:

```ini
[tox]
envlist = py39, py310
isolated_build = True

[testenv]
deps =
    pytest
    # any other testing deps for your project
commands =
    pytest tests/
```

???

This is a pretty common starting point.
`envlist = py39, py310`: When you run `tox`, it will try to create two environments, one for Python 3.9 and one for Python 3.10. It will look for `python3.9` and `python3.10` on your system PATH.
`isolated_build = True`: Tox will first build a source distribution (sdist) and a wheel of your `my_project` in an isolated environment. This ensures your packaging setup is correct.
`[testenv]`: This applies to both `py39` and `py310` environments.
`deps = pytest`: In each virtual environment (for py39 and py310), Tox will install `pytest`. It will also install your project (`my_project`) itself!
`commands = pytest tests/`: After setting up the environment and installing dependencies, Tox will run the `pytest tests/` command.

If Python 3.9 isn't found as `python3.9` on the PATH, Tox might complain. We can be more specific using `basepython`.

---

## Example 1 Explained: What Happens?

When you run `tox`:

1.  Tox reads `tox.ini`.
2.  It sees `envlist = py3.9, py3.10`.
3.  **For `py3.9`:**
    *   Creates a new virtual environment (e.g., in `.tox/py3.9`). It tries to use an interpreter named `python3.9`.
    *   Builds your package (because of `isolated_build = True`).
    *   Installs your package and the dependencies from `[testenv]`'s `deps` (i.e., `pytest`) into `.tox/py3.9`.
    *   Runs `pytest tests/` inside the `.tox/py3.9` environment.
4.  **For `py3.10`:**
    *   Same process, but using an interpreter named `python3.10` and its own environment in `.tox/py3.10`.
5.  Reports the results for each environment.

All output, temporary files, and virtual environments are stored in a `.tox/` directory.

???

This step-by-step breakdown is crucial. Tox does a lot of work for you!
The `.tox` directory is where all the magic happens. It can get quite large if you have many environments, but it's self-contained.
And yes, definitely add `.tox/` to your `.gitignore` file – you don't want to commit virtual environments and build artifacts.
If `python3.9` or `python3.10` aren't directly available by those names on your system, Tox will fail to create the environment. This is where `basepython` in specific `[testenv:name]` sections becomes very useful.

---
## Writing Your Own `tox.ini`: Let's Build One!

Let's add more features:

*   Specify exact Python versions.
*   Add a linting step with Flake8.
*   Pass arguments to Pytest.

.columns[
.column[
```ini
[tox]
envlist =
    py3.8
    py3.9
    py3.10
    py3.11
    lint
isolated_build = True
[testenv]
# This section provides defaults for python test environments
# It's inherited by [testenv:py38], [testenv:py39], etc.
deps =
    pytest
    pytest-cov  # For code coverage
commands =
    pytest --cov=src --cov-report=term-missing tests/ {posargs}
# Specific Python versions
[testenv:py3.8]
basepython = python3.8
```
]
.column[
```ini
[testenv:py3.9]
basepython = python3.9
[testenv:py3.10]
basepython = python3.10
[testenv:py3.11]
basepython = python3.11
# Linting environment - doesn't need to install the package itself
[testenv:lint]
deps =
    flake8
    black
    isort
basepython = python3.9  # Or your preferred Python for linting
commands =
    flake8 src/ tests/
    black --check src/ tests/
    isort --check-only src/ tests/
```
]
]

???

Okay, now we're cooking!
`envlist` now includes Python 3.8 through 3.11, plus a `lint` environment.
In `[testenv]`, we've added `pytest-cov` to generate coverage reports.
The `commands` line is interesting: `pytest --cov=src --cov-report=term-missing tests/ {posargs}`.
`--cov=src` tells pytest-cov to measure coverage for code in the `src` directory.
`{posargs}` is a Tox substitution: any arguments you pass to `tox` *after* `--` will be inserted here. For example, `tox -e py39 -- -k "test_specific_feature"` would run only tests matching "test_specific_feature" in the py39 environment.
We added `basepython` for each Python version to be explicit. Tox will search for these specific executables.
The `[testenv:lint]` environment is separate. It has its own dependencies (`flake8`, `black`, `isort`). We don't need to install our main project package into the linting environment, so `skip_install = True` could be added here if needed (though often it's fine without if the commands don't depend on the package being importable). We also specify a `basepython` for linting, usually one of your supported Pythons.
The commands for linting check formatting and style.

---

## Key `tox.ini` Directives Deep Dive

*   `envlist = pyX, pyY, nameZ`: Defines environments.
*   `isolated_build = True`: Builds your package sdist/wheel in an isolated env first. Good.
*   `basepython = pythonX.Y`: Specifies the Python interpreter to use for an environment (e.g., `python3.9`). Tox searches your `PATH`.
*   `deps = ...`: List of dependencies to install in the venv. One per line, indented.
    *   Can include version specifiers: `pytest<8.0`
    *   Can point to local files: `-r requirements-dev.txt`
*   `commands = ...`: Commands to run. Executed sequentially. If one fails, the environment fails.
    *   `{posargs}`: Allows passing arguments from the `tox` command line to your test command.
        *   `tox -e py39 -- -k test_my_function`
    *   `{envdir}`: Path to the virtual environment directory (e.g., `.tox/py39`).
*   `changedir = my_subdir`: Changes directory before running commands. Default is project root.
*   `skip_install = True`: (In a `[testenv:...]` section) Don't install the current package into this test environment. Useful for linters or doc builders that don't need your package installed.

???

Let's zoom in on some of these directives.
`envlist` is your master list.
`isolated_build` is a modern best practice. Older Tox configs might not have it, or might have `sdist_mode = modern`.
`basepython` is key for ensuring you're using the right Python. If `python3.9` isn't on your PATH, that environment creation will fail.
`deps` is flexible. You can pin versions, or even tell Tox to install dependencies from a `requirements.txt` file.
`commands` are the heart of the execution. The `{posargs}` substitution is incredibly useful for focused testing. `tox -e py39 -- -v` would pass `-v` to pytest for verbose output.
`skip_install` is handy for environments like `lint` or `docs` where you're just running tools that don't need your actual package to be installed in their venv.
`changedir` can be useful if your test runner expects to be in a specific directory.

---

## Running Tox Commands

*   `tox`
    *   Runs all environments listed in `envlist`.
*   `tox -e py39`
    *   Runs only the `py39` environment.
*   `tox -e lint,docs`
    *   Runs only the `lint` and `docs` environments.
*   `tox --recreate` or `tox -r`
    *   Forces Tox to recreate the virtual environments instead of reusing existing ones. Useful if dependencies change or something seems broken.
*   `tox -e py310 -- -k "some_test_name" -v`
    *   Runs the `py310` environment.
    *   Passes `-k "some_test_name" -v` to the command specified in `tox.ini` (thanks to `{posargs}`).
*   `tox list` or `tox -l`
    *   Lists all available environments and their descriptions.

???

These are the commands you'll be typing most often.
`tox` is your daily driver.
`tox -e <envname>` is for focusing on a specific environment, great for debugging.
`tox -r` is your "turn it off and on again" for Tox environments. If things get weird, try recreating the environments.
Passing arguments with `--` and `{posargs}` is a superpower for developers.
`tox list` is good for remembering what environments you've defined, especially in complex projects.

---

## Why Bother? The Benefits Recap

*   **Consistency:** Same testing setup for everyone on the team and for CI.
*   **Confidence:** Know your code works across multiple Python versions/configurations.
*   **Automation:** Reduces manual, error-prone steps.
*   **Early Bug Detection:** Catch compatibility issues or packaging errors sooner.
*   **CI Friendly:** Tox is a staple in CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins, etc.).
*   **Clear Definition:** `tox.ini` clearly documents how to test your project.

???

So, why go through the effort of setting up a `tox.ini`?
It's all about making your life, your team's life, and your future self's life easier.
It brings a level of professionalism and robustness to your project.
When you see a `tox.ini` in a project, you know there's a defined way to test it, which is a huge plus for contributors and maintainers.

---

## Beyond the Basics (A Little Speculation & Further Learning)

Tox is powerful! What else *could* it do?

*   **Factor-conditional settings:** Change settings based on Python version or OS.
    *   `deps = pytest-windows-tools; platform_system == "Windows"`
*   **Matrix Expansion:** Define axes for environments (e.g., python version, django version) and Tox generates all combinations.
    *   `envlist = py{39,310}-django{32,40}`
*   **Documentation Building:** An environment to build your Sphinx docs.
    *   `[testenv:docs]` with `sphinx-build` command.
*   **Building Distributions:** An environment to build sdists and wheels.
    *   `[testenv:build]` with `python -m build` command.
*   **Plugins:** Tox has a plugin system!
    *   `tox-docker`: Run tests inside Docker containers.
    *   `tox-conda`: Use Conda environments instead of virtualenv.
    *   And many more!

If you're curious, the official Tox documentation is your best resource!

???

We've covered the essentials, but Tox can do much more.
Factor-conditional settings are neat for OS-specific dependencies or commands.
Matrix expansion is super powerful for libraries that need to test against multiple versions of other libraries (like Django or Flask).
You can basically automate any command-line task related to your project using a Tox environment. Building docs, creating releases, etc.
And plugins can extend Tox's capabilities even further. If there's something specific you need, there might be a plugin for it!
I'd really encourage you to check out the official docs if you want to go deeper.

---

class: center, middle

## Questions? 🤔

Thanks for listening!

???

Alright, that's the overview! Hopefully, this gives you a good starting point with Tox.
It might seem like a bit to set up initially, but the pay-off in terms of consistency and automation is well worth it.
Any questions?
