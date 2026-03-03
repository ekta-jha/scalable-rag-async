import os
from dotenv import load_dotenv
from app.core.azure_openai_client import get_azure_openai_client
from app.rag.retriever import retrieve_similar_chunks

load_dotenv()

def rag_query_task(query: str):
    chunks = retrieve_similar_chunks(query, k=3)
    context_text = "\n\n".join(chunks)

    client = get_azure_openai_client()

    response = client.chat.completions.create(
        model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        messages=[
            {"role": "system", "content": "Answer using the provided context only."},
            {"role": "user", "content": f"Context:\n{context_text}\n\nQuery:\n{query}"},
        ],
    )

    return {"answer": response.choices[0].message.content}