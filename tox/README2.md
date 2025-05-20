name: title-slide
class: center middle

# All About Tox!
## Your Friendly Python Test Automation Buddy

???
*   **Welcome & Intro:** "Hey everyone, thanks for coming! Today we're diving into a tool that I think is a real game-changer for Python developers: Tox."
*   **Enthusiasm:** "If you've ever wrestled with making sure your Python code works in different environments, or just want to make your testing life easier, you're in the right place."
*   **Quick Hook:** "We'll see how Tox can be your little automation buddy, taking care of the tedious bits so you can focus on writing great code."
*   Make sure to update "[Your Name/Handle Here]".

---
name: what-is-tox
class:
## So, What's the Big Deal with Tox?

Ever found yourself saying (or hearing):
*   "Hmm, this code works on *my* machine..." 🤔
*   "Will this library work with Python 3.8? And 3.9? And 3.10? And 3.11? Oh my!" 🤯
*   "How do I make sure my linters and formatters run the same way for everyone?"
*   "Does my package actually... you know... *install* correctly?"

If yes, then Tox might just be your new best friend!

.footnote[The "it works on my machine" problem is classic!]

???
*   **Relate to Audience:** "Who here has ever uttered the infamous phrase 'Well, it works on MY machine'?" (Pause for nods/chuckles). "We've all been there, right?"
*   **Pain Points:** "These are common headaches. Managing different Python versions, ensuring consistent linting, or even just being confident your package installs cleanly can be a real drain."
*   **Tease the Solution:** "Tox is designed to tackle exactly these kinds of problems head-on."
*   **Elaborate on "install correctly":** "Sometimes we forget to list a dependency, or our `setup.py` / `pyproject.toml` has a typo. Tox helps catch this early!"

---
name: tox-to-the-rescue
## Tox to the Rescue!

Tox is a command-line tool that aims to **automate and standardize testing in Python**.

Think of it as a little robot that:
1.  Creates **isolated environments** (like little sandboxes).
2.  Installs your project and its **dependencies** into these sandboxes.
3.  Runs your **tests, linters, doc builders**, or whatever commands you tell it to!
4.  Does this for **multiple Python versions** or configurations.

It's all about .highlight[reproducibility] and .highlight[consistency]!

.footnote[Isolation is key! No more global package conflicts.]

???
*   **Clear Definition:** "So, what exactly IS Tox? At its heart, it's about automation and standardization for your Python testing workflows."
*   **Robot Analogy:** "I like to think of it as this diligent little robot. You give it a list of instructions, and it goes off and does the work for you, reliably, every single time."
*   **Emphasize Keywords:** "The big wins here are *reproducibility* and *consistency*. Everyone on the team, and your CI server, runs things the exact same way."
*   **Isolation is HUGE:** "And that 'isolated environments' bit? That's crucial. No more weird interactions with packages you installed globally three months ago for some other project."

---
name: key-superpowers
## Key Superpowers of Tox

<dl>
  <dt>Multi-Environment Testing</dt>
  <dd>Easily test against Python 3.7, 3.8, 3.9, 3.10, 3.11, PyPy, etc.</dd>

  <dt>Isolated Virtual Environments</dt>
  <dd>Each test run gets a fresh, clean environment.</dd>

  <dt>Dependency Management</dt>
  <dd>Manages test-specific dependencies separately.</dd>

  <dt>Standardized Commands</dt>
  <dd>Ensures everyone runs tests, linters, etc., the same way.</dd>

  <dt>Packaging Check</dt>
  <dd>Builds and installs your package, catching errors early.</dd>

  <dt>Versatile</dt>
  <dd>Not just for <code>pytest</code>. Run linters, formatters, doc builders, etc.</dd>
</dl>

.footnote[Imagine the time saved not manually setting up 5 Python versions!]

