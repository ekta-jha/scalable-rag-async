import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

from app.core.my_qdrant_client import get_qdrant_client
from app.rag.embeddings import get_embedding

load_dotenv()

def retrieve_similar_chunks(query: str, k: int = 3):
    client = get_qdrant_client()

    collection_name = os.getenv("QDRANT_COLLECTION")
    embedding_model = get_embedding()

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embedding_model,
    )

    results = vector_store.similarity_search(query, k = k)

    return [doc.page_content for doc in results]
