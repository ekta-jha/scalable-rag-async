# Scalable RAG with Async Queues & Distributed Workers

## Architecture

User → FastAPI → Redis (Valkey) → RQ Workers → RAG Pipeline → Qdrant → LLM

## Features

- Async job processing
- Distributed workers
- Dockerized microservices
- Vector search with Qdrant
- Queue-based LLM processing

## Setup

```bash
docker-compose up --build