???
*   **Walk Through Superpowers:** "Let's break down what makes Tox so powerful."
*   **Multi-Environment:** "This is a big one. Want to support Python 3.8 through 3.12? Tox handles setting up environments for each."
*   **Isolation (Reiterate):** "Again, clean sandboxes every time. So important."
*   **Dependency Management:** "Your main project has its dependencies, but your tests might need `pytest`, `pytest-cov`, etc. Tox keeps these separate and clean."
*   **Packaging Check:** "This is often an unsung hero. Tox usually builds your package from source and installs it. If your `pyproject.toml` or `setup.py` is broken, you'll know *before* you try to publish!"
*   **Versatility:** "Don't just think 'pytest'. Think linters like Flake8 or Ruff, formatters like Black, even building your Sphinx documentation."

---
name: tox-ini
## The Configuration File: `tox.ini`

All of Tox's configuration lives in a single file, usually named `tox.ini`, placed in the root of your project.

It is an INI-style configuration file.

### Core Sections

<dl>
    <dt><code>[tox]</code></dt>
    <dd>Global settings for Tox itself.</dd>
    <dt><code>[testenv]</code></dt>
    <dd>Defines a base template for your test environments.</dd>
    <dt><code>[testenv:name]</code></dt>
    <dd>Defines a specific, named environment.</dd>
</dl>

Let's peek inside...

.footnote[`tox.ini` is the brain of the operation.]

???
*   **Central Config:** "So how do you tell Tox what to do? It all happens in one file: `tox.ini`."
*   **Location:** "You'll typically find this right in the root directory of your Python project."
*   **INI Format:** "It uses the INI format, which is pretty straightforward – sections in square brackets, key-value pairs. Easy to read, easy to write."
*   **Core Sections Intro:** "We'll look at the main sections you'll encounter. `[tox]` for global stuff, `[testenv]` as a general template, and then specific `[testenv:your-env-name]` sections."

---
name: tox-ini-example-global
## `tox.ini` - The `[tox]` Section

This section controls overall Tox behavior.
.columns[
.column[
```ini
[tox]
envlist =                         ; Default environments to run
    py3.9
    py3.10
    py3.11
    lint
    docs
isolated_build = True             ; Recommended! Builds your package in isolation.
skip_missing_interpreters = True  ; Don't fail if a Python version isn't found.
```
]
.column[
<dl>
    <dt><code>envlist</code></dt>
    <dd>The list of environments to run when you just type <code>tox</code>.</dd>
    <dt><code>isolated_build</code></dt>
    <dd>Builds your package in isolation first. Catches packaging issues!</dd>
    <dt><code>skip_missing_interpreters</code></dt>
    <dd>Skips envs if Python version isn't found.</dd>
</dl>
]
]

.footnote[`envlist` is your go-to list of tasks.]

???
*   **Global Settings:** "The `[tox]` section is for settings that apply to Tox itself, globally."
*   **`envlist`:** "This is key. It's the default list of environments that will run if you just type `tox` in your terminal. You can list Python versions, or custom tasks like 'lint' or 'docs'."
*   **`isolated_build = True`:** "Super important! This tells Tox to first build your package (like creating a wheel or sdist) in a clean, isolated environment *before* trying to install it into your test environments. This is how it catches packaging errors. It's on by default in newer Tox versions, and highly recommended."
*   **`skip_missing_interpreters = True`:** "This is a lifesaver. If your `envlist` says 'run on Python 3.7' but you don't have Python 3.7 installed locally, Tox will just politely skip it instead of erroring out. Great for when CI has all Pythons but you only have a couple."

---
name: tox-ini-example-testenv
## `tox.ini` - The `[testenv]` Section (The Blueprint)

This is like a base configuration or a template that specific environments can inherit from or override.

.columns[
.column[
```ini
[testenv]
description = Run tests with pytest
deps =
    pytest
    pytest-cov
commands =
    pytest {posargs} tests/
```
]
.column[
<dl>
    <dt><code>description</code></dt>
    <dd>Human-readable explanation.</dd>
    <dt><code>deps</code></dt>
    <dd>Dependencies for <i>this environment</i>.</dd>
    <dt><code>commands</code></dt>
    <dd>Actual commands to run. <code>{posargs}</code> passes command-line arguments.</dd>
</dl>
]
]

