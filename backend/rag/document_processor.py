
from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """Extract text from every page of a PDF."""

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path}"
        )

    if not pdf_path.is_file():
        raise ValueError("The provided path is not a file.")

    try:
        reader = PdfReader(str(pdf_path))

        if reader.is_encrypted:
            raise ValueError(
                "This PDF is password-protected and cannot be read."
            )

        extracted_pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()

                if page_text and page_text.strip():
                    extracted_pages.append(
                        f"\n--- Page {page_number} ---\n{page_text.strip()}"
                    )

            except Exception as error:
                print(
                    f"Warning: Could not extract page {page_number}: {error}"
                )

        return "\n".join(extracted_pages)

    except Exception as error:
        raise RuntimeError(
            f"Failed to read PDF file: {error}"
        ) from error
