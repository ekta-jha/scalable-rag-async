import os
from dotenv import load_dotenv
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from app.core.my_qdrant_client import get_qdrant_client

load_dotenv()

# list all the documents that is converted as vector
def list_documents():

    client = get_qdrant_client()
    collection_name = os.getenv("QDRANT_COLLECTION")

    # Scroll through stored vectors
    records, _ = client.scroll(
        collection_name=collection_name,
        limit = 100,
        with_payload=True
    )

    documents = set()

    for record in records:
        metadata = record.payload.get("metadata",{})
        file_name = metadata.get("file_name")

        if file_name:
            documents.add(file_name)
    
    return list(documents)

# Delete the document
def delete_document(file_name: str):
    client = get_qdrant_client()
    collection_name = os.getenv("QDRANT_COLLECTION")

    client.delete(
        collection_name=collection_name,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="metadata.file_name",
                    match=MatchValue(value=file_name)
                )
            ]
        )
    )

    return {"deleted_document": file_name}