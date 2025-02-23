"""Main module for Database 360."""

from typing import Dict, List
from database360.config.loader import ConfigurationLoader
from database360.probe_resources.probe_catalog import probe_resource

class ProbeRunner:
    """Manages and executes various probes on resources."""

    def __init__(self, institution_config: Dict[str, str]):
        """Initialize the ProbeRunner.

        Args:
            institution_config: Dictionary containing institution configuration
        """
        self.institution_config = institution_config
        self.results = []

    def run_probes(self, resources: List[Dict]) -> List[Dict]:
        """Run all probes on the provided resources.

        Args:
            resources: List of resource dictionaries to probe

        Returns:
            List of dictionaries containing probe results for each resource
        """
        self.results = []

        print("\nProbing resources...")
        for i, resource in enumerate(resources, 1):
            database_name = resource.get('database_name', 'Unknown')
            print(f"\nProcessing {i}/{len(resources)}: {database_name}")

            # Run catalog probe
            catalog_result = self._run_catalog_probe(resource)

            # Combine results
            resource_results = {
                'database_name': database_name,
                'catalog_probe': catalog_result
            }

            self.results.append(resource_results)

        return self.results

    def _run_catalog_probe(self, resource: Dict) -> Dict:
        """Run the catalog probe on a single resource.

        Args:
            resource: Resource dictionary to probe

        Returns:
            Dictionary containing catalog probe results
        """
        try:
            return probe_resource(self.institution_config['catalog_search_url'], resource)
        except Exception as e:
            print(f"Error in catalog probe for {resource.get('database_name', 'Unknown')}: {e}")
            return {'error': str(e)}

def main():
    """Main entry point for the application."""
    # Get configuration source
    config_source = "https://docs.google.com/spreadsheets/d/1VbcDF6cndXZVD186GqjV8qPabl6v3PQH/edit?gid=671040191#gid=671040191"

    # Initialize configuration loader
    config_loader = ConfigurationLoader(config_source)

    # Load configurations
    institution_config = config_loader.load_institution_config()
    resources = config_loader.load_resources()

    print("\nInstitution Configuration:")
    print(f"Catalog Search URL: {institution_config['catalog_search_url']}\n")

    print("Resources Configuration:")
    for resource in resources:
        print(resource)

    # Initialize and run probes
    probe_runner = ProbeRunner(institution_config)
    results = probe_runner.run_probes(resources)

    # Here you might want to save the results to a file
    return results

if __name__ == "__main__":
    main()
