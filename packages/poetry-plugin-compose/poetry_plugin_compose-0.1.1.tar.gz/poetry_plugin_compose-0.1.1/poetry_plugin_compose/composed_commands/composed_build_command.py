from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand
from poetry_plugin_compose.composed_commands.sub_command_runner import (
    run_sub_command_sync,
)


class ComposedBuildCommand(ComposedCommand):
    name = "build"
    description = "Build sub packages"
    examples = [
        {
            "description": "run poetry build in every sub-package",
            "output": "poetry compose build",
        },
        {
            "description": "run poetry build in the integration_test package",
            "output": "poetry compose build -d integration_test --",
        },
    ]

    def run(self, args, package):
        self._write_line("building " + package)
        return_code = run_sub_command_sync(["poetry", "build", *args], package)
        self.report_output(return_code)
        return return_code
