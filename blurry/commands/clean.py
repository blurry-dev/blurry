import shutil

from rich import print

from blurry.settings import get_build_directory
from blurry.settings import update_settings


def clean_build_directory():
    """Removes the build directory for a clean build."""
    update_settings()
    build_directory = get_build_directory()

    try:
        shutil.rmtree(build_directory)
    except FileNotFoundError:
        pass

    print(f"Cleaned build directory: {build_directory} 🧹")
