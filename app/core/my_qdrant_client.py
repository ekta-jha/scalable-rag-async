import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

def get_qdrant_client() -> QdrantClient:
    """
    Returns a configured Qdrant client instance.

    Uses environment variables:
    - QDRANT_HOST
    - QDRANT_PORT

    Falls back to sensible defaults for local development.
    """

    host = os.getenv("QDRANT_HOST")
    port = os.getenv("QDRANT_PORT")

    return QdrantClient(
        host=host,
        port=port,
    )