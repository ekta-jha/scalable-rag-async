import os
from fastapi import APIRouter, UploadFile, File, Query
from typing import Optional
from rq.job import Job
from rq import Retry

from app.core.redis_client import redis_conn, queue
from app.rag.pdf_loader import load_pdf, split_documents
from app.rag.embeddings import get_embedding
from app.rag.vector_store import store_documents
from app.rag.retriever import retrieve_similar_chunks
from app.queue.tasks import rag_query_task, ingest_document_task
from app.rag.documents import list_documents, delete_document



router = APIRouter()

# Uploading document and Creating embedding + storing it in Vector DB
@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = f"/shared/{file.filename}"

    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Enqueue ingestion job
    job = queue.enqueue(
        ingest_document_task,
        file_location,
        job_timeout = 300
    )

    return{
        "job_id": job.id,
        "status": "queued"
    }

# Similarity Search APi
@router.get("/similarity_search")
def search(
    query: str = Query(...),
    file_name: str | None = Query
    ):
    results = retrieve_similar_chunks(
        query=query,
        file_name=file_name
    )

    return {
        "query": query,
        "matches_found": len(results),
        "results": results
    }

# RAG Query API
@router.post("/rag-query")
def enqueue_rag_query(
        query: str = Query(...),
        file_name: Optional[str] = Query(None)):
    """
    Enqueue a RAG query to be processed by the worker.
    Returns a job ID.
    """
    job = queue.enqueue(
        rag_query_task,
        query,
        file_name,
        job_timeout=120,
        result_ttl=3600
    )

    return{
        "job_id": job.id,
        "status": "queued"
    }

# Endpoint to check job status and fetch results
@router.get("/job/{job_id}")
def get_job_ressult(job_id: str):
    """
    Fetch status or result of a queue job.
    """
    job = Job.fetch(job_id, connection=redis_conn)

    if job.is_finished:
        return{
            "status": "finished",
            "result": job.result
        }
    
    if job.is_failed:
        return {
            "status": "failed",
            "error": str(job.exc_info)
        }
    return {
        "status": job.get_status()
    }

# fetch all the documents
@router.get("/documents")
def get_documents():

    doc = list_documents()

    return {
        "documents": doc
    }

# Delete the document
@router.delete("/documents/{file_name}")
def remove_document(file_name:str):

    result = delete_document(file_name)

    return{
        "status": "deleted",
        "document": result["deleted_document"]
    }


