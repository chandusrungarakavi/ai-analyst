# AI Analyst Agent Configuration

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

To modify an agent's behavior:

1. Open `config.json`
2. Locate the agent configuration under the "agents" object
3. Modify the desired parameters (model, description, instruction)
4. Save the file - changes will be applied when the system restarts

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

- Keep sensitive information out of the configuration file
- Backup the configuration file before making changes
- Test changes in a development environment first