.footnote[`deps` are specific to *this* test environment, not your main project.]

???
*   **The Blueprint/Template:** "Think of `[testenv]` as your default blueprint. Settings here will apply to all your specific test environments unless they explicitly override them."
*   **`description`:** "Nice for humans. If you run `tox -av` (list environments), this description shows up."
*   **`deps`:** "These are the Python packages needed *for this test environment*. So, `pytest`, `pytest-cov`, maybe `mock` if you're on older Python. Tox will `pip install` these into the isolated virtual environment it creates just for this run. These are *not* your project's main dependencies."
*   **`commands`:** "This is what Tox will actually execute. Each line is a new command. Here, we're running `pytest`."
*   **`{posargs}`:** "This is a neat trick! It means 'pass through any arguments that were given on the command line after a `--`'. So you can run `tox -e py39 -- -k test_specific_function` and the `-k test_specific_function` part gets passed to pytest. Super useful for focused testing."

---
name: tox-ini-specific-envs
## `tox.ini` - Specific Environments `[testenv:name]`

Now we define actual, runnable environments.

.columns[
.column[
```ini
[testenv:py3.9]
description = Run tests with pytest on Python 3.9
# Inherits deps and commands from [testenv]
[testenv:py3.10]
description = Run tests with pytest on Python 3.10
[testenv:lint]
description = Run linters (flake8, black, ruff)
deps =
    flake8
    black
    ruff
commands =
    flake8 .
    black --check .
    ruff check .
```
]
.column[
*   `pyXX` convention tells Tox which Python interpreter to use.
*   The `lint` environment shows Tox isn't just for `pytest`.
]
]

.footnote[You can have as many named environments as you need!]

???
*   **Defining Specific Tasks:** "Okay, so we have the blueprint. Now let's define some actual environments we want to run."
*   **`[testenv:py39]` / `[testenv:py310]`:** "The `pyXX` naming convention is special. When Tox sees `py39`, it knows to look for a Python 3.9 interpreter. These environments will inherit the `deps` and `commands` from our main `[testenv]` section, unless we override them here."
*   **`[testenv:lint]` Example:** "This shows the versatility. We've created a completely separate environment called `lint`. It has its own dependencies – `flake8`, `black`, `ruff` – and its own commands to run these linters. It doesn't run pytest at all."
*   **Customization:** "You can have as many of these as you need: `docs`, `format`, `typecheck`, whatever!"

---
name: running-tox
## Running Tox: The Commands!

1.  **Install Tox**:
    ```bash
    pip install tox
    # or pipx install tox (recommended)
    ```

2.  **Run Tox**:
    *   `tox`
        *   runs `envlist`
    *   `tox -e py3.9`
        *   runs only `py3.9`
    *   `tox -e lint,docs`
        *   runs `lint` and `docs`
    *   `tox -r` or `tox --recreate`
        *   forces recreation of venvs
    *   `tox -av` or `tox list --verbose`
        *   lists environments
    *   `tox --notest`
        *   sets up envs, doesn't run commands

.footnote[Pro-tip: `pipx install tox` keeps it out of your project venvs.]

???
*   **Installation First:** "First things first, you need Tox installed. `pip install tox` works. I personally recommend `pipx install tox`. Pipx is great for installing Python command-line tools in their own isolated environments, so they don't clutter your global or project environments."
*   **Basic `tox` command:** "Just typing `tox` in your project root (where `tox.ini` lives) will run all the environments you listed in `envlist`."
*   **Specific Environments (`-e`):** "Use `-e` (for environment) to run specific ones. `tox -e py39`, or `tox -e lint,docs` for multiple."
*   **Recreate (`-r`):** "Sometimes things get weird, or you've changed dependencies in `tox.ini`. `tox -r` tells Tox to delete the old virtual environments and create them fresh. Good troubleshooting step."
*   **List Environments (`-av`):** "`tox -av` is handy to see all the environments defined in your `tox.ini` and their descriptions."
*   **`--notest`:** "This one's good for debugging your setup. It'll create the virtualenvs and install dependencies, but it *won't* run the actual `commands`. Lets you poke around in the `.tox` directory if needed."

