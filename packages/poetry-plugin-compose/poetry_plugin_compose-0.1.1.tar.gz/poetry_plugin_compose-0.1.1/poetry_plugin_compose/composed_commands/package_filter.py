from os import path
from poetry_plugin_compose.packages.sub_package_contains import (
    sub_package_contains,
)
from poetry_plugin_compose.packages.sub_package_has_dependency import (
    sub_package_has_dependency,
)


class PackageFilter:
    def filter(self, package):
        raise NotImplementedError()


class PackageHasDependencyFilter(PackageFilter):
    def __init__(self, dependency_name):
        self.dependency_name = dependency_name

    def filter(self, package):
        return (
            sub_package_has_dependency(package, self.dependency_name),
            f"package {package} does not have a dependency to {self.dependency_name}",
        )


class PackageIsDirectory(PackageFilter):
    def __init__(self, directory):
        self.directory = directory

    def filter(self, package):
        return (
            path.normpath(package) == path.normpath(self.directory),
            package + f" is not '{self.directory}'",
        )


class PackageContainsFileFilter(PackageFilter):
    def __init__(self, file_name):
        self.file_name = file_name

    def filter(self, package):
        return (
            sub_package_contains(package, self.file_name),
            f"package {package} does not contain file {self.file_name}",
        )
