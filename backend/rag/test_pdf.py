from backend.rag.document_processor import extract_text_from_pdf

pdf_path = "data/sample.pdf"

text = extract_text_from_pdf(pdf_path)

print("\nPDF TEXT EXTRACTION SUCCESSFUL!")
print("--------------------------------")
print(text[:1000])