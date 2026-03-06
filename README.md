# Scalable RAG Async

Scalable Retrieval-Augmented Generation (RAG) API built with FastAPI, Redis/RQ background jobs, Qdrant vector search, and Azure OpenAI.

This project is designed to decouple ingestion and query processing from request/response latency by using async queue workers.

## What This Project Does

- Accepts PDF uploads through an API.
- Processes ingestion asynchronously in background workers.
- Chunks and embeds document content with Azure OpenAI embeddings.
- Stores vectors in Qdrant for semantic retrieval.
- Supports semantic similarity search across all docs or a specific file.
- Runs RAG question-answering jobs asynchronously using retrieved context.
- Provides job status/result polling endpoints.
- Supports listing and deleting indexed documents.

## Architecture

```text
Client
  -> FastAPI API
  -> Redis Queue (RQ)
  -> Worker(s)
      -> PDF Loader + Chunking
      -> Azure OpenAI Embeddings
      -> Qdrant Vector Store
      -> Azure OpenAI Chat Completion
  <- Job Status / Results
```

## Feature List

1. Asynchronous PDF ingestion using RQ workers.
2. Asynchronous RAG query execution with queue-based processing.
3. Job tracking endpoint for queued/running/finished/failed states.
4. PDF parsing via LangChain `PyPDFLoader`.
5. Recursive text chunking (`chunk_size=1000`, `chunk_overlap=200`).
6. Azure OpenAI embeddings integration.
7. Qdrant vector storage for document chunks.
8. Semantic similarity search endpoint.
9. Optional file-level filtering for similarity and RAG queries.
10. Metadata tagging for chunks (`document_id`, `file_name`).
11. Document catalog endpoint (`/documents`) from vector metadata.
12. Document delete endpoint that removes vectors by `file_name`.
13. Dockerized API and worker services.
14. Shared Docker volume for uploaded file handoff (`/shared`).
15. FastAPI automatic docs (`/docs`, `/redoc`).

## Tech Stack

- FastAPI
- Redis + RQ
- LangChain
- Qdrant
- Azure OpenAI
- Docker / Docker Compose

## Project Structure

```text
app/
  api/
    routes.py                # REST endpoints
  core/
    redis_client.py          # Redis + queue setup
    azure_openai_client.py   # Azure OpenAI chat client
    my_qdrant_client.py      # Qdrant client
  rag/
    pdf_loader.py            # PDF load + split
    embeddings.py            # Azure embeddings model
    vector_store.py          # Qdrant writes
    retriever.py             # Similarity search
    pipeline.py              # End-to-end ingestion
    documents.py             # List/delete documents
  queue/
    tasks.py                 # Background task functions
    worker.py                # RQ worker entrypoint
```

## Prerequisites

- Python 3.11+
- Redis instance (or Valkey-compatible endpoint)
- Qdrant instance
- Azure OpenAI resource with:
  - Chat deployment
  - Embedding deployment
- Docker (optional but recommended)

## Environment Variables

Create a `.env` file in the project root.

```env
# Redis
REDIS_HOST=host.docker.internal
REDIS_PORT=6379

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=your_collection_name

# Azure OpenAI embeddings
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=<embedding_api_key>
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=<embedding_deployment_name>
AZURE_OPENAI_EMBEDDING_API_VERSION=<api_version>

# Azure OpenAI chat
AZURE_OPENAI_CHAT_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_CHAT_API_KEY=<chat_api_key>
AZURE_OPENAI_CHAT_DEPLOYMENT=<chat_deployment_name>
AZURE_OPENAI_CHAT_API_VERSION=<api_version>
```

## Run With Docker Compose

```bash
docker-compose up --build
```

API: `http://localhost:8000`  
Swagger docs: `http://localhost:8000/docs`

## Run Locally (Without Docker)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

3. Start worker (separate terminal):

```bash
python -m app.queue.worker
```

## API Endpoints

### 1) Upload PDF (async ingestion)

- `POST /upload-pdf`
- Form field: `file`
- Response: `job_id`, queue status

### 2) Similarity search

- `GET /similarity_search?query=<text>&file_name=<optional.pdf>`
- Returns top matching chunks

### 3) RAG query (async)

- `POST /rag-query?query=<text>&file_name=<optional.pdf>`
- Response: `job_id`, queue status

### 4) Job status/result

- `GET /job/{job_id}`
- Returns current state or final result/error

### 5) List indexed documents

- `GET /documents`

### 6) Delete indexed document

- `DELETE /documents/{file_name}`

## Example Workflow

1. Upload PDF using `/upload-pdf`.
2. Poll `/job/{job_id}` until ingestion is `finished`.
3. Test retrieval with `/similarity_search`.
4. Submit `/rag-query`.
5. Poll `/job/{job_id}` for final answer.

## Notes

- Uploaded files are saved to `/shared` for worker access.
- Current queue name is `default`.
- RAG answers are instructed to use retrieved context only.
