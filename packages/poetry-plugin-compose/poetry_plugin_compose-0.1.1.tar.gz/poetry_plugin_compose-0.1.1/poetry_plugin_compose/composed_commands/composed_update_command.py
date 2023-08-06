from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand
from poetry_plugin_compose.composed_commands.sub_command_runner import (
    run_sub_command_sync,
)


class ComposedUpdateCommand(ComposedCommand):
    name = "update"
    description = "Updates dependencies in every sub-packages"
    examples = [
        {
            "description": "run poetry update in every sub-package",
            "output": "poetry compose update",
        },
        {
            "description": "run poetry update in the integration_test package",
            "output": "poetry compose update -d integration_test --",
        },
    ]

    def run(self, args, package):
        self._write_line("Running update in " + " in " + package)
        return_code = run_sub_command_sync(["poetry", "update", *args], package)
        self.report_output(return_code)
        return return_code
