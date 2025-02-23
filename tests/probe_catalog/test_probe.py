"""Tests for probe.py module."""

from database360.probe_catalog.probe import probe_resource, HEADERS
import pytest
import requests
import time

def test_probe_resources_art_architecture(mocker):
    # Mock sleep to avoid delays in tests
    mocker.patch('time.sleep')
    
    # Mock responses for both the search and catalog pages
    mock_search_response = mocker.Mock()
    mock_search_response.text = '''
        <html>
            <body>
                <a href="/catalog/12345">Art &amp; Architecture Source</a>
            </body>
        </html>
    '''
    
    mock_catalog_response = mocker.Mock()
    mock_catalog_response.text = '''
        <html>
            <body>
                <a href="http://resolver.library.cornell.edu/misc/8910">Click here for Art & Architecture Source</a>
            </body>
        </html>
    '''
    
    mock_get = mocker.patch('requests.get')
    mock_get.side_effect = [mock_search_response, mock_catalog_response]
    
    # Test data
    catalog_search_url = "https://catalog.library.cornell.edu/catalog"
    resource = {
        'Database Name': 'Art & Architecture Source',
        'PURL': 'http://resolver.library.cornell.edu/misc/8910'
    }
    
    # Run the probe
    result = probe_resource(catalog_search_url, resource)
    
    # Verify the requests were made with the correct headers
    calls = mock_get.call_args_list
    assert len(calls) == 2
    for call in calls:
        assert 'Mozilla' in call.kwargs['headers']['User-Agent']
    
    # Verify the results
    assert result['Catalog URL Link'] == 'https://catalog.library.cornell.edu/catalog/12345'
    assert result['PURL Link Text'] == 'Click here for Art & Architecture Source'
