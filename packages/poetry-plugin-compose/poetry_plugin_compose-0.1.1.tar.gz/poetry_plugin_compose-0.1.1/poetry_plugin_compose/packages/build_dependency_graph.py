from poetry_plugin_compose.packages.discover_packages import discover_packages
from poetry_plugin_compose.packages.get_package_dependencies import (
    get_package_dependencies,
)
from poetry_plugin_compose.packages.get_package_descriptor import get_package_descriptor
from poetry_plugin_compose.toposort.graph import Graph


def build_dependency_graph():
    graph = Graph(lambda it: it)
    packages = discover_packages(".")
    package_map = {}
    for package in packages:
        package_descriptor = get_package_descriptor(package)
        package_map[package_descriptor.name] = package_descriptor
        graph.add_node(package_descriptor.name)
    for package in packages:
        package_descriptor = get_package_descriptor(package)
        dependencies = get_package_dependencies(package)
        for dependency in dependencies:
            if graph.has_node(dependency.name):
                package_map[package_descriptor.name].dependencies.append(dependency)
                graph.add_edge(package_descriptor.name, dependency.name)
    return graph.toposort(), package_map
