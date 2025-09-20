from fastapi import FastAPI, HTTPException
import json
import os
from config_models import RootConfig
from typing import Dict, Any
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_config() -> RootConfig:
    """Load agent configurations from config.json file."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    try:
        with open(config_path, "r") as f:
            config_data = json.load(f)
            return RootConfig(**config_data)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Configuration file not found")
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500, detail="Invalid JSON in configuration file"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid configuration format: {str(e)}"
        )


# Database connection settings from environment variables
def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "postgres"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        host=os.getenv("POSTGRES_HOST", "db"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
    return conn


@app.get("/api/agent-config", response_model=RootConfig)
def get_config():
    """Get the agent configuration."""
    return load_config()


@app.put("/config", response_model=Dict[str, str])
async def update_config(config: RootConfig):
    """Update the agent configuration."""
    config_path = os.path.join(os.path.dirname(__file__), "agent_config.json")
    try:
        with open(config_path, "w") as f:
            json.dump(config.model_dump(), f, indent=4)
        return {"message": "Configuration updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/api/agents")
def get_agents():
    config_path = os.path.join(os.path.dirname(__file__), "agent_config.json")
    try:
        with open(config_path) as f:
            config = json.load(f)
        agents = list(config.get("agents", {}).keys())
        return agents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
