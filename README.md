<p align="center">
  <img width="200" height="200" alt="gwrefpy" src="https://github.com/user-attachments/assets/4763ec7a-c703-414f-ba81-1520793f5f8d" style="display: block; margin: 0 auto" />
</p>

# gwrefpy

En python-implementering av Akvifärs referensmetod för att studera förändrade grundvattenförhållanden.

## Development

This project uses `uv` as the package manager. To set up the development environment:

```bash
# Install dependencies
uv sync

# Run tests
uv run python -m pytest tests/

# Run linter
uv run ruff check .

# Format code
uv run ruff format .

# Check formatting without making changes
uv run ruff format --check .
```

# Referenser

[Strandanger, A. "Akvifärs referensmetod för att studera förändrade grundvattenförhållanden", Svenska Geotekniska Föreningen, Sundbyberg, Sverige, SGF 2024:04. Tillgänglig: https://svenskageotekniskaforeningen.se/wp-content/uploads/Publikationer/SGF_Rapporter/2024_2_Akvifars_refmetod.pdf](https://svenskageotekniskaforeningen.se/wp-content/uploads/Publikationer/SGF_Rapporter/2024_2_Akvifars_refmetod.pdf)
