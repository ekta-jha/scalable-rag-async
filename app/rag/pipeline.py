import os
import uuid
from app.rag.pdf_loader import load_pdf, split_documents
from app.rag.embeddings import get_embedding
from app.rag.vector_store import store_documents

def ingest_pdf(file_path: str):
    """
    End-to-end ingetion pipeline for a pdf
    """
    # 1. Load PDF
    documents = load_pdf(file_path)

    # 2. split into chunks
    chunks = split_documents(documents)

    # 3. generate unique document id
    document_id = str(uuid.uuid4())
    file_name = os.path.basename(file_path)

    # 4. attach metadata to each chunk
    for chunk in chunks:
        chunk.metadata["document_id"] = document_id
        chunk.metadata["file_name"] = file_name

    # 5. Get Azure Embedding Model
    embeddings_model = get_embedding()

    # 4️ Store directly in Qdrant
    points_stored = store_documents(
        chunks=chunks,
        embedding=embeddings_model
    )

    return{
        "pages_loaded": len(documents),
        "file_name": file_name,
        "chunks_created": len(chunks),
        "points_stored": points_stored
    }