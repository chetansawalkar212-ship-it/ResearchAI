
from pathlib import Path

from backend.orchestrator.graph import build_graph
from backend.pdf_exporter import export_report


def get_file_path(prompt, extension):

    while True:
        file_path = input(prompt).strip().strip('"')

        if not file_path:
            return ""

        path = Path(file_path)

        if path.suffix.lower() != extension:
            print(f"Please enter a valid {extension} file.")
            continue

        if not path.is_file():
            print("File not found. Please check the path.")
            continue

        return str(path)


def main():

    print("\n================================")
    print("       RESEARCH AI SYSTEM")
    print("================================\n")

    topic = input("Enter your research topic: ").strip()

    if not topic:
        print("\nError: Please enter a valid research topic.")
        return

    pdf_path = get_file_path(
        "\nEnter PDF file path (press Enter to skip): ",
        ".pdf"
    )

    csv_path = get_file_path(
        "\nEnter CSV file path (press Enter to skip): ",
        ".csv"
    )

    print("\nResearchAI is working...")
    print("Agents are collaborating. Please wait.\n")

    try:

        app = build_graph()

        result = app.invoke({
            "topic": topic,
            "pdf_path": pdf_path,
            "csv_path": csv_path,
            "research": "",
            "web_research": "",
            "document_analysis": "",
            "data_analysis": "",
            "source_results": [],
            "analysis": "",
            "report": ""
        })

        report = result["report"]

        print("\n========== FINAL RESEARCH REPORT ==========\n")
        print(report)

        print("\nGenerating PDF report...")

        try:
            pdf_file = export_report(report)

            print("\nPDF report successfully saved!")
            print(f"PDF Location: {pdf_file}")

        except Exception as error:
            print("\nPDF export failed.")
            print(f"Error: {error}")

    except KeyboardInterrupt:
        print("\n\nResearchAI stopped by user.")

    except Exception as error:
        print("\nSomething went wrong while running ResearchAI.")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
