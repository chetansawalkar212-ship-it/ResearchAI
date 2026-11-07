
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from xml.sax.saxutils import escape


def export_report(report):
    """Generate a professional PDF from a research report."""

    output_folder = Path("data")
    output_folder.mkdir(parents=True, exist_ok=True)

    output_path = output_folder / "research_report.pdf"

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#312e81"),
        spaceAfter=20
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=16,
        spaceAfter=8
    )

    story = []

    story.append(
        Paragraph("ResearchAI Research Report", title_style)
    )

    story.append(Spacer(1, 12))

    safe_report = escape(str(report))
    formatted_report = safe_report.replace("\n", "<br/>")

    story.append(
        Paragraph(formatted_report, body_style)
    )

    document.build(story)

    return str(output_path)
