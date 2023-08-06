# Poetry compose

A poetry plugin to manage multiple project from a single root, a-la monorepo.

[Docs available here](https://maxlarue.github.io/poetry-plugin-compose/)

# Work in progress
This is a work in progress, you might find some bugs, some improvements and some annoyance.
Do not hesitate to report them through github issues.

## Getting started

Install plugin

```bash
poetry self add poetry-plugin-compose
```

Start linting all sub projects in a single line

```bash
poetry compose run flake8 .
```

or running pytest in every package that has it installed

```bash
poetry compose run -i pytest -- pytest -vvv
```

## Project layout
Poetry compose is intended to run in a flat setup where each subdirectory that contains a `pyproject.toml` 
file is considered a sub-project. Such as 
```
database
    __init__.py
    pyproject.toml
    database
        __init__.py
    tests
        __init__.py
users
    __init__.py
    pyproject.toml
    users
        __init__.py
    tests
        __init__.py
profiles
    __init__.py
    pyproject.toml
    profiles
        __init__.py
    tests
        __init__.py
posts
    __init__.py
    pyproject.toml
    posts
        __init__.py
    tests
        __init__.py
scripts
    run.sh
```
but poetry will recursively descend into every subdirectory, so you could have other setups such as
```
packages
    database
        __init__.py
        pyproject.toml
        database
            __init__.py
        tests
            __init__.py
    users
        __init__.py
        pyproject.toml
        users
            __init__.py
        tests
            __init__.py
    profiles
        __init__.py
        pyproject.toml
        profiles
            __init__.py
        tests
            __init__.py
    posts
        __init__.py
        pyproject.toml
        posts
            __init__.py
        tests
            __init__.py
scripts
    run.sh
```


## Dependencies

poetry compose supports finding dependency order of your packages and always compose commands in a valid order.
poetry compose does not support circular dependencies though, and you should avoid them between your packages.
You can find the computed dependency order using the following command:
```bash
   poetry compose dependency-order
```

## Linking two packages

the easiest way to link two sub packages is to cd into the dependent one and run the followng command:
```bash
cd profiles
poetry add -e ../users
```

## local development

The recommended way to run plugin as you develop them is to install them in editable mode through poetry's packaged pip executable.

Example:

```
/Users/macbook/Library/"Application Support"/pypoetry/venv/bin/pip install -e ../poetry_multi_package
```

### Documentation

Documentation is mostly generated from the command themselves.
Also the root readme of the project serves as the welcome page of the docs.
In order to sync the doc runs the following
```
cd scripts
poetry run python generate_doc.py
```

Then to deploy
```
poetry compose run -d doc -- mkdocs gh-deploy
```