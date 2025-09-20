import json
import os
from typing import Dict, Any
from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.tools import AgentTool, google_search
from google.adk.tools import FunctionTool
from google.adk.agents.llm_agent import Agent
from vertexai import rag
import vertexai
from google.adk.tools import FunctionTool


RAG_LOCATION = "europe-west3"
RAG_NAME = "startup-pitch-decks"
RAG_ID = "4611686018427387904"
PROJECT_ID = "ai-analyst-for-startup-eval"
CORPUS_NAME = f"projects/{PROJECT_ID}/locations/{RAG_LOCATION}/ragCorpora/{RAG_ID}"


vertexai.init(project=PROJECT_ID, location=RAG_LOCATION)


def load_config() -> Dict[str, Any]:
    """Load agent configurations from local config.json file."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load configuration from config.json: {str(e)}")


def get_tool_from_name(config: Dict[str, Any], tool_name: str) -> Any:
    """Get tool instance from tool name defined in config."""
    tools_map = {
        "google_search": google_search,
        "query_rag_corpus": FunctionTool(query_rag_corpus),
        # Add more tool mappings here as needed
    }
    return tools_map.get(tool_name)


def query_rag_corpus(query_text: str):
    # Create the resource config
    rag_resource = rag.RagResource(rag_corpus=CORPUS_NAME)

    # Execute the query directly using the API
    response = rag.retrieval_query(
        rag_resources=[rag_resource],
        text=query_text,
    )
    return response.text if hasattr(response, "text") else str(response)


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
