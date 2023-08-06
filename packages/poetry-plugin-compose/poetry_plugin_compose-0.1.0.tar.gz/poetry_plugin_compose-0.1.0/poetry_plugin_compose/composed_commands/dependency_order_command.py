from typing import List

from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand
from poetry_plugin_compose.packages.build_dependency_graph import build_dependency_graph
from poetry_plugin_compose.toposort.graph import CircularGraphException


class DependencyOrderCommand(ComposedCommand):
    name = "dependency-order"
    description = "Find dependency order between packages"
    examples = [
        {
            "description": "get a valid dependency order of every sub package",
            "output": "poetry compose dependency-order",
        }
    ]

    def handle(self, args: List[str]):
        try:
            order, _ = build_dependency_graph()
            self._write_line(", ".join(order))
        except CircularGraphException as e:
            self._write_error(str(e))
            return 1
        return 0

    def run(self, args, package):
        pass
