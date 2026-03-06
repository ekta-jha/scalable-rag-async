import os
from dotenv import load_dotenv

from app.rag.embeddings import get_embedding
from app.core.azure_openai_client import get_azure_openai_client
from app.rag.retriever import retrieve_similar_chunks
from app.rag.pipeline import ingest_pdf

load_dotenv()

# Celery worker tasks for document ingestion
def ingest_document_task(file_path: str):
    """
    Worker task to ingest a PDF document into the vector store.
    """
    return ingest_pdf(file_path)

# Celery worker task for RAG query
def rag_query_task(query: str, file_name: str | None=None):
    """ 
    Worker task: performs RAG for a given query.

    Steps:
    - Retrieve top chunks from vector store
    - Create a prompt for Azure OpenAI
    - Call Azure OpenAI Chat Completion
    - Return final answer
    """
    # Step A - Semantic Search
    chunks = retrieve_similar_chunks(
            query=query, 
            k=3,
            file_name=file_name
        )

    # Combine chunks
    context_text = "\n\n".join(chunks)
    
    # Step B — Prepare Azure Chat client
    client = get_azure_openai_client()

    # Step C — Build prompt
    system_msg = "You are an AI assistant. Answer using the provided context only."
    user_msg = f"Context: \n{context_text}\n\n User Query:\n{query}"

    # Call Chat Completion
    response = client.chat.completions.create(
        model= os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"), #type: ignore
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
    )
    answer = response.choices[0].message.content
    
    return {"answer": answer}


