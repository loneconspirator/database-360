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
    database_name = resource.get('database_name')
    purl = resource.get('purl')
    results = {}

    if not database_name:
        return results

    search_url = catalog_search_url + urllib.parse.quote(database_name)
    print(f"Searching: {search_url}")

    catalog_link = find_database_link(search_url, database_name)
    if catalog_link:
        results['catalog_url_link'] = catalog_link
        if purl:
            purl_link_text = find_purl_link_text(catalog_link, purl)
            if purl_link_text:
                results['purl_link_text'] = purl_link_text

    time.sleep(DELAY_BETWEEN_REQUESTS)
    return results

def find_database_link(search_url: str, database_name: str) -> Optional[str]:
    """
    Search the catalog page for a link matching the database name.

    Args:
        search_url: URL to search for the database
        database_name: Name of the database to look for

    Returns:
        URL of the catalog entry if found, None otherwise
    """
    try:
        response = requests.get(search_url, headers=HEADERS)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and database_name.lower() in link.text.lower() and '/catalog/' in href:
                # Get the absolute URL
                print(f"Found link: {href}")
                return urllib.parse.urljoin(search_url, href)

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
