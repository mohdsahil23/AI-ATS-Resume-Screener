import re

def extract_email(text):
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return email[0] if email else "Not Found"


def extract_phone(text):
    phone = re.findall(r"\+?\d[\d\s\-]{8,15}", text)
    return phone[0] if phone else "Not Found"


def extract_linkedin(text):
    linkedin = re.findall(r"https?://(?:www\.)?linkedin\.com/[^\s]+", text)
    return linkedin[0] if linkedin else "Not Found"


def extract_github(text):
    github = re.findall(r"https?://(?:www\.)?github\.com/[^\s]+", text)
    return github[0] if github else "Not Found"


def extract_name(text):
    lines = text.split("\n")

    for line in lines:
        line = line.strip()

        if len(line.split()) >= 2 and len(line) < 40:
            return line

    return "Not Found"
def extract_education(text):

    education_keywords = [
        "B.Tech", "Bachelor", "B.E", "BCA", "B.Sc",
        "M.Tech", "MCA", "M.Sc", "MBA",
        "Intermediate", "12th", "High School", "10th",
        "Diploma"
    ]

    found = []

    for keyword in education_keywords:
        if keyword.lower() in text.lower():
            found.append(keyword)

    if found:
        return ", ".join(found)

    return "Not Found"
def extract_experience(text):

    text = text.lower()

    experience_keywords = [
        "fresher",
        "intern",
        "internship",
        "1 year",
        "2 years",
        "3 years",
        "4 years",
        "5 years",
        "experience"
    ]

    found = []

    for keyword in experience_keywords:
        if keyword in text:
            found.append(keyword.title())

    if found:
        return ", ".join(found)

    return "Fresher"
def extract_projects(text):

    lines = text.split("\n")

    project_keywords = [
        "projects",
        "project"
    ]

    projects = []

    capture = False

    for line in lines:

        line = line.strip()

        if any(keyword in line.lower() for keyword in project_keywords):
            capture = True
            continue

        if capture:

            if line == "":
                break

            projects.append(line)

    if projects:
        return " | ".join(projects[:3])

    return "Not Found"