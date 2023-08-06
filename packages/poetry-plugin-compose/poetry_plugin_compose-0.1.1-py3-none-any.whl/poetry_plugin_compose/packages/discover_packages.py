import os
from typing import Callable


def is_directory_containing_file(directory: str, filename: str):
    content = os.listdir(directory)
    return filename in content


def is_poetry_project(directory: str):
    return is_directory_containing_file(directory, "pyproject.toml")


def discover_packages_matching(directory: str, filter_func: Callable[[str], bool]):
    stack = [directory]
    packages = []
    while stack:
        current = stack.pop()
        if current != directory and filter_func(current):
            packages.append(current)
        else:
            content = os.listdir(current)
            for file in [
                directory
                for directory in content
                if not directory.startswith(".")
                and os.path.isdir(os.path.join(current, directory))
            ]:
                stack.append(os.path.join(current, file))
    return packages


def discover_packages(directory):
    return discover_packages_matching(directory, is_poetry_project)
