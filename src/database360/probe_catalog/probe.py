"""Functions for probing the catalog."""

import urllib.parse
import time
from typing import Dict, List, Optional, Tuple
import requests
from bs4 import BeautifulSoup

# Constants for rate limiting
DELAY_BETWEEN_REQUESTS = 2  # seconds between requests

# Headers for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

def probe_resource(catalog_search_url: str, resource: Dict) -> Dict:
    """Probe the catalog for a single resource.

    Args:
        catalog_search_url: Base URL for the catalog search
        resource: Dictionary containing resource information including database name and PURL

    Returns:
        Updated resource dictionary with catalog link and PURL link text
    """
    database_name = resource.get('Database Name')
    purl = resource.get('PURL')

    if not database_name:
        return resource

    search_url = urllib.parse.urljoin(
        catalog_search_url,
        urllib.parse.quote(database_name)
    )

    catalog_link = find_database_link(search_url, database_name)
    if catalog_link:
        resource['Catalog URL Link'] = catalog_link
        if purl:
            purl_link_text = find_purl_link_text(catalog_link, purl)
            if purl_link_text:
                resource['PURL Link Text'] = purl_link_text

    time.sleep(DELAY_BETWEEN_REQUESTS)
    return resource

def find_database_link(search_url: str, database_name: str) -> Optional[str]:
    """
    Search the catalog page for a link matching the database name.

    Args:
        search_url: URL to search
        database_name: Name of the database to find

    Returns:
        URL of the matching link if found, None otherwise
    """
    try:
        response = requests.get(search_url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for links containing the database name
        for link in soup.find_all('a'):
            if database_name.lower() in link.text.lower():
                # Get the absolute URL
                return urllib.parse.urljoin(search_url, link.get('href'))

    except requests.RequestException as e:
        print(f"Error searching for {database_name}: {e}")

    return None

def find_purl_link_text(catalog_url: str, purl: str) -> Optional[str]:
    """
    Follow a catalog link and find the text of a link with the given PURL.

    Args:
        catalog_url: URL of the catalog page to check
        purl: PURL to look for in href attributes

    Returns:
        Text of the link if found, None otherwise
    """
    try:
        response = requests.get(catalog_url, headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for a link with the PURL as its href
        purl_link = soup.find('a', href=purl)
        if purl_link:
            return purl_link.text

    except requests.RequestException as e:
        print(f"Error following catalog link {catalog_url}: {e}")

    return None
