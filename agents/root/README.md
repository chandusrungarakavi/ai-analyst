# AI Analyst Agent Configuration

## Overview

The AI Analyst system uses a configuration-driven approach with configurations managed by the API service. All agent configurations are stored in the API's `config.json` file and served through a REST endpoint.

## Overview

The AI Analyst system uses a configuration-driven approach to define and create agents. All agent configurations are stored in `config.json`, making it easy to modify agent parameters without changing the code.

## Configuration File Structure

The configuration file (`config.json`) contains settings for all agents in the system:

```json
{
  "model": "default-model-name",
  "agents": {
    "agent_name": {
      "model": "model-name",
      "name": "agent-name",
      "description": "agent-description",
      "instruction": "agent-instruction"
    }
    // ... other agents
  }
}
```

## Available Agents

1. benchmark_agent: Analyzes and benchmarks startups
2. deal_notes_agent: Processes documents and generates deal notes
3. recommendation_agent: Provides investment recommendations
4. root_agent: Coordinates between specialized agents

## Modifying Agent Configuration

Agent configurations can be modified through the API endpoints:

### 1. View Current Configuration

```bash
GET http://localhost:8000/config

Response:
{
    "model": "gemini-2.5-flash",
    "agents": {
        "benchmark_agent": {
            "model": "gemini-2.5-flash",
            "name": "benchmark_agent",
            "description": "...",
            "instruction": "..."
        },
        ...
    }
}
```

### 2. Update Configuration

```bash
PUT http://localhost:8000/config
Content-Type: application/json

# Request Body: Updated configuration object
{
    "model": "gemini-2.5-flash",
    "agents": {
        ...
    }
}

# Response
{
    "message": "Configuration updated successfully"
}
```

Changes made through the API are immediately reflected in the configuration file and will be picked up by new agent instances.

## Adding New Agents

To add a new agent:

1. Add a new configuration object in `config.json`
2. Update the root_agent.py to create and integrate the new agent
3. Add any necessary tools or dependencies

## Error Handling

The system includes validation for:

- Missing configuration file
- Invalid JSON format
- Missing agent configurations

## Notes

- Keep sensitive information out of the configuration
- Test configuration changes in a development environment first
- Always validate configuration JSON before updating
- Consider using environment variables for the API URL
- The API endpoint is secured by default - ensure proper authentication in production
- Backup configurations before making major changes

## Environment Variables

- `API_URL`: The URL of the configuration API (default: "http://localhost:8000")

Example:

```bash
export API_URL=http://api.example.com
# or on Windows
set API_URL=http://api.example.com
```
