
from backend.rag.vector_store import get_vector_collection

print("Connecting to ChromaDB...")

collection = get_vector_collection()

print("\nCHROMADB CONNECTION SUCCESSFUL!")
print("--------------------------------")
print("Collection name:", collection.name)
print("Total stored documents:", collection.count())
