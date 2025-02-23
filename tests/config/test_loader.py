"""Tests for configuration loader."""

import pytest
from database360.config.loader import ConfigurationLoader

def test_config_loader_initialization(config_file):
    """Test that the configuration loader can be initialized."""
    loader = ConfigurationLoader(config_file)
    assert loader.config_file.exists()

def test_catalog_search_url_exists(config_file):
    """Test that the institution configuration contains a catalog search URL key."""
    loader = ConfigurationLoader(config_file)
    config = loader.load_institution_config()
    
    assert 'catalog_search_url' in config, "Configuration must contain 'catalog_search_url' key"
    assert config['catalog_search_url'] is not None, "Catalog Search URL value should not be None"
    assert config['catalog_search_url'] == 'https://catalog.library.cornell.edu/catalog?utf8=%E2%9C%93&controller=catalog&action=index&search_field=title&q=', \
        "Catalog Search URL should match expected value"

def test_first_resource_record(config_file):
    """Test that the first record in Resources has the expected database name."""
    loader = ConfigurationLoader(config_file)
    records = loader.load_resources()
    
    assert len(records) > 0, "Resources should not be empty"
    first_record = records[0]
    assert 'database_name' in first_record, "First record should have 'database_name' field"
    assert first_record['database_name'] == 'ARTbibliographies Modern', \
        "First database should be 'ARTbibliographies Modern'"
