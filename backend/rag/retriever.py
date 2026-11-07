
from backend.rag.embedding_engine import get_embedding_model
from backend.rag.vector_store import get_vector_collection


def retrieve_relevant_chunks(question, document_id=None, top_k=3):
    """Find the most relevant PDF text chunks for a question."""

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Please provide a valid question.")

    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
        raise ValueError("top_k must be a positive integer.")

    question = question.strip()

    print("1. Connecting to ChromaDB...")

    try:
        collection = get_vector_collection()

        if collection.count() == 0:
            print("No documents found in the database.")
            return []

        print("2. Loading embedding model...")
        embedding_model = get_embedding_model()

        print("3. Converting question into a vector...")
        question_embedding = embedding_model.embed_query(question)

        print("4. Searching ChromaDB...")

        query_filter = None

        if document_id:
            query_filter = {
                "document_id": document_id
            }

        query_arguments = {
            "query_embeddings": [question_embedding],
            "n_results": top_k
        }

        if query_filter:
            query_arguments["where"] = query_filter

        results = collection.query(**query_arguments)

        documents = results.get("documents") or [[]]
        metadatas = results.get("metadatas") or [[]]

        retrieved_documents = documents[0] if documents else []
        retrieved_metadata = metadatas[0] if metadatas else []

        chunks = []

        for document, metadata in zip(
            retrieved_documents,
            retrieved_metadata
        ):
            if not document:
                continue

            metadata = metadata or {}

            chunks.append({
                "text": document,
                "source": metadata.get("source", "Unknown")
            })

        print("5. Retrieval completed!")
        print("Total relevant chunks:", len(chunks))

        return chunks

    except (ValueError, TypeError):
        raise

    except Exception as error:
        print(f"Retrieval error: {error}")

        raise RuntimeError(
            "Failed to retrieve information from the document database."
        ) from error
