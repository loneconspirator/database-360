"""Configuration loader for Database 360."""

import pandas as pd
from typing import Dict, List
from pathlib import Path

class ConfigurationLoader:
    """Loads and manages configuration from Excel files."""
    
    def __init__(self, config_file: str):
        """Initialize the configuration loader.
        
        Args:
            config_file: Path to the configuration Excel file
        """
        self.config_file = Path(config_file)
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
    
    def load_institution_config(self) -> Dict[str, str]:
        """Load institution configuration from the Institution sheet.
        
        Returns:
            Dictionary with institution configuration key-value pairs
        """
        try:
            df = pd.read_excel(self.config_file, sheet_name='Institution', usecols=[0, 1])
            return dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        except Exception as e:
            print(f"Error loading institution configuration: {e}")
            return {}
    
    def load_resources(self) -> List[Dict]:
        """Load resources configuration from the Resources sheet.
        
        Returns:
            List of dictionaries where each dictionary represents a resource record
        """
        try:
            df = pd.read_excel(self.config_file, sheet_name='Resources')
            return df.to_dict('records')
        except Exception as e:
            print(f"Error loading resources configuration: {e}")
            return []
