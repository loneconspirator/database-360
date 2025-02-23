"""Tests for ProbeRunner."""

import pytest
from database360.main import ProbeRunner

def test_probe_runner_initialization():
    """Test that ProbeRunner can be initialized with institution config."""
    institution_config = {'catalog_search_url': 'http://example.com'}
    runner = ProbeRunner(institution_config)
    assert runner.institution_config == institution_config
    assert runner.results == []

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
