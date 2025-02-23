"""Functions for probing the catalog."""

import urllib.parse
import time
import re
from typing import Dict, List, Optional, Tuple, Pattern
import requests
from bs4 import BeautifulSoup

# Constants for rate limiting
DELAY_BETWEEN_REQUESTS = 2  # seconds between requests

# Headers for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

def probe_resource(catalog_search_url: str, resource: Dict, link_matcher: Optional[str] = None) -> Dict:
    """Probe the catalog for a single resource.

    Args:
        catalog_search_url: Base URL for the catalog search
        resource: Dictionary containing resource information including database name and PURL
        link_matcher: Optional regex pattern to match catalog links. If not provided, returns first matching link.

    Returns:
        Dictionary containing probe results (catalog link and PURL link text if found)
    """
    database_name = resource.get('database_name')
    purl = resource.get('purl')
    results = {}

    if not database_name:
        return results

    search_url = catalog_search_url + urllib.parse.quote(database_name)
    print(f"Searching: {search_url}")

    # Compile the regex pattern if provided
    link_pattern = re.compile(link_matcher) if link_matcher else None

    catalog_link = find_database_link(search_url, database_name, link_pattern)
    if catalog_link:
        results['catalog_url_link'] = catalog_link
        if purl:
            purl_link_text = find_purl_link_text(catalog_link, purl)
            if purl_link_text:
                results['purl_link_text'] = purl_link_text

    time.sleep(DELAY_BETWEEN_REQUESTS)
    return results

def find_database_link(search_url: str, database_name: str, link_pattern: Optional[Pattern] = None) -> Optional[str]:
    """Search the catalog page for a link matching the database name and pattern.

    Args:
        search_url: URL to search for the database
        database_name: Name of the database to look for
        link_pattern: Optional compiled regex pattern to match against links. If not provided, returns first matching link.

    Returns:
        URL of the catalog entry if found, None otherwise
    """
    try:
        response = requests.get(search_url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a'):
            href = link.get('href')
            if href and database_name.lower() in link.text.lower():
                # If we have a pattern, check if the href matches
                if link_pattern is None or link_pattern.search(href):
                    # Get the absolute URL
                    print(f"Found link: {href}")
                    return urllib.parse.urljoin(search_url, href)

    except requests.RequestException as e:
        print(f"Error searching for {database_name}: {e}")
        return None

def find_purl_link_text(catalog_url: str, purl: str) -> Optional[str]:
    """Find the link text for a PURL in a catalog page.

    Args:
        catalog_url: URL of the catalog page to search
        purl: PURL to look for

    Returns:
        Link text if found, None otherwise
    """
    try:
        response = requests.get(catalog_url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            if link.get('href') == purl:
                return link.text.strip()

    except requests.RequestException as e:
        print(f"Error finding PURL link text: {e}")
        return None
