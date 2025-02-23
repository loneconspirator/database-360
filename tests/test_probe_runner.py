"""Tests for probe runner."""

import pytest
from unittest.mock import patch
from database360.probe_runner import ProbeRunner

def test_probe_runner_initialization():
    """Test that ProbeRunner initializes correctly."""
    institution_config = {'catalog_search_url': 'http://example.com'}
    runner = ProbeRunner(institution_config)
    assert runner.institution_config == institution_config
    assert runner.results == []

@patch('database360.probe_runner.probe_resource')
def test_probe_runner_with_custom_link_matcher(mock_probe_resource, mocker):
    """Test that ProbeRunner uses custom link matcher from institution config."""
    # Set up mock return value
    mock_probe_resource.return_value = {'catalog_url_link': 'http://example.com/catalog/123'}

    # Create ProbeRunner with custom link matcher
    institution_config = {
        'catalog_search_url': 'http://example.com',
        'valid_catalog_links_match': r'/custom/pattern/'
    }
    runner = ProbeRunner(institution_config)

    # Run probe
    resource = {'database_name': 'Test DB'}
    results = runner.run_probes([resource])

    # Verify probe_resource was called with correct arguments
    mock_probe_resource.assert_called_once_with(
        'http://example.com',
        resource,
        link_matcher=r'/custom/pattern/'
    )

    # Verify results
    assert len(results) == 1
    assert results[0]['database_name'] == 'Test DB'
    assert results[0]['catalog_probe'] == {'catalog_url_link': 'http://example.com/catalog/123'}

@patch('database360.probe_runner.probe_resource')
def test_probe_runner_without_link_matcher(mock_probe_resource, mocker):
    """Test that ProbeRunner works without link matcher in config."""
    # Set up mock return value
    mock_probe_resource.return_value = {'catalog_url_link': 'http://example.com/catalog/123'}

    # Create ProbeRunner without link matcher
    institution_config = {'catalog_search_url': 'http://example.com'}
    runner = ProbeRunner(institution_config)

    # Run probe
    resource = {'database_name': 'Test DB'}
    results = runner.run_probes([resource])

    # Verify probe_resource was called with correct arguments
    mock_probe_resource.assert_called_once_with(
        'http://example.com',
        resource,
        link_matcher=None
    )

    # Verify results
    assert len(results) == 1
    assert results[0]['database_name'] == 'Test DB'
    assert results[0]['catalog_probe'] == {'catalog_url_link': 'http://example.com/catalog/123'}

def test_run_probes():
    """Test that ProbeRunner can run probes on resources."""
    institution_config = {'catalog_search_url': 'http://example.com'}
    resources = [
        {'database_name': 'Test DB 1'},
        {'database_name': 'Test DB 2'}
    ]
    
    runner = ProbeRunner(institution_config)
    results = runner.run_probes(resources)
    
    assert len(results) == 2
    assert results[0]['database_name'] == 'Test DB 1'
    assert results[1]['database_name'] == 'Test DB 2'
    assert 'catalog_probe' in results[0]
    assert 'catalog_probe' in results[1]
