"""Configuration loader for Database 360."""

import pandas as pd
from typing import Dict, List
from pathlib import Path
import urllib.parse
import requests
import tempfile
import os
import re

class ConfigurationLoader:
    """Loads and manages configuration from Excel files or Google Sheets URLs."""
    
    @staticmethod
    def to_snake_case(text: str) -> str:
        """Convert a string to snake case.
        
        Args:
            text: String to convert
            
        Returns:
            Snake case version of the string
        """
        # First, convert to lowercase
        text = text.strip().lower()
        # Replace spaces and hyphens with underscores
        text = re.sub(r'[-\s]+', '_', text)
        # Remove any duplicate underscores
        text = re.sub(r'_+', '_', text)
        return text

    @staticmethod
    def convert_dict_keys_to_snake_case(d: Dict) -> Dict:
        """Convert all keys in a dictionary to snake case.
        
        Args:
            d: Dictionary to convert
            
        Returns:
            Dictionary with snake case keys
        """
        return {ConfigurationLoader.to_snake_case(k): v for k, v in d.items()}

    def __init__(self, config_source: str):
        """Initialize the configuration loader.
        
        Args:
            config_source: Path to the configuration Excel file or URL to a publicly accessible Google Sheet
        """
        self.config_source = config_source
        
        # Check if the source is a URL
        parsed = urllib.parse.urlparse(config_source)
        if parsed.scheme and parsed.netloc:  # It's a URL
            try:
                # If it's a Google Sheets URL, convert it to an export URL
                if 'docs.google.com' in parsed.netloc and '/spreadsheets/d/' in parsed.path:
                    # Extract the file ID
                    file_id = parsed.path.split('/d/')[1].split('/')[0]
                    config_source = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
                
                # Download the file to a temporary location
                response = requests.get(config_source)
                response.raise_for_status()
                
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
                temp_file.write(response.content)
                temp_file.close()
                
                self.config_file = Path(temp_file.name)
            except Exception as e:
                raise RuntimeError(f"Failed to download configuration from URL: {e}")
        else:  # It's a local file path
            self.config_file = Path(config_source)
            if not self.config_file.exists():
                raise FileNotFoundError(f"Configuration file not found: {config_source}")
    
    def __del__(self):
        """Cleanup temporary files if they exist."""
        # Check if we have a temporary file (URL case)
        if hasattr(self, 'config_file') and str(self.config_file).startswith(tempfile.gettempdir()):
            try:
                os.unlink(self.config_file)
            except:
                pass
    
    def load_institution_config(self) -> Dict[str, str]:
        """Load institution configuration from the Institution sheet.
        
        Returns:
            Dictionary with institution configuration key-value pairs with snake_case keys
        """
        try:
            df = pd.read_excel(self.config_file, sheet_name='Institution', usecols=[0, 1], engine='openpyxl')
            # Convert keys to snake case
            return {self.to_snake_case(key): value for key, value in zip(df.iloc[:, 0], df.iloc[:, 1])}
        except Exception as e:
            print(f"Error loading institution configuration: {e}")
            return {}
    
    def load_resources(self) -> List[Dict]:
        """Load resources configuration from the Resources sheet.
        
        Returns:
            List of dictionaries where each dictionary represents a resource record with snake_case keys
        """
        try:
            df = pd.read_excel(self.config_file, sheet_name='Resources', engine='openpyxl')
            records = df.to_dict('records')
            # Convert all keys to snake case
            return [self.convert_dict_keys_to_snake_case(record) for record in records]
        except Exception as e:
            print(f"Error loading resources configuration: {e}")
            return []
