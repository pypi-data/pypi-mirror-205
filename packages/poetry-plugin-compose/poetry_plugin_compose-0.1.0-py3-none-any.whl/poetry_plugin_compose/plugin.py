import sys

from cleo.events.console_command_event import ConsoleCommandEvent
from cleo.events.console_events import COMMAND
from cleo.events.event_dispatcher import EventDispatcher
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_plugin_compose.compose_command import (
    compose_command_factory,
    ComposeCommand,
)


class MultiPackagePlugin(ApplicationPlugin):
    def activate(self, application):
        application.command_loader.register_factory("compose", compose_command_factory)
        application.event_dispatcher.add_listener(COMMAND, self.bootstrap, 100)

    def bootstrap(
        self, event: ConsoleCommandEvent, event_name: str, dispatcher: EventDispatcher
    ) -> None:
        if sys.argv[1] == "compose":
            event.disable_command()
            event.stop_propagation()
            command = ComposeCommand()
            command._io = event.io
            sys.exit(command.handle())
