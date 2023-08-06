from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand
from poetry_plugin_compose.composed_commands.sub_command_runner import (
    run_sub_command_sync,
)


class ComposedRunCommand(ComposedCommand):
    name = "run"
    description = "Run multiple commands in parallel"
    examples = [
        {
            "description": "run poetry run pytest in every sub-package",
            "output": "poetry compose run pytest",
        },
        {
            "description": "run pytest in every sub-package where it is installed",
            "output": "poetry compose run -i pytest -- pytest -s",
        },
    ]

    def run(self, args, package):
        self._write_line("running command " + " ".join(args) + " in " + package)
        return_code = run_sub_command_sync(["poetry", "run", *args], package)
        self.report_output(return_code)
        return return_code
