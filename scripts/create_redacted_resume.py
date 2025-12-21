#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
import re

# Read the About markdown and extract relevant sections
with open('about/index.md', 'r') as f:
    md = f.read()

# Remove YAML front matter
md = re.sub(r"^---.*?---\n", '', md, flags=re.S)

# Strip markdown headers into plain text equivalents
md = re.sub(r"^# (.*)$", r"\1", md, flags=re.M)
md = re.sub(r"^## (.*)$", r"\1", md, flags=re.M)
md = re.sub(r"^### (.*)$", r"\1", md, flags=re.M)
md = re.sub(r"\*\*(.*?)\*\*", r"\1", md)
md = re.sub(r"\*(.*?)\*", r"\1", md)
md = re.sub(r"`(.*?)`", r"\1", md)

# Remove any phone numbers and the word 'Nashville' just in case
md = re.sub(r"\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", "", md)
md = re.sub(r"Nashville", "", md, flags=re.I)

# Clean up extra whitespace
md = re.sub(r"\n{3,}", "\n\n", md).strip()

# Convert HTML anchor tags to plain text: <a href="url">text</a> -> "text (url)"
md = re.sub(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r"\2 (\1)", md, flags=re.S)
# Remove remaining HTML tags
md = re.sub(r'<[^>]+>', '', md)

# Generate PDF
doc = SimpleDocTemplate("assets/resume/viswaroop_resume_dec25.pdf", pagesize=letter,
                        rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Heading', fontSize=14, leading=16, spaceAfter=8, spaceBefore=12))
styles.add(ParagraphStyle(name='NormalSmall', fontSize=10, leading=14))

flow = []
flow.append(Paragraph("Viswaroop Vadlamudi", styles['Heading']))
flow.append(Paragraph("Senior Cloud & DevSecOps Engineer", styles['NormalSmall']))
flow.append(Spacer(1, 12))
flow.append(Paragraph("NOTE: This PDF has been redacted to remove phone number and location for privacy.", styles['NormalSmall']))
flow.append(Spacer(1, 12))

for part in md.split('\n\n'):
    # Treat list-like sections
    if part.strip().startswith('-') or part.strip().startswith('*'):
        items = [re.sub(r'^[-*]\s*', '', line).strip() for line in part.splitlines() if line.strip()]
        lf = ListFlowable([ListItem(Paragraph(it, styles['NormalSmall'])) for it in items], bulletType='bullet')
        flow.append(lf)
    else:
        flow.append(Paragraph(part.replace('\n', '<br/>'), styles['NormalSmall']))
    flow.append(Spacer(1, 8))

doc.build(flow)
print('Generated assets/resume/viswaroop_resume_dec25.pdf (redacted)')