from pypdf import PdfReader
from backend.llm import get_llm


class DocumentAgent:

    def __init__(self):
        self.llm = get_llm()

    def analyze_pdf(self, file_path: str):

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            return "No readable text found in this PDF."

        prompt = f"""
        You are an expert Document Analysis Agent.

        Analyze this document:

        {text[:20000]}

        Provide:
        1. Document Summary
        2. Important Points
        3. Key Findings
        4. Important Information
        5. Conclusion

        Use simple language.
        """

        response = self.llm.invoke(prompt)

        return response.content