
import chromadb
from pathlib import Path


DB_PATH = Path("data/chroma_db")


def get_vector_collection():
    """Create or connect to the persistent ChromaDB collection."""

    DB_PATH.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    collection = client.get_or_create_collection(
        name="research_documents"
    )

    return collection
