from poetry_plugin_compose.composed_commands.sub_command_runner import (
    run_sub_command_sync_silent,
)


def sub_package_has_dependency(package: str, dependency: str):
    return_code, stdout, stderr = run_sub_command_sync_silent(
        ["poetry", "show", dependency], package
    )
    return return_code == 0
