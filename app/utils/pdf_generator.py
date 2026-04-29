from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.models.schemas import CandidateBrief
import io

def generate_brief_pdf(brief: CandidateBrief) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    Story = []

    # Title
    Story.append(Paragraph(f"Candidate Brief: {brief.profile.name}", styles['Title']))
    Story.append(Spacer(1, 12))

    # Overview
    Story.append(Paragraph(f"Rank: {brief.rank} | Score: {brief.overall_score}/10", styles['Heading2']))
    Story.append(Paragraph(f"Current Role: {brief.profile.current_role}", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Fit Summary
    Story.append(Paragraph("Fit Summary", styles['Heading2']))
    Story.append(Paragraph(brief.fit_summary, styles['Normal']))
    Story.append(Spacer(1, 12))

    # Strengths
    Story.append(Paragraph("Why Strong", styles['Heading2']))
    for s in brief.why_strong:
        Story.append(Paragraph(f"• {s}", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Concerns
    Story.append(Paragraph("Concerns", styles['Heading2']))
    for c in brief.concerns:
        Story.append(Paragraph(f"• {c}", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Suggested Questions
    Story.append(Paragraph("Suggested Interview Questions", styles['Heading2']))
    for q in brief.suggested_questions:
        Story.append(Paragraph(f"• {q}", styles['Normal']))
    Story.append(Spacer(1, 12))

    # Sources
    Story.append(Paragraph("Sources", styles['Heading2']))
    for s in brief.sources:
        Story.append(Paragraph(f"<a href='{s}'>{s}</a>", styles['Normal']))

    doc.build(Story)
    return buffer.getvalue()
