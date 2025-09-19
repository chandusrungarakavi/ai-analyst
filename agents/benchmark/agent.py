from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search


benchmark_agent = Agent(
    model='gemini-2.5-flash',
    name='benchmark_agent',
    description='Benchmarks startups against sector peers using financial multiples, hiring data, and traction signals.',
    instruction='Given the startup, use Google Search to find relevant data and benchmark the startup against its sector peers. Provide a detailed report with financial multiples, hiring data, and traction signals.',
    tools=[google_search]
)

deal_notes_agent = Agent(
    model='gemini-2.5-flash',
    name='deal_notes_agent',
    description='Ingests pitch decks, call transcripts, founder updates, and emails to generate structured deal notes.',
    instruction='Given a collection of documents (pitch decks, transcripts, etc.), analyze them and generate structured deal notes.'
)

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A root agent that delegates tasks to specialized sub-agents for deal note generation and startup benchmarking.',
    instruction='Given a user request, determine whether to generate deal notes or benchmark a startup, then delegate to the appropriate sub-agent.',
    sub_agents=[deal_notes_agent, benchmark_agent],
)
# root_agent = Agent(
#     model='gemini-2.5-flash',
#     name='root_agent',
#     description='An agent that finds and analyzes news about startups using Google Search.',
#     instruction="Given a startup name, search for recent news and provide a concise analysis of the startup's current status, including funding, product launches, and market sentiment.",
#     tools=[google_search],
# )
