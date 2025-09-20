# How to Run the AI Analyst Agents and API App with Docker Compose

## 1. Build and Start All Services

Open a terminal in the project root and run:

```sh
docker-compose up --build
```

This will build all Docker images and start the following services:

- **ai-analyst-agent** (main agent)
- **api-app** (FastAPI app with PostgreSQL connection)
- **db** (PostgreSQL database)
- **pgadmin** (PostgreSQL web UI)

## 2. Stop All Services

Press `Ctrl+C` in the terminal, or run:

```sh
docker-compose down
```

## 3. Access the Services

- **Main Agent (ai-analyst-agent):**
  - [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API App:**
  - [http://127.0.0.1:8001/fetch](http://127.0.0.1:8001/fetch)
    - This endpoint connects to the PostgreSQL database and returns a sample result.
- **pgAdmin (PostgreSQL UI):**
  - [http://127.0.0.1:5050](http://127.0.0.1:5050)
    - Login with:
      - Email: `admin@admin.com`
      - Password: `admin`
    - To connect pgAdmin to your database:
      1. Click "Add New Server" in pgAdmin.
      2. Name: any name (e.g., `LocalDB`)
      3. Host: `db`
      4. Port: `5432`
      5. Username: `postgres`
      6. Password: `postgres`
      7. Save and connect. You can now browse and query your PostgreSQL data in the browser.

## 4. Live Code Updates

The following folders are mounted as volumes for live code updates:

- `agents` (for the main agent service)
- `api_app` (for the API app service)

Any changes you make to files in these folders on your host will be reflected in the running containers. This allows for rapid development and testing without rebuilding the images.

## 5. Custom Commands

To run a different agent or script, modify the `command` section in `docker-compose.yml` as needed.

---

**Note:** All dependencies should now be managed in the appropriate `requirements.txt` files for each service.

For troubleshooting or advanced usage, refer to the Docker and Docker Compose documentation.
