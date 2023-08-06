import argparse
from typing import List, Dict

from cleo.io.io import IO

from poetry_plugin_compose.composed_commands.composed_command_utils import (
    split_compose_command_and_sub_command,
)
from poetry_plugin_compose.packages.build_dependency_graph import build_dependency_graph
from poetry_plugin_compose.composed_commands.package_filter import (
    PackageContainsFileFilter,
    PackageHasDependencyFilter,
    PackageIsDirectory,
)


class ComposedCommand:
    name: str
    io: IO
    parser: argparse.ArgumentParser
    description: str
    examples: List[Dict[str, str]] = []

    def __init__(self):
        self.parser = self.get_parser()

    def set_io(self, io: IO):
        self.io = io

    def match(self, args: List[str]):
        return args and args[0] == self.name

    def print_help(self):
        self.parser.print_help()

    def split_args(self, args: List[str]):
        return split_compose_command_and_sub_command(args)

    def handle(self, args: List[str]):
        root_command, sub_command = self.split_args(args)
        options = self.parser.parse_args(root_command[1:])
        filters = self._get_package_filters(options)
        package_order, package_map = build_dependency_graph()
        return_code = 0
        for package_name in package_order:
            package_dir = package_map[package_name].dir
            if self.filter_package(package_dir, filters):
                return_code += self.run(sub_command, package_dir)
        return return_code

    def run(self, args, package):
        raise NotImplementedError()

    def filter_package(self, package, filters):
        for filter in filters:
            can_run, msg = filter.filter(package)
            if not can_run:
                self._write_line(msg + " skipping")
                return False
        return True

    def report_output(self, return_code):
        if return_code > 0:
            self._write_failure()
        else:
            self._write_success()

    def get_log_intro(self):
        return f"[poetry compose {self.name}] "

    def _write_empty(self):
        self.io.write_line("")

    def _write_line(self, line: str):
        self.io.write_line("<info>" + self.get_log_intro() + line + "</info>")

    def _write_success(self):
        self.io.write_line("<comment>" + self.get_log_intro() + " success</comment>")

    def _write_error(self, error):
        self.io.write_line("<error>" + self.get_log_intro() + error + " failure</error>")

    def _write_failure(self):
        self._write_error("failure")

    def _get_package_filters(self, options):
        filters = []
        if options.contains:
            filters.append(PackageContainsFileFilter(options.contains))
        if options.ignore_missing:
            filters.append(PackageHasDependencyFilter(options.ignore_missing))
        if options.directory:
            filters.append(PackageIsDirectory(options.directory))
        return filters

    def get_parser(self):
        parser = argparse.ArgumentParser(
            prog="poetry compose " + self.name, description=self.description
        )
        parser.add_argument(
            "-i",
            "--ignore-missing",
            action="store",
            help="Only run in packages that have this dependency",
        )
        parser.add_argument(
            "-c",
            "--contains",
            action="store",
            help="Only run in packages that include this file",
        )
        parser.add_argument(
            "-d",
            "--directory",
            action="store",
            help="Only run in selected directory",
        )
        return parser
