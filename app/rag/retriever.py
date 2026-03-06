import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

from app.core.my_qdrant_client import get_qdrant_client
from app.rag.embeddings import get_embedding

load_dotenv()

# Retrieve Result from all documents pr specific by file_name

def retrieve_similar_chunks(query: str, k: int = 3, file_name: str | None = None):
    client = get_qdrant_client()

    collection_name = os.getenv("QDRANT_COLLECTION")
    embedding_model = get_embedding()

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embedding_model,
    )

    search_filter = None

    if file_name:
        search_filter = Filter(
            must=[
                FieldCondition(
                    key="metadata.file_name",
                    match = MatchValue(value=file_name)
                )
            ]
        )
    
    results = vector_store.similarity_search(
        query,
        k=k,
        filter = search_filter
    )
    
    return [doc.page_content for doc in results]
