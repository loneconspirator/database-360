"""Main entry point for Database 360."""

from pathlib import Path
from database360.config.loader import ConfigurationLoader
from database360.probe_runner import ProbeRunner

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

    # Initialize and run probes
    probe_runner = ProbeRunner(institution_config)
    results = probe_runner.run_probes(resources)

    print("\nProbe Results:")
    for result in results:
        print(result)

    # Here you might want to save the results to a file
    return results

if __name__ == "__main__":
    main()
