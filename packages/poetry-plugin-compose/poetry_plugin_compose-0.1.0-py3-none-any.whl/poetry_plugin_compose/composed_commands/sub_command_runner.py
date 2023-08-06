import subprocess
from typing import List
from shlex import join


def run_sub_command_sync(command: List[str], root: str):
    completed = subprocess.call(join(command), cwd=root, shell=True)
    return completed


def run_sub_command_sync_silent(command: List[str], root: str):
    completed = subprocess.run(
        " ".join(command),
        cwd=root,
        shell=True,
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    return completed.returncode, completed.stdout, completed.stderr
