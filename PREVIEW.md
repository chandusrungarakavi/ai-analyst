# How to Run the AI Analyst Agents with Docker Compose

1. **Build and Start the Service**

   Open a terminal in the project root and run:

   ```sh
   docker-compose up --build
   ```

   This will build the Docker image and start the agent service.

2. **Stop the Service**

   Press `Ctrl+C` in the terminal, or run:

   ```sh
   docker-compose down
   ```

3. **Live Code Updates**

   The `agents` folder and `req.txt` are mounted as volumes, so changes to these files on your host will be reflected in the running container.

4. **Custom Commands**

   To run a different agent or script, modify the `command` section in `docker-compose.yml` as needed.

---

---

**Access the ADK Web UI:**

Once the container is running, open your browser and go to:

```bash
http://127.0.0.1:8000
```

to check the ADK web UI.

For troubleshooting or advanced usage, refer to the Docker and Docker Compose documentation.
