
from backend.rag.retriever import retrieve_relevant_chunks

question = "How does AI help doctors?"

print("Searching ResearchAI knowledge base...\n")

results = retrieve_relevant_chunks(question)

print("\nRETRIEVAL TEST SUCCESSFUL!")
print("--------------------------")

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}:")
    print("Source:", result["source"])
    print("Text:", result["text"])
