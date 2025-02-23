"""Functions for probing PURLs and checking their content."""

import requests
from typing import Dict
import math

def probe_purl(resource: Dict) -> Dict:
    """Probe a PURL and check if it leads to a page containing specific text.

    Args:
        resource: Dictionary containing resource information including 'purl' and
                 'database_home_page_should_contain_text'

    Returns:
        Dictionary containing probe results. Will contain 'purl_led_to_database' key
        only if the comparison was actually made. Returns empty dict if arguments
        are missing or empty.
    """
    results = {}

    # Handle NaN values from pandas DataFrame
    purl = resource.get('purl', '')
    expected_text = resource.get('database_home_page_should_contain_text', '')

    # Convert NaN to empty string
    if isinstance(purl, float) and math.isnan(purl):
        purl = ''
    if isinstance(expected_text, float) and math.isnan(expected_text):
        expected_text = ''

    # Strip strings
    purl = str(purl).strip()
    expected_text = str(expected_text).strip()

    if not purl or not expected_text:
        return results

    try:
        # Use a session to handle redirects
        session = requests.Session()

        # Set headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        }

        # Make the request and follow redirects
        response = session.get(purl, headers=headers, allow_redirects=True, timeout=30)
        response.raise_for_status()

        # Check if the expected text is in the page content
        results['purl_led_to_database'] = expected_text.lower() in response.text.lower()

    except (requests.RequestException, Exception) as e:
        print(f"Error checking PURL {purl}: {str(e)}")
        results = {}

    return results
