"""Main entry point for Database 360."""

from pathlib import Path
from database360.config.loader import ConfigurationLoader

def main():
    """Main entry point for the application."""
    # Get the project root directory (two levels up from this file)
    project_root = Path(__file__).parent.parent.parent
    config_file = project_root / 'institution_data' / 'Configuration.xlsx'
    
    # Initialize configuration loader
    loader = ConfigurationLoader(config_file)
    
    # Load institution configuration
    institution_config = loader.load_institution_config()
    print("\nInstitution Configuration:")
    for key, value in institution_config.items():
        print(f"{key}: {value}")
    
    # Load resources
    resources = loader.load_resources()
    print("\nResources Configuration:")
    for resource in resources:
        print(resource)

if __name__ == "__main__":
    main()
