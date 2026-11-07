
import re


def split_text_into_chunks(text, chunk_size=1000, overlap=150):
    """Split long text into smaller overlapping chunks."""

    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be non-negative and smaller than chunk_size."
        )

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            # Prefer splitting at a sentence or word boundary.
            boundary = text.rfind(". ", start, end)

            if boundary == -1:
                boundary = text.rfind(" ", start, end)

            if boundary > start:
                end = boundary + 1

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        next_start = max(start + 1, end - overlap)

        start = next_start

    return chunks
