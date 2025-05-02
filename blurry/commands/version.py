import importlib.metadata
from rich import print


def print_blurry_version():
    """Prints the current Blurry version."""
    version = importlib.metadata.version("blurry-cli")

    print(f"v{version}")
