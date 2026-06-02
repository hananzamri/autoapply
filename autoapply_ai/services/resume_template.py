from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet


def create_resume_pdf(text: str, output_path: str):
    doc = SimpleDocTemplate(output_path)

    styles = getSampleStyleSheet()

    story = []

    for line in text.split("\n"):
        if line.strip():
            story.append(
                Paragraph(line, styles["Normal"])
            )
            story.append(Spacer(1, 4))

    doc.build(story)