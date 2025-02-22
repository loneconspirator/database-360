# Database 360

A tool for managing and searching library database resources.

## Project Structure

```
database-360/
├── src/
│   └── database360/         # Main package
│       ├── config/          # Configuration management
│       │   └── loader.py    # Excel configuration loader
│       └── main.py          # Application entry point
├── tests/                   # Test directory
│   └── config/             # Configuration tests
├── institution_data/       # Institution-specific data
│   └── Configuration.xlsx  # Configuration spreadsheet
└── requirements.txt        # Project dependencies
```

## Development Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package in development mode:
```bash
pip install -e .
```

4. Run tests:
```bash
python -m pytest tests/
```

## Configuration

The application uses an Excel file (`institution_data/Configuration.xlsx`) with two sheets:

1. `Institution`: Contains institution-specific settings
   - First column: Setting name
   - Second column: Setting value

2. `Resources`: Contains database resource information
   - Each row represents a database resource
   - First row contains column headers
