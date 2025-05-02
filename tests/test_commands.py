import importlib.metadata
from blurry.commands.version import print_blurry_version


def test_print_blurry_version(capsys):
    expected_version = importlib.metadata.version("blurry-cli")
    print_blurry_version()
    captured = capsys.readouterr()
    assert captured.out == f"v{expected_version}\n"
