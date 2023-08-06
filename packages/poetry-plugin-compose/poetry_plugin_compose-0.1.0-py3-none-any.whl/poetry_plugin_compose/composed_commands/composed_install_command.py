from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand
from poetry_plugin_compose.composed_commands.sub_command_runner import (
    run_sub_command_sync,
)


class ComposedInstallCommand(ComposedCommand):
    name = "install"
    description = "Run install in multiple sub-packages"
    examples = [
        {
            "description": "run poetry install in every sub-package",
            "output": "poetry compose install",
        },
        {
            "description": "run poetry install in the integration_test package",
            "output": "poetry compose install -d integration_test --",
        },
    ]

    def run(self, args, package):
        self._write_line("installing dependencies in " + " in " + package)
        return_code = run_sub_command_sync(["poetry", "install", *args], package)
        self.report_output(return_code)
        return return_code
