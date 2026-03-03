import os
from fastapi import APIRouter, UploadFile, File, Query
from rq.job import Job
from rq import Retry

from app.core.redis_client import check_redis,redis_conn
from app.queue.queue_client import queue
from app.queue.tasks import test_task
from app.rag.pdf_loader import load_pdf, split_documents
from app.rag.embeddings import get_embedding
from app.rag.vector_store import store_documents
from app.rag.retriever import retrieve_similar_chunks


router = APIRouter()

# checks the fastapi app status
@router.get("/")
def health():
    return {"status": "API running"}

# checks the redis connection status
@router.get("/redis-health")
def redis_health():
    status = check_redis()
    return {"redis_connected": status}

# Test enqueue to redis
@router.post("/enqueue-test")
def enqueue_test():
    job = queue.enqueue(
            test_task,
            retry=Retry(max=3),
            job_timeout=30
        )
    return {"job_id": job.id}

# check the job status
@router.get("/status/{job_id}")
def get_status(job_id: str):
    job = Job.fetch(job_id, connection=redis_conn)

    return{
        "status": job.get_status(),
        "result": job.result
    }

# Uploading document and Creating embedding + storing it in Vector DB
@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = f"/tmp/{file.filename}"

    with open(file_location, "wb") as f:
        f.write(await file.read())

    # 1. Load PDF
    documents = load_pdf(file_location)

    # 2. split into chunks
    chunks = split_documents(documents)

    # 3. Get Azure Embedding Model
    embeddings_model = get_embedding()

    # 4️ Store directly in Qdrant
    points_stored = store_documents(
        chunks=chunks,
        embedding=embeddings_model
    )

    return{
        "filename": file.filename,
        "pages_loaded": len(documents),
        "chunks_created": len(chunks),
        "points_stored": points_stored
    }

@router.get("/search")
def search(query: str = Query(...)):
    results = retrieve_similar_chunks(query)

    return {
        "query": query,
        "matches_found": len(results),
        "results": results
    }

