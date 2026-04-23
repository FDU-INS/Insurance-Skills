"""Test basic package functionality."""

import patientsim


def test_version() -> None:
    """Test that the package version is defined."""
    assert hasattr(patientsim, "__version__")
    assert isinstance(patientsim.__version__, str)
    assert patientsim.__version__ == "2.1.0"
