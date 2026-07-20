import PyPDF2

# Resume PDF Path
resume_path = "resumes/resume.pdf"

# Job Description Path
jd_path = "jd/job_description.txt"

# Read Resume PDF
with open(resume_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text

resume_text = resume_text.lower()

# Read Job Description
with open(jd_path, "r") as file:
    jd_text = file.read().lower()

# Skill Database
skills = [
    "python",
    "java",
    "sql",
    "html",
    "css",
    "javascript",
    "c",
    "c++",
    "git",
    "github",
    "mysql",
    "mongodb",
    "machine learning",
    "deep learning",
    "linux",
    "numpy",
    "pandas"
]

resume_skills = set()
jd_skills = set()

# Find Resume Skills
for skill in skills:
    if skill in resume_text:
        resume_skills.add(skill)

# Find JD Skills
for skill in skills:
    if skill in jd_text:
        jd_skills.add(skill)

# Match & Missing Skills
matched = resume_skills.intersection(jd_skills)
missing = jd_skills - resume_skills

# Match Score
if len(jd_skills) > 0:
    score = (len(matched) / len(jd_skills)) * 100
else:
    score = 0

print("\n========== ATS Resume Report ==========\n")

print("Matched Skills:")
for skill in matched:
    print("✅", skill.title())

print("\nMissing Skills:")
for skill in missing:
    print("❌", skill.title())

print(f"\nATS Match Score: {score:.2f}%")