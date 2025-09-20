## Project Structure

- `agents/` - Contains all agent logic
  - `benchmark/` - Benchmark agent code
  - `root/` - Root agent code
- `api_app/` - API application (FastAPI, Flask, etc.)
- `tests/` - Unit and integration tests
- `docs/` - Documentation
- `requirements.txt` or `req.txt` - Python dependencies
- `requirements.txt` - Python dependencies for the entire project
- `docker-compose.yml` - Docker Compose config
- `PREVIEW.md` - Preview or project notes

## Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   pip install -r requirements.txt
   ```
2. Run the API app:
   ```sh
   cd api_app
   python main.py
   ```

## Development

- Add new agents in `agents/`.
- Add tests in `tests/`.
- Update documentation in `docs/`.

---

For more details, see files in each directory.
