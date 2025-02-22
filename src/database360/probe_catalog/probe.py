"""Functions for probing the catalog."""

import urllib.parse
from typing import Dict, List, Optional, Tuple
import requests
from bs4 import BeautifulSoup

def probe_resources(catalog_search_url: str, resources: List[Dict]) -> List[Dict]:
    """
    Probe the catalog for each resource, finding and following links that match database names.

    Args:
        catalog_search_url: Base URL for catalog searches
        resources: List of resource dictionaries containing database names

    Returns:
        List of resource dictionaries with additional catalog information
    """
    results = []
    for resource in resources:
        result = resource.copy()
        database_name = resource.get('Database Name')
        purl = resource.get('PURL')
        if not database_name:
            continue

        # Construct search URL
        encoded_name = urllib.parse.quote(database_name)
        search_url = f"{catalog_search_url}{encoded_name}"

        # First find the catalog link
        catalog_link = find_database_link(search_url, database_name)
        if catalog_link:
            result['catalog_link'] = catalog_link

            # Then follow the catalog link to find the PURL text
            if purl:
                purl_link_text = find_purl_link_text(catalog_link, purl)
                if purl_link_text:
                    result['catalog_purl_link_text'] = purl_link_text

        results.append(result)

    return results

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
        response = requests.get(search_url)
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
        response = requests.get(catalog_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for a link with the PURL as its href
        purl_link = soup.find('a', href=purl)
        if purl_link:
            return purl_link.text

    except requests.RequestException as e:
        print(f"Error following catalog link {catalog_url}: {e}")

    return None
