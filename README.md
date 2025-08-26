<p align="center">
  <img width="200" height="200" alt="gwrefpy" src="https://github.com/user-attachments/assets/4763ec7a-c703-414f-ba81-1520793f5f8d" style="display: block; margin: 0 auto" />
</p>

# gwrefpy

A Python implementation of the Akvifär reference method for detecting deviations in groundwater level time series.

## Overview

`gwrefpy` provides tools for analyzing groundwater monitoring data to identify changes in groundwater conditions using statistical methods. The package implements the Akvifär reference method, which enables detection of deviations in groundwater level time series through systematic analysis of monitoring well data.

### Key Features

- **Well Data Management**: Comprehensive handling of groundwater monitoring well data with time series support
- **Statistical Analysis**: Built-in linear regression and trend analysis capabilities
- **Data Persistence**: Custom `.gwref` file format for saving and loading well data
- **Time Series Support**: Flexible time representation supporting both datetime and float formats
- **Extensible Design**: Modular architecture allowing for future enhancements

## Installation

### Using pip (Recommended)

Install the latest stable version from PyPI:

```bash
pip install gwrefpy
```

Update to the latest version:

```bash
pip install --upgrade gwrefpy
```

Uninstall the package:

```bash
pip uninstall gwrefpy
```

### Development Installation

For development work, clone the repository and install using `uv`:

```bash
git clone https://github.com/your-username/gwrefpy.git
cd gwrefpy
uv sync
uv pip install -e .
```

## Requirements

- Python ≥ 3.11
- pandas
- scipy

## Quick Start

```python
import gwrefpy as gr

# more to be added...
```

## Documentation

Read the docs at https://gwrefpy.readthedocs.io/

### API Reference

API docs available at https://gwrefpy.readthedocs.io/en/latest/api.html

### Examples

*[Comprehensive examples and tutorials to be added]*

## Testing

Run the test suite using pytest:

```bash
uv run python -m pytest tests/
```

## Development

### Building the Package

```bash
uv build
```

### Contributing

*[Contributing guidelines to be added]*

### Development Commands

- Install dependencies: `uv sync`
- Run tests: `uv run python -m pytest tests/`
- Build package: `uv build`
- Development install: `uv pip install -e .`

## Project Structure

```
gwrefpy/
├── src/gwrefpy/
│   ├── __init__.py          # Package initialization
│   ├── well.py              # Core WellBase class
│   ├── constants.py         # Default constants and styling
│   └── io/
│       ├── __init__.py
│       └── io.py           # File I/O operations
├── tests/
│   ├── __init__.py
│   └── decorators.py       # Testing utilities
├── README.md
├── pyproject.toml
└── CLAUDE.md               # Development guidance
```

## Changelog

### Version 0.1.0

...

## License

*[License information to be added]*

## Support

*[Support and contact information to be added]*

## References

[Strandanger, A. "Akvifärs referensmetod för att studera förändrade grundvattenförhållanden", Svenska Geotekniska Föreningen, Sundbyberg, Sverige, SGF 2024:04.](https://svenskageotekniskaforeningen.se/wp-content/uploads/Publikationer/SGF_Rapporter/2024_2_Akvifars_refmetod.pdf)

## Acknowledgments

*[Acknowledgments to be added]*
