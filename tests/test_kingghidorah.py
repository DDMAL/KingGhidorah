import pathlib
import re

from kingghidorah import __version__


def test_version():
  # Get current file, parent, parent (AKA from Root KD Dir) and get the file "pyproject.toml"
  with open(pathlib.Path(__file__).parent.parent / "pyproject.toml") as f:
    pattern = f"(?<=version = \")(.*?)(?=\")"
    release = re.findall(pattern, f.read(), re.DOTALL)[0]
    assert __version__ == release
