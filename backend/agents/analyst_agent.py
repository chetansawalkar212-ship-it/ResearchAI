
from backend.llm import get_llm


class AnalystAgent:

    def __init__(self):
        self.llm = get_llm()

    def analyze(self, research_data: str):

        prompt = f"""
        You are an expert AI Analyst Agent.

        Review the following research:

        {research_data}

        Your tasks:
        1. Identify the most important findings.
        2. Check for missing information.
        3. Identify possible contradictions.
        4. Separate facts from assumptions.
        5. Give recommendations.

        Be objective and use simple language.
        Do not invent facts.
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
