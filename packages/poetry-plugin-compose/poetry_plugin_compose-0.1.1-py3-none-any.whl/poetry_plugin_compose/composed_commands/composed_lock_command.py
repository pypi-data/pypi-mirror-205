from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand
from poetry_plugin_compose.composed_commands.sub_command_runner import (
    run_sub_command_sync,
)


class ComposedLockCommand(ComposedCommand):
    name = "lock"
    description = "Lock sub packages"
    examples = [
        {
            "description": "run poetry lock in every sub-package",
            "output": "poetry compose lock",
        },
        {
            "description": "run poetry lock in the integration_test package",
            "output": "poetry compose lock -d integration_test --",
        },
    ]

    def run(self, args, package):
        self._write_line("building " + package)
        return_code = run_sub_command_sync(["poetry", "lock", *args], package)
        self.report_output(return_code)
        return return_code
