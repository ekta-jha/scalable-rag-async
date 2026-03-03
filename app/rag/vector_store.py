import os
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore

load_dotenv()

def store_documents(chunks, embedding):
    host = os.getenv("QDRANT_HOST")
    port = os.getenv("QDRANT_PORT")
    collection_name = os.getenv("QDRANT_COLLECTION")

    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embedding,
        url=f"http://{host}:{port}",
        collection_name=collection_name,
    )

    return len(chunks)