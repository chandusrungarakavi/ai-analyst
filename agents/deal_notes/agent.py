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

def query_rag_corpus(
    query_text: str
):
    # Create the resource config
    rag_resource = rag.RagResource(rag_corpus=CORPUS_NAME)
        
    # Execute the query directly using the API
    response = rag.retrieval_query(
        rag_resources=[rag_resource],
        text=query_text,
    )
    return response.text if hasattr(response, "text") else str(response)


deal_notes_agent = Agent(
    model="gemini-2.5-flash",
    name='deal_notes_agent',
    description='Searches ingested pitch decks, call transcripts, founder updates, and emails to generate structured deal notes.',
    instruction='Given a collection of documents (pitch decks, transcripts, etc.), analyze them and generate structured deal notes.',
    tools=[FunctionTool(query_rag_corpus)]
)