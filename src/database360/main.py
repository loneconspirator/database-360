"""Main entry point for Database 360."""

from pathlib import Path
from database360.config.loader import ConfigurationLoader
from database360.probe_catalog.probe import probe_resource

def main():
    """Main entry point for the application."""
    # Get the project root directory (two levels up from this file)
    project_root = Path(__file__).parent.parent.parent
    # config_source = project_root / 'institution_data' / 'Configuration.xlsx'
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

    print("\nProbing catalog for resources...")
    probed_resources = []

    for i, resource in enumerate(resources, 1):
        database_name = resource.get('database_name', 'Unknown')
        print(f"\nProcessing {i}/{len(resources)}: {database_name}")

        probed_resource = probe_resource(institution_config['catalog_search_url'], resource)
        probed_resources.append(probed_resource)

    # Here you might want to save the probed_resources to a file
    return probed_resources

if __name__ == "__main__":
    main()
