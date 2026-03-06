# Scalable RAG with Async Queues & Distributed Workers

## Architecture

User → FastAPI → Redis (Valkey) → RQ Workers → RAG Pipeline → Qdrant → LLM


                ┌───────────────┐
                │   FastAPI     │
                │   API Layer   │
                └──────┬────────┘
                       │
                       │ enqueue job
                       ▼
                ┌───────────────┐
                │     Redis     │
                │  Job Queue    │
                └──────┬────────┘
                       │
                       │ worker pulls job
                       ▼
                ┌───────────────┐
                │     Worker    │
                │   RAG Task    │
                └──────┬────────┘
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
   Qdrant Vector DB            Azure OpenAI
   (Semantic Search)           (Answer Gen)



## Features

- Async job processing
- Distributed workers
- Dockerized microservices
- Vector search with Qdrant
- Queue-based LLM processing

## Setup

```bash
docker-compose up --build