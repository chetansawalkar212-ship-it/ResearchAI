
import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


def get_embedding_model():
    """Create and return Google's embedding model."""

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is missing. Please check your .env file."
        )

    try:
        return GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=api_key
        )

    except Exception as error:
        raise RuntimeError(
            f"Failed to initialize Gemini embedding model: {error}"
        ) from error
