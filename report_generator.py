from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

def generate_pdf(candidate, filename):

    pdf = SimpleDocTemplate(filename)

    elements = []

    elements.append(Paragraph("<b>ATS Resume Report</b>", styles["Title"]))

    elements.append(Paragraph(f"<b>Name:</b> {candidate['Name']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Email:</b> {candidate['Email']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Phone:</b> {candidate['Phone']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Education:</b> {candidate['Education']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Experience:</b> {candidate['Experience']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Projects:</b> {candidate['Projects']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Skills:</b> {candidate['Found Skills']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Missing Skills:</b> {candidate['Missing Skills']}", styles["Normal"]))
    elements.append(Paragraph(f"<b>ATS Score:</b> {candidate['Score']}%", styles["Normal"]))
    elements.append(Paragraph(f"<b>Status:</b> {candidate['Status']}", styles["Normal"]))

    pdf.build(elements)