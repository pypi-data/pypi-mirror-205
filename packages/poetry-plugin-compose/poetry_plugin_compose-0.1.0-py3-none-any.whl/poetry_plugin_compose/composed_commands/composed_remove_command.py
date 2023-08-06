from shlex import join

from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand
from poetry_plugin_compose.composed_commands.sub_command_runner import (
    run_sub_command_sync,
)


class ComposedRemoveCommand(ComposedCommand):
    name = "remove"
    description = "Removes a dependency from every sub-packages"
    examples = [
        {
            "description": "remove flake8 from every sub-packages",
            "output": "poetry compose remove flake8",
        },
        {
            "description": "remove flake8 from every subpackage where black is installed",
            "output": "poetry compose install -i black -- flake8",
        },
        {
            "description": "remove flake8 as a dev dependency from every subpackage where black is installed",
            "output": "poetry compose install -i black -- flake8 --group-dev",
        },
    ]

    def run(self, args, package):
        self._write_line("Running remove " + join(args) + " in " + " in " + package)
        return_code = run_sub_command_sync(["poetry", "remove", *args], package)
        self.report_output(return_code)
        return return_code
