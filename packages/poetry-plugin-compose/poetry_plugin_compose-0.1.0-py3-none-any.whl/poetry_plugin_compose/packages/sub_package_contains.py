import os


def sub_package_contains(package: str, file: str):
    content = os.listdir(package)
    return file in content
