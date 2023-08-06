from shlex import join

from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand
from poetry_plugin_compose.composed_commands.sub_command_runner import (
    run_sub_command_sync,
)


class ComposedAddCommand(ComposedCommand):
    name = "add"
    description = "Add a dependency to every sub-packages"
    examples = [
        {
            "description": "add flake8 to every sub-packages",
            "output": "poetry compose add flake8",
        },
        {
            "description": "add flake8 to every subpackage where black is installed",
            "output": "poetry compose install -i black -- flake8",
        },
        {
            "description": "add flake8 as a dev dependency to every subpackage where black is installed",
            "output": "poetry compose install -i black -- flake8 --group-dev",
        },
    ]

    def run(self, args, package):
        self._write_line("Running add " + join(args) + " in " + package)
        return_code = run_sub_command_sync(["poetry", "add", *args], package)
        self.report_output(return_code)
        return return_code
