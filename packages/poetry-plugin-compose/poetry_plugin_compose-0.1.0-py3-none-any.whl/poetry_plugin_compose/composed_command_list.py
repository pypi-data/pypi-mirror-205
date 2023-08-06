from poetry_plugin_compose.composed_commands.composed_add_command import (
    ComposedAddCommand,
)
from poetry_plugin_compose.composed_commands.composed_build_command import (
    ComposedBuildCommand,
)
from poetry_plugin_compose.composed_commands.composed_check_command import (
    ComposedCheckCommand,
)
from poetry_plugin_compose.composed_commands.composed_install_command import (
    ComposedInstallCommand,
)
from poetry_plugin_compose.composed_commands.composed_lock_command import (
    ComposedLockCommand,
)
from poetry_plugin_compose.composed_commands.composed_publish_command import (
    ComposedPublishCommand,
)
from poetry_plugin_compose.composed_commands.composed_remove_command import (
    ComposedRemoveCommand,
)
from poetry_plugin_compose.composed_commands.composed_run_command import (
    ComposedRunCommand,
)
from poetry_plugin_compose.composed_commands.composed_update_command import (
    ComposedUpdateCommand,
)
from poetry_plugin_compose.composed_commands.dependency_order_command import (
    DependencyOrderCommand,
)

ALL_COMPOSED_COMMAND_CLASSES = [
    ComposedInstallCommand,
    ComposedAddCommand,
    ComposedBuildCommand,
    ComposedCheckCommand,
    ComposedLockCommand,
    ComposedPublishCommand,
    ComposedRemoveCommand,
    ComposedUpdateCommand,
    ComposedRunCommand,
    DependencyOrderCommand,
]
