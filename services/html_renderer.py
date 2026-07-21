from pathlib import Path
from datetime import datetime

# File paths
TEMPLATE_PATH = Path("templates/report_template.html")
CSS_PATH = Path("assets/css/report.css")


def render_report(report_html: str) -> str:
    """
    Renders the final HTML report by injecting:
    - CSS
    - Generated Date
    - Gemini Report HTML
    """

    # Read template
    html = TEMPLATE_PATH.read_text(encoding="utf-8")

    # Read CSS
    styles = CSS_PATH.read_text(encoding="utf-8")

    # Inject CSS
    html = html.replace(
        "{{CSS}}",
        styles
    )

    # Inject current date
    html = html.replace(
        "{{DATE}}",
        datetime.now().strftime("%d %B %Y • %I:%M %p")
    )

    # Inject report body
    html = html.replace(
        "{{REPORT}}",
        report_html
    )

    return html