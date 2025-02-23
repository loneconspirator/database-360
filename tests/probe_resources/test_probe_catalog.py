"""Tests for catalog probe."""

import pytest
import requests
import time
from database360.probe_resources.probe_catalog import probe_resource, HEADERS

def test_probe_resource():
    """Test that probe_resource returns expected results."""
    resource = {'database_name': 'Test DB'}
    catalog_url = 'http://example.com'
    
    result = probe_resource(catalog_url, resource)
    assert isinstance(result, dict)
    assert result == {}  # Should return empty dict for invalid URL

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
        'database_name': 'Art & Architecture Source',
        'purl': 'http://resolver.library.cornell.edu/misc/8910'
    }

    # Run the probe
    result = probe_resource(catalog_search_url, resource)

    # Verify the requests were made with the correct headers
    calls = mock_get.call_args_list
    assert len(calls) == 2
    assert all(call.kwargs.get('headers') == HEADERS for call in calls)

    # Verify the results
    assert result['catalog_url_link'] == 'https://catalog.library.cornell.edu/catalog/12345'
    assert result['purl_link_text'] == 'Click here for Art & Architecture Source'
