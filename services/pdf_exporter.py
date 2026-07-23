from pathlib import Path
from weasyprint import HTML


OUTPUT_DIR = Path("downloads/generated_reports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_pdf(filename: str, html_content: str) -> Path:
    """
    Converts rendered HTML into a PDF and saves it.

    Returns:
        Path to generated PDF
    """

    pdf_path = OUTPUT_DIR / filename.replace(".html", ".pdf")

    HTML(string=html_content).write_pdf(pdf_path)

    return pdf_path