---
name: how-it-works-simplified
## How It Works (A Simplified View)

When you run `tox -e py3.9`:

1.  **Parse `tox.ini`**.
2.  **Interpreter Check**: Looks for Python 3.9.
3.  **Create Virtual Environment**: In `.tox/py3.9/`.
4.  **Install Dependencies**:
    *   Installs `deps` from `tox.ini`.
    *   **Crucially**: If `isolated_build = True`, first builds your project (sdist/wheel) and installs *that*.
5.  **Run Commands**.
6.  **Report Results**.

All output and temp files go into `.tox/`.

.footnote[The `.tox` directory is where all the magic happens. It is safe to delete it.]

???
*   **Behind the Scenes:** "Let's quickly peek under the hood. What's Tox actually doing?"
*   **Step-by-step for `tox -e py39`:**
    1.  "Reads your `tox.ini`."
    2.  "Tries to find a Python 3.9 interpreter."
    3.  "Creates a brand new virtual environment, usually in a hidden directory called `.tox/py39/`."
    4.  "Installs dependencies: First, if `isolated_build` is on (and it should be!), it builds your actual project into a distributable format like a wheel. Then it installs that wheel AND any other dependencies listed in the `deps` for that environment into the new venv." (Emphasize this packaging check!)
    5.  "Runs the `commands` you specified."
    6.  "Tells you if it passed or failed."
*   **`.tox` directory:** "All this magic happens inside the `.tox` directory. You should definitely add `.tox/` to your `.gitignore` file because it's just temporary build artifacts and environments. You can safely delete it anytime; Tox will just recreate it."

---
name: why-bother
## Why Bother? The Glorious Payoffs!

*   **Confidence!** Know your code works across Python versions.
*   **Consistency!** Tests run the same for everyone and on CI/CD.
*   **Easier CI/CD**: Integrates beautifully with GitHub Actions, GitLab CI, etc.
*   **Cleaner Project**: Keeps test/lint dependencies out of main requirements.
*   **Early Bug Detection**: Catches version-specific or packaging issues early.
*   **Saves Time (Eventually!)**: Setup upfront saves debugging time later.

.footnote[Confidence is a beautiful thing for a developer.]

???
*   **The "Why":** "Okay, this sounds like a bit of setup. Why go through the trouble?"
*   **Confidence:** "This is HUGE. You can be much more confident that your library or application actually works as expected across all the Python versions you care about."
*   **Consistency:** "No more 'works on my machine.' If it passes in Tox, it should pass for your colleagues and on your CI server. This reduces so much friction."
*   **CI/CD Dream:** "Continuous Integration/Continuous Deployment systems LOVE Tox. You just tell your CI pipeline to run `tox`, and it does all the heavy lifting."
*   **Cleanliness:** "Your main project dependencies (`requirements.txt` or `pyproject.toml`) stay clean, only listing what your *application* needs to run, not what your *tests* or *linters* need."
*   **Early Detection:** "Find out that your code breaks on Python 3.8, or that your packaging is messed up, *before* you release it to the world."
*   **Time Saver:** "Yes, there's a small learning curve and setup time. But the amount of time and frustration it saves you in the long run by catching bugs early and standardizing your process is well worth it."

---
name: advanced-magic
## A Touch of Advanced Magic (Brief Mentions)

Tox can do even more cool stuff:

*   **Factoring Settings**: Use `[testenv]` and overrides.
*   **Environment Variables**: `setenv` for test runs.
*   **Passing Arguments**: `{posargs}`, `{envdir}`, etc.
*   **Depending on Other Environments**: `depends = otherenv`.
*   **Integration with `pyproject.toml`**.
*   **GitHub Actions Integration**: `[gh-actions]` section for auto-generating workflows!
*   **Parallel Mode**: `tox -p auto` for speed!

.footnote[Tox is surprisingly deep once you get into it!]

