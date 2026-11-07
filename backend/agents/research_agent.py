
from backend.llm import get_llm


class ResearchAgent:

    def __init__(self):
        self.llm = get_llm()

    def research(self, topic: str):

        prompt = f"""
        You are an expert AI Research Agent.

        Research the following topic:
        {topic}

        Provide:
        1. Introduction
        2. Important facts
        3. Key findings
        4. Advantages
        5. Disadvantages
        6. Conclusion

        Use simple and clear language.
        If you are unsure about a fact, mention it.
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
