from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand
from poetry_plugin_compose.composed_commands.sub_command_runner import (
    run_sub_command_sync,
)


class ComposedCheckCommand(ComposedCommand):
    name = "check"
    description = "Run poetry check in sub-packages"
    examples = [
        {
            "description": "run poetry check in every sub-package",
            "output": "poetry compose check",
        },
        {
            "description": "run poetry check in the integration_test package",
            "output": "poetry compose check -d integration_test --",
        },
    ]

    def run(self, args, package):
        self._write_line("Checking " + package)
        return_code = run_sub_command_sync(["poetry", "check", *args], package)
        self.report_output(return_code)
        return return_code
