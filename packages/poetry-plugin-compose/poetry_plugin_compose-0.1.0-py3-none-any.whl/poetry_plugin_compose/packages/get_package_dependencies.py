import os
from dataclasses import dataclass

import tomli


@dataclass
class Dependency:
    name: str
    is_local: bool
    local_path: str


def get_package_dependencies(package: str):
    with open(os.path.join(package, "pyproject.toml"), "rb") as f:
        pyproject = tomli.load(f)
        values = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", [])
        dependencies = []
        for name, attrs in values.items():
            if isinstance(attrs, dict) and attrs.get("path"):
                dependencies.append(
                    Dependency(name=name, is_local=True, local_path=attrs.get("path"))
                )
            else:
                dependencies.append(
                    Dependency(name=name, is_local=False, local_path="")
                )
        return dependencies
