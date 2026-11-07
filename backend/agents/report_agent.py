
from backend.llm import get_llm


class ReportAgent:

    def __init__(self):
        self.llm = get_llm()

    def generate_report(self, topic: str, findings: str):

        prompt = f"""
        You are a professional AI Research Report Writer.

        Research Topic:
        {topic}

        Research Findings:
        {findings}

        Create a professional research report with:

        1. Title
        2. Executive Summary
        3. Introduction
        4. Detailed Findings
        5. Analysis
        6. Recommendations
        7. Conclusion

        Important rules:
        - Do not create a Sources section.
        - Do not invent website URLs or citations.
        - Do not invent facts that are not in the findings.
        - Clearly mention uncertainty where information is incomplete.
        - Use clear headings and simple professional language.
        """

        response = self.llm.invoke(prompt)
        content = response.content

        if isinstance(content, list):
            return "\n".join(
                item.get("text", "")
                for item in content
                if isinstance(item, dict) and item.get("type") == "text"
            )

        return str(content)
