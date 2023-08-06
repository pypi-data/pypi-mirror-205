import sys
from typing import List

from cleo.commands.command import Command
from cleo.io.inputs.argument import Argument
from cleo.io.io import IO

from poetry_plugin_compose.composed_command_list import ALL_COMPOSED_COMMAND_CLASSES
from poetry_plugin_compose.composed_commands.composed_command import ComposedCommand


class ComposeCommand(Command):
    name = "compose"
    arguments = [Argument(name="sub command", is_list=True)]
    sub_command_classes = ALL_COMPOSED_COMMAND_CLASSES
    sub_commands: List[ComposedCommand] = []
    _io: IO

    def __init__(self):
        super().__init__()
        self.usages = ["compose <sub-command>"]
        self.description = "Manage multiple packages from a single root"
        self._ignore_validation_errors = True

    def handle(self) -> int:
        self._build_sub_commands()
        subcommand_args = sys.argv[2:]
        if subcommand_args[0] in ["--help", "-h"]:
            self.__print_help()
            return 0
        for command in self.sub_commands:
            if command.match(subcommand_args):
                if len(subcommand_args) > 1 and subcommand_args[0] in ["--help", "-h"]:
                    command.print_help()
                    return 0
                else:
                    return_code = command.handle(subcommand_args)
                    if return_code > 0:
                        self._io.write_line(
                            "<error>At least one command failed</error>"
                        )
                    else:
                        self._io.write_line(
                            "<comment>Every command succeeded</comment>"
                        )
                    return return_code
        command_name = subcommand_args[0] if subcommand_args else ""
        self._io.write_line(
            "<error>" + "could not find command '" + command_name + "'</error>"
        )
        self.__print_help()
        return 1

    def _build_sub_commands(self):
        self.sub_commands = [command() for command in self.sub_command_classes]
        for command in self.sub_commands:
            command.set_io(self._io)

    def set_io(self, io: IO):
        self._io = io

    def __print_help(self):
        self._io.write_line("Available commands:")
        for command in self.sub_commands:
            self._io.write_line(
                "    <comment>" + command.name + "</comment>: " + command.description
            )


def compose_command_factory():
    return ComposeCommand()
