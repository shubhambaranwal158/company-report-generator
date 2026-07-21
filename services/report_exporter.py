from pathlib import Path

OUTPUT_FOLDER = Path("generated_reports")

OUTPUT_FOLDER.mkdir(exist_ok=True)


def save_html(filename: str,
              html: str):

    filepath = OUTPUT_FOLDER / filename

    filepath.write_text(
        html,
        encoding="utf-8"
    )

    return filepath