???
*   **Just Scratching the Surface:** "We've covered the basics, but Tox has a lot more up its sleeve for more complex scenarios."
*   **Briefly mention each:**
    *   "We saw factoring with `[testenv]`, but you can get quite sophisticated."
    *   "Need to set specific environment variables for a test run? Tox can do that."
    *   "More placeholders like `{posargs}` for dynamic command generation."
    *   "You can make one Tox environment depend on another finishing successfully."
    *   "Modern Tox can also pull some of its config from `pyproject.toml` if you're moving towards that standard."
    *   "The GitHub Actions integration is really slick. Tox can help generate your CI matrix for different Python versions automatically."
    *   "And for speed, `tox -p auto` can run your environments in parallel if they don't depend on each other. Big time saver for large test suites!"
*   **Encourage Exploration:** "Don't feel you need to learn all this at once, but it's good to know the power is there if you need it."

---
name: getting-started-summary
## Getting Started with Tox: Your Quick Guide

1.  **Install Tox**: `pip install tox` (or `pipx install tox`)
2.  **Create `tox.ini`** in project root.
3.  **Define `[tox]` section** (`envlist`, `isolated_build`).
4.  **Define `[testenv]` (base)** (`deps`, `commands`).
5.  **Define specific environments** (e.g., `[testenv:lint]`).
6.  **Run `tox`**!
7.  **Iterate and Refine**.
8.  **Add `.tox/` to `.gitignore`**!

.footnote[Start simple, then expand as your project grows.]

???
*   **Quick Recap:** "So, how do you actually get started today?"
*   **Walk through steps:**
    1.  "Install it."
    2.  "Create that `tox.ini` file."
    3.  "Set up your global `[tox]` section – `envlist` is the most important one to start."
    4.  "Create a base `[testenv]` with your common test dependencies (like `pytest`) and your main test command."
    5.  "If you have other tasks like linting, add specific environments like `[testenv:lint]`."
    6.  "Then, just run `tox` from your terminal in that directory."
    7.  "You'll probably tweak it as you go, and that's perfectly normal."
    8.  "And please, please, add `.tox/` to your `.gitignore`. You'll thank me later."
*   **Encouragement:** "Start simple. Even just one environment for your main Python version is a great first step."

---
name: speculation-corner
## Speculation Corner (Why isn't this built-in?)

You might wonder, "If Tox is so great, why isn't something like it part of Python's standard library?"

My best guess:
*   **Python's Philosophy**: Stdlib = lean, core building blocks. Tox is higher-level.
*   **Opinionated Nature**: Tox has its way (INI). Stdlib avoids being too prescriptive.
*   **Complexity & Scope**: Managing interpreters, venvs, packaging, commands is a lot.
*   **Pace of Development**: External tools iterate faster than stdlib.
*   **Alternatives Exist (Sort of)**: `nox` (Python-based config) offers similar features.

Tox's de facto standard status is a testament to its utility!

.footnote[It's like asking why Git isn't part of every OS. Specialization!]

???
*   **A Common Question:** "Sometimes people ask, if Tox is so useful, why isn't it just part of Python itself, like `venv` or `unittest`?"
*   **Offer Speculations (clearly state these are opinions/guesses):**
    *   "Python's standard library tends to be pretty lean and focused on providing the fundamental building blocks. Tox is more of an orchestration tool that sits on top of those."
    *   "Tox is also a bit opinionated – it uses INI files, it has its specific workflow. The standard library often tries to be less opinionated to allow for different approaches."
    *   "Frankly, what Tox does is *complex*. Managing all those interpreters, virtual environments, package building steps... it's a big job."
    *   "Tools in the wider ecosystem, like Tox, can develop and release new features much more quickly than something tied to Python's release cycle."
    *   "And there are other tools like `nox`, which uses Python files for configuration, that offer similar capabilities. The ecosystem provides choice."
*   **Positive Spin:** "The fact that Tox has become such a widely adopted, de facto standard in the community, even without being in the stdlib, really shows how valuable it is."

---
name: questions
class: center middle

# Questions? 🤔
## Let's Tox About It!

.big-text[Thanks for listening!]

.footnote[Check out the Tox docs: https://tox.wiki/]
