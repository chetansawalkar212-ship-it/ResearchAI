
from backend.rag.embedding_engine import get_embedding_model

print("Loading Google Embedding Model...")

embedding_model = get_embedding_model()

print("Converting text into numerical vectors...")

vector = embedding_model.embed_query(
    "Artificial Intelligence helps doctors."
)

print("\nEMBEDDING TEST SUCCESSFUL!")
print("--------------------------")
print("Vector length:", len(vector))
print("First 5 values:", vector[:5])
