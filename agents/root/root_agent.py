import os
from typing import Dict, Any
import requests
from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.tools import AgentTool, google_search


def load_config() -> Dict[str, Any]:
    """Load agent configurations from API."""
    api_url = os.getenv("API_URL", "http://localhost:8000")
    try:
        response = requests.get(f"{api_url}/config")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to load configuration from API: {str(e)}")


def get_tool_from_name(config: Dict[str, Any], tool_name: str) -> Any:
    """Get tool instance from tool name defined in config."""
    tools_map = {
        "google_search": google_search
        # Add more tool mappings here as needed
    }
    return tools_map.get(tool_name)


def create_agent_from_config(config: Dict[str, Any], name: str) -> Agent:
    """Create an agent instance from configuration."""
    agent_config = config.get("agents", {}).get(name)
    if not agent_config:
        raise ValueError(f"Configuration for agent '{name}' not found")

    # Get tools from configuration
    tools = []
    tool_names = agent_config.get("tools", [])
    for tool_name in tool_names:
        tool = get_tool_from_name(config, tool_name)
        if tool:
            tools.append(tool)

    return Agent(
        model=agent_config.get("model"),
        name=agent_config.get("name"),
        description=agent_config.get("description"),
        instruction=agent_config.get("instruction"),
        tools=tools,
    )


# Load configuration
config = load_config()

# Create sub-agents and their tools dynamically
agents = {}
agent_tools = {}

# Create all agents except root agent
for agent_name, agent_config in config.get("agents", {}).items():
    if agent_name != "root_agent":
        agents[agent_name] = create_agent_from_config(config, agent_name)
        agent_tools[agent_name] = AgentTool(agent=agents[agent_name])

# Get root agent configuration
root_config = config.get("agents", {}).get("root_agent", {})

# Create root agent with all tools
root_agent = LlmAgent(
    model=root_config.get("model"),
    name=root_config.get("name"),
    description=root_config.get("description"),
    instruction=root_config.get("instruction"),
    tools=list(agent_tools.values()),
)
