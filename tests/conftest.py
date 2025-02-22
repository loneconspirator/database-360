"""Test configuration and fixtures for Database 360."""

import pytest
from pathlib import Path

@pytest.fixture
def config_file() -> str:
    """Return the path to the test configuration file."""
    return str(Path(__file__).parent.parent / 'institution_data' / 'Configuration.xlsx')
