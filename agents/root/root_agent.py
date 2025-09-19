from google.adk.agents.llm_agent import Agent, LlmAgent
from google.adk.tools import AgentTool, google_search

# Sub-agent: Startup benchmarking
benchmark_agent = Agent(
    model="gemini-2.5-flash",
    name="benchmark_agent",
    description="Benchmarks startups against sector peers using financial multiples, hiring data, and traction signals.",
    instruction=(
        "Given the startup, use Google Search to find relevant data and benchmark the startup against its sector peers. "
        "Provide a detailed report with financial multiples, hiring data, and traction signals."
    ),
    tools=[google_search],
)

# Sub-agent: Deal notes generation
deal_notes_agent = Agent(
    model="gemini-2.5-flash",
    name="deal_notes_agent",
    description="Ingests pitch decks, call transcripts, founder updates, and emails to generate structured deal notes.",
    instruction=(
        "Given a collection of documents (pitch decks, transcripts, etc.), analyze them and generate structured deal notes."
    ),
)

# Wrap sub-agents as tools
benchmark_tool = AgentTool(agent=benchmark_agent)
deal_notes_tool = AgentTool(agent=deal_notes_agent)

# Root agent: Delegates to sub-agents
root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Delegates tasks to specialized sub-agents for deal note generation and startup benchmarking.",
    instruction=(
        "Given a user request, determine whether to generate deal notes or benchmark a startup, then delegate to the appropriate sub-agent."
    ),
    tools=[deal_notes_tool, benchmark_tool],
)
