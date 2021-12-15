"""
Provides library level metadata and constants.
"""

NAME: str = "redpandas"
VERSION: str = "1.3.1"


def version() -> str:
    """Returns the version number of this library."""
    return VERSION


def print_version() -> None:
    """Prints the version number of this library"""
    print(version())

