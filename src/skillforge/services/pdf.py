"""Roadmap PDF export."""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from skillforge.models import Roadmap


def generate_roadmap_pdf(plan: Roadmap) -> bytes:
    """Create the downloadable roadmap PDF in memory."""
    buffer = BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30,
                                 topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("SkillForgeTitle", parent=styles["Title"], fontSize=20,
                                 textColor=colors.HexColor("#4B7BEC"), spaceAfter=20)
    day_style = ParagraphStyle("SkillForgeDay", parent=styles["Heading2"], fontSize=14,
                               textColor=colors.black, spaceAfter=10)
    topic_style = ParagraphStyle("SkillForgeTopic", parent=styles["Normal"], fontSize=11,
                                 spaceAfter=5)
    story = [Paragraph("🚀 SkillForge Roadmap", title_style), Spacer(1, 10)]
    for day, topics in plan.items():
        story.append(Paragraph(day.replace("_", " ").title(), day_style))
        if topics:
            story.extend(Paragraph(f"• {topic}", topic_style) for topic in topics)
        else:
            story.append(Paragraph("😴 Rest / Theory Day", topic_style))
        story.append(Spacer(1, 10))
    document.build(story)
    return buffer.getvalue()
