
from google.adk.agents import Agent

benchmark_agent = Agent(
    model='gemini-2.5-flash',
    name='benchmark_agent',
    description='Benchmarks startups against sector peers using financial multiples, hiring data, and traction signals.',
    instruction='Given a startup and sector, compare the startup to its sector peers using financial multiples, hiring data, and traction signals. Return a structured benchmark report.'
)
