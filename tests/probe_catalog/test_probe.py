"""Tests for probe.py module."""

from database360.probe_catalog.probe import probe_resources
import pytest
import requests

def test_probe_resources_art_architecture(mocker):
    """Test probing resources finds the correct catalog link for Art & architecture source."""
    # Mock HTML content that would be returned by the search
    search_html = '''
    <html>
        <body>
            <div class="document">
                <h1>Search Results</h1>
                <div class="result">
                    <a href="/catalog/4417670">Art &amp; architecture source</a>
                    <p>Database for art research</p>
                </div>
            </div>
        </body>
    </html>
    '''
    
    # Mock HTML content that would be returned by the catalog page
    catalog_html = '''
    <html>
        <body>
            <div class="record">
                <h1>Art & architecture source</h1>
                <div class="holdings">
                    <a href="http://resolver.library.cornell.edu/misc/4417670">Available online</a>
                </div>
            </div>
        </body>
    </html>
    '''
    
    def mock_get(url):
        """Mock requests.get to return different responses based on URL."""
        response = mocker.Mock()
        response.raise_for_status.return_value = None
        
        if 'search_field=title' in url:
            response.text = search_html
        else:
            response.text = catalog_html
        return response
    
    # Mock the requests.get function
    mocker.patch('requests.get', side_effect=mock_get)
    
    # Test data
    catalog_search_url = 'https://catalog.library.cornell.edu/catalog?utf8=%E2%9C%93&controller=catalog&action=index&search_field=title&q='
    resources = [{
        'Database Name': 'Art & architecture source',
        'PURL': 'http://resolver.library.cornell.edu/misc/4417670'
    }]
    
    # Run the function
    results = probe_resources(catalog_search_url, resources)
    
    # Verify the results
    assert len(results) == 1
    result = results[0]
    
    # Check catalog link
    assert result['catalog_link'] == 'https://catalog.library.cornell.edu/catalog/4417670'
    
    # Check PURL link text
    assert result['catalog_purl_link_text'] == 'Available online'
    
    # Verify both requests were made
    assert requests.get.call_count == 2
    requests.get.assert_any_call(f"{catalog_search_url}Art%20%26%20architecture%20source")
    requests.get.assert_any_call('https://catalog.library.cornell.edu/catalog/4417670')
