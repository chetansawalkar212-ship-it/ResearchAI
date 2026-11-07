
import uuid
from pathlib import Path

from backend.rag.document_processor import extract_text_from_pdf
from backend.rag.text_chunker import split_text_into_chunks
from backend.rag.embedding_engine import get_embedding_model
from backend.rag.vector_store import get_vector_collection


def store_pdf_in_database(pdf_path):
    """Extract, split, embed, and store PDF content in ChromaDB."""

    pdf_path = str(Path(pdf_path))

    if not Path(pdf_path).exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    print("1. Reading PDF...")
    text = extract_text_from_pdf(pdf_path)

    if not text or not text.strip():
        raise ValueError("No readable text found in the PDF.")

    print("2. Splitting text into chunks...")
    chunks = split_text_into_chunks(text)

    chunks = [
        chunk.strip()
        for chunk in chunks
        if chunk and chunk.strip()
    ]

    if not chunks:
        raise ValueError("No valid text chunks could be created.")

    print("3. Loading embedding model...")
    embedding_model = get_embedding_model()

    print("4. Converting chunks into embeddings...")
    embeddings = embedding_model.embed_documents(chunks)

    if len(embeddings) != len(chunks):
        raise ValueError("Embedding count does not match chunk count.")

    print("5. Connecting to ChromaDB...")
    collection = get_vector_collection()

    document_id = str(uuid.uuid4())
    source_name = Path(pdf_path).name

    print("6. Storing chunks in database...")

    try:
        collection.add(
            ids=[
                f"{document_id}_{i}"
                for i in range(len(chunks))
            ],
            documents=chunks,
            embeddings=embeddings,
            metadatas=[
                {
                    "source": source_name,
                    "document_id": document_id,
                    "chunk_number": i
                }
                for i in range(len(chunks))
            ]
        )

    except Exception as error:
        print(f"ChromaDB storage error: {error}")
        raise RuntimeError(
            "Failed to store PDF content in the vector database."
        ) from error

    print("\nPDF STORED SUCCESSFULLY!")
    print("Document:", source_name)
    print("Total chunks stored:", len(chunks))

    return document_id
