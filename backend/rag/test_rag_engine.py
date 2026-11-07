
from backend.rag.rag_engine import store_pdf_in_database

pdf_path = "data/sample.pdf"

print("Starting RAG storage test...\n")

document_id = store_pdf_in_database(pdf_path)

print("\nRAG STORAGE TEST COMPLETED!")
print("Document ID:", document_id)
