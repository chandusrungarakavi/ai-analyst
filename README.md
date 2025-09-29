### Check out docs/ for the user guide

## Project Structure

- `agents/` - Contains all agents logic
- `adk-web/` - UI interface
- `docs/` - Documentation
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Docker Compose config
- `PREVIEW.md` - Run the app locally

### API
Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### UI
Install dependencies:
   ```sh
   npm i
   ```

## Configuration Management

The API provides endpoints to manage agent configurations:

1. Get Current Configuration

```bash
GET /config

Response:
{
    "model": "gemini-2.5-flash",
    "agents": {
        "benchmark_agent": { ... },
        "deal_notes_agent": { ... },
        ...
    }
}
```

## Development

- Add new agents in `agents/`.
- Update documentation in `docs/`.

---

For more details, see files in each directory.
