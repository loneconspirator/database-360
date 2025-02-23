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

def test_probe_resource_with_custom_matcher():
    """Test probe_resource with custom link matcher."""
    resource = {'database_name': 'Test DB'}
    catalog_url = 'http://example.com'

    # Test with a custom pattern that won't match anything
    result = probe_resource(catalog_url, resource, link_matcher=r'/custom/pattern/')
    assert result == {}

def test_probe_resource_no_matcher(mocker):
    """Test that probe_resource finds first link when no matcher is provided."""
    # Mock responses for both the search and catalog pages
    mock_search_response = mocker.Mock()
    mock_search_response.text = '''
        <html>
            <body>
                <a href="/other/link">Art &amp; Architecture Source</a>
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

    # Mock requests.get
    mock_get = mocker.patch('requests.get')
    mock_get.side_effect = [mock_search_response, mock_catalog_response]

    # Test data
    catalog_search_url = "https://catalog.library.cornell.edu/catalog"
    resource = {
        'database_name': 'Art & Architecture Source',
        'purl': 'http://resolver.library.cornell.edu/misc/8910'
    }

    # Run the probe with no matcher (should find first link)
    result = probe_resource(catalog_search_url, resource)
    assert result['catalog_url_link'] == 'https://catalog.library.cornell.edu/other/link'
    assert result['purl_link_text'] == 'Click here for Art & Architecture Source'

    # Verify the requests were made with the correct headers
    calls = mock_get.call_args_list
    assert len(calls) == 2  # One call for search, one for PURL
    assert all(call.kwargs.get('headers') == HEADERS for call in calls)

def test_probe_resources_art_architecture(mocker):
    # Mock sleep to avoid delays in tests
    mocker.patch('time.sleep')

    # Mock responses for both the search and catalog pages
    mock_search_response = mocker.Mock()
    mock_search_response.text = '''
        <html>
            <body>
                <a href="/other/link">Art &amp; Architecture Source</a>
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

    # Run the probe with default matcher (should find /catalog/ link)
    result = probe_resource(catalog_search_url, resource, link_matcher=r'/catalog/')
    assert result['catalog_url_link'] == 'https://catalog.library.cornell.edu/catalog/12345'
    assert result['purl_link_text'] == 'Click here for Art & Architecture Source'

    # Reset mocks
    mock_get.reset_mock()
    mock_get.side_effect = [mock_search_response, mock_catalog_response]

    # Run the probe with custom matcher (should find /other/link)
    result = probe_resource(catalog_search_url, resource, link_matcher=r'/other/')
    assert result['catalog_url_link'] == 'https://catalog.library.cornell.edu/other/link'
    assert result['purl_link_text'] == 'Click here for Art & Architecture Source'

    # Verify the requests were made with the correct headers
    calls = mock_get.call_args_list
    assert len(calls) == 2  # One call for search, one for PURL
    assert all(call.kwargs.get('headers') == HEADERS for call in calls)
