from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand
from poetry_plugin_compose.composed_commands.sub_command_runner import (
    run_sub_command_sync,
)


class ComposedPublishCommand(ComposedCommand):
    name = "publish"
    description = "Publish sub packages"
    examples = [
        {
            "description": "run poetry publish in every sub-package",
            "output": "poetry compose publish",
        },
        {
            "description": "run poetry publish in the integration_test package",
            "output": "poetry compose publish -d integration_test --",
        },
    ]

    def run(self, args, package):
        self._write_line("building " + package)
        return_code = run_sub_command_sync(["poetry", "publish", *args], package)
        self.report_output(return_code)
        return return_code
