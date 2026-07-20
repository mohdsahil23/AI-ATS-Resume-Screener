import PyPDF2

# Resume PDF Path
file_path = "resumes/resume.pdf"

# Read Resume PDF
with open(file_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

# Convert text to lowercase
resume_text = resume_text.lower()

# Skill Database
skills = [
    "python",
    "java",
    "sql",
    "html",
    "css",
    "javascript",
    "c++",
    "c",
    "mysql",
    "mongodb",
    "git",
    "github",
    "linux",
    "machine learning",
    "deep learning",
    "numpy",
    "pandas",
    "flask",
    "django"
]

# Find Skills
found_skills = []

for skill in skills:
    if skill in resume_text:
        found_skills.append(skill)

# Print Output
print("\n========== Skills Found ==========\n")

if found_skills:
    for skill in found_skills:
        print("✅", skill.title())
else:
    print("No skills found.")

print("\nTotal Skills Found:", len(found_skills))