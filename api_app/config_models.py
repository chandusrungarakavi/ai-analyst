from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Model for individual agent configuration."""

    model: str = Field(..., description="The model to use for this agent")
    name: str = Field(..., description="Name of the agent")
    description: str = Field(..., description="Description of the agent's purpose")
    instruction: str = Field(..., description="Instructions for the agent's behavior")
    tools: Optional[List[str]] = Field(
        default=[], description="List of tool names available to this agent"
    )


class RootConfig(BaseModel):
    """Root configuration model."""

    model: str = Field(..., description="Default model for all agents")
    tools: Dict[str, str] = Field(
        default_factory=dict, description="Map of tool names to their implementations"
    )
    agents: Dict[str, AgentConfig] = Field(
        ..., description="Map of agent names to their configurations"
    )

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "model": "gemini-2.5-flash",
                "tools": {"google_search": "google_search"},
                "agents": {
                    "benchmark_agent": {
                        "model": "gemini-2.5-flash",
                        "name": "benchmark_agent",
                        "description": "Benchmarks startups against sector peers",
                        "instruction": "Given the startup, analyze and benchmark...",
                        "tools": ["google_search"],
                    }
                },
            }
        }
