import os
from dataclasses import dataclass

import tomli


@dataclass
class PackageDescriptor:
    name: str
    dir: str
    dependencies: list


def get_package_descriptor(package: str):
    with open(os.path.join(package, "pyproject.toml"), "rb") as f:
        pyproject = tomli.load(f)
        name = pyproject.get("tool", {}).get("poetry", {}).get("name")
        return PackageDescriptor(name=name, dir=package, dependencies=[])
