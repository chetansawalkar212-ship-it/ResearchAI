
from ddgs import DDGS
from urllib.request import Request, urlopen
from html.parser import HTMLParser
from urllib.parse import urlparse


class PageTextExtractor(HTMLParser):

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {
            "script", "style", "noscript", "svg",
            "nav", "footer"
        }
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):

        if tag in self.skip_tags:
            self.skip_depth += 1

    def handle_endtag(self, tag):

        if tag in self.skip_tags and self.skip_depth > 0:
            self.skip_depth -= 1

    def handle_data(self, data):

        if self.skip_depth == 0:
            clean_text = data.strip()

            if clean_text:
                self.text_parts.append(clean_text)

    def get_text(self):
        return " ".join(self.text_parts)


class WebResearchAgent:

    def __init__(self):
        self.search_tool = DDGS()

    def extract_page_content(self, url: str):

        try:
            parsed_url = urlparse(url)

            if parsed_url.scheme not in ("http", "https"):
                return "Unsupported URL."

            request = Request(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 ResearchAI/1.0"
                    )
                }
            )

            with urlopen(request, timeout=15) as response:

                content_type = response.headers.get(
                    "Content-Type", ""
                )

                if "text/html" not in content_type.lower():
                    return "This page is not an HTML webpage."

                charset = response.headers.get_content_charset() or "utf-8"

                html = response.read(2_000_000).decode(
                    charset,
                    errors="replace"
                )

            extractor = PageTextExtractor()
            extractor.feed(html)

            page_text = extractor.get_text()

            if not page_text:
                return "No readable text found on this page."

            return page_text[:12000]

        except Exception as error:

            print(f"Page extraction failed: {error}")
            return "Could not extract webpage content."

    def research(self, topic: str, max_results: int = 5):

        print(f"\nSearching the web for: {topic}\n")

        try:
            results = self.search_tool.text(
                topic,
                max_results=max_results
            )

            research_data = []

            for index, result in enumerate(results, start=1):

                title = result.get("title", "No title")
                url = result.get("href", "")
                body = result.get("body", "No description")

                print(
                    f"\nReading webpage {index}/{max_results}: "
                    f"{title}"
                )

                page_content = self.extract_page_content(url)

                research_data.append({
                    "title": title,
                    "url": url,
                    "description": body,
                    "content": page_content
                })

            return research_data

        except Exception as error:

            print(f"Web search failed: {error}")
            return []


if __name__ == "__main__":

    agent = WebResearchAgent()

    topic = input("Enter a research topic: ")

    results = agent.research(topic)

    for index, result in enumerate(results, start=1):

        print(f"\n--- Source {index} ---")
        print("Title:", result["title"])
        print("URL:", result["url"])
        print("Description:", result["description"])
        print("Extracted Content:")
        print(result["content"][:1000])
