"""Tests for PURL probe."""

import pytest
import requests
from database360.probe_resources.probe_purl import probe_purl

def test_probe_purl_empty_resource():
    """Test probe_purl with empty resource."""
    resource = {}
    result = probe_purl(resource)
    assert isinstance(result, dict)
    assert result == {}

def test_probe_purl_empty_values():
    """Test probe_purl with empty string values."""
    resource = {
        'purl': '',
        'database_home_page_should_contain_text': ''
    }
    result = probe_purl(resource)
    assert result == {}

    resource = {
        'purl': '  ',  # whitespace only
        'database_home_page_should_contain_text': 'some text'
    }
    result = probe_purl(resource)
    assert result == {}

def test_probe_purl_missing_text():
    """Test probe_purl with missing expected text."""
    resource = {'purl': 'http://example.com'}
    result = probe_purl(resource)
    assert result == {}

def test_probe_purl_success(mocker):
    """Test probe_purl with successful match."""
    # Mock the requests session
    mock_session = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.text = 'Welcome to Test Database'
    mock_response.raise_for_status = mocker.Mock()
    mock_session.get.return_value = mock_response
    
    mocker.patch('requests.Session', return_value=mock_session)
    
    resource = {
        'purl': 'http://example.com/db',
        'database_home_page_should_contain_text': 'Test Database'
    }
    
    result = probe_purl(resource)
    assert result == {'purl_led_to_database': True}
    
    # Verify the request was made with correct parameters
    mock_session.get.assert_called_once_with(
        'http://example.com/db',
        headers=mocker.ANY,
        allow_redirects=True,
        timeout=30
    )

def test_probe_purl_no_match(mocker):
    """Test probe_purl with no text match."""
    # Mock the requests session
    mock_session = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.text = 'Different content'
    mock_response.raise_for_status = mocker.Mock()
    mock_session.get.return_value = mock_response
    
    mocker.patch('requests.Session', return_value=mock_session)
    
    resource = {
        'purl': 'http://example.com/db',
        'database_home_page_should_contain_text': 'Test Database'
    }
    
    result = probe_purl(resource)
    assert result == {'purl_led_to_database': False}

def test_probe_purl_request_error(mocker):
    """Test probe_purl with request error."""
    # Mock the requests session to raise an exception
    mock_session = mocker.Mock()
    mock_session.get.side_effect = requests.RequestException('Connection error')
    
    mocker.patch('requests.Session', return_value=mock_session)
    
    resource = {
        'purl': 'http://example.com/db',
        'database_home_page_should_contain_text': 'Test Database'
    }
    
    result = probe_purl(resource)
    assert result == {}
