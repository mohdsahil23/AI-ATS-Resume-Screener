import streamlit as st
import PyPDF2
import pandas as pd
from ai_analyzer import analyze_resume
from database import save_candidate, get_candidates
from report_generator import generate_pdf

from parser import (
    extract_name,
    extract_email,
    extract_phone,
    extract_linkedin,
    extract_github,
    extract_education,
    extract_experience,
    extract_projects
   )

# Page Settings
st.set_page_config(
    page_title="ATS Resume Screener",
    page_icon="📄"
)

# Title
st.title("📄 ATS Resume Screener")

with st.sidebar:

    st.title("📋 Menu")

    st.success("Version 1.0")

    st.write("Developer: Mo Sahil Ansari")

    st.divider()

    st.info("""
### Features

✅ Resume Upload

✅ Multiple Resume Upload

✅ ATS Matching

✅ Candidate Ranking

✅ Candidate Profile

✅ SQLite Database

✅ PDF Export

✅ Excel Export

⚠ AI Analysis (Temporarily Disabled)
""")

st.write("Upload your Resume PDF(s)")

# Upload Multiple Resumes
resumes = st.file_uploader(
    "📂 Upload Resume(s) (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

# Upload Job Description
jd = st.file_uploader(
    "Upload Job Description (.txt)",
    type=["txt"]
)

# Skills Database
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

# Read JD only once
jd_text = ""
jd_skills = []

if jd is not None:
    jd_text = jd.read().decode("utf-8").lower()

    for skill in skills:
        if skill in jd_text:
            jd_skills.append(skill)

results = []

# Process Every Resume
if resumes:

    for resume in resumes:

        reader = PyPDF2.PdfReader(resume)

        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text
        original_text = resume_text
        resume_text = resume_text.lower()
        name = extract_name(original_text)
        email = extract_email(original_text)
        phone = extract_phone(original_text)
        linkedin = extract_linkedin(original_text)
        github = extract_github(original_text)
        education = extract_education(original_text)
        experience = extract_experience(original_text)
        projects = extract_projects(original_text)

        found_skills = []

        for skill in skills:
            if skill in resume_text:
                found_skills.append(skill)

        matched = []
        missing = []

        for skill in jd_skills:
            if skill in found_skills:
                matched.append(skill)
            else:
                missing.append(skill)

        if len(jd_skills) > 0:
            score = (len(matched) / len(jd_skills)) * 100
        else:
            score = 0

        if score >= 80:

                status = "🟢 Shortlisted"

        elif score >= 60:

                status = "🟡 Review"

        else:

                status = "🔴 Rejected"


        results.append({

            "Resume": resume.name,

            "Name": name,

            "Email": email,

            "Phone": phone,

            "Education": education,

            "Experience": experience,

            "Projects": projects,

            "LinkedIn": linkedin,

            "GitHub": github,

            "Score": round(score, 2),

            "Matched Skills": len(matched),

            "Missing Skills": ", ".join(missing),

            "Found Skills": ", ".join(found_skills),
            
            "Resume Text": original_text,

            "Status": status

        })
        
        results[-1]["Status"] = status

        save_candidate(results[-1])
# Show Results
# ===========================
# SHOW RESULTS
# ===========================

if results:

    # Sort by ATS Score
    results = sorted(
        results,
        key=lambda x: x["Score"],
        reverse=True
    )

    total_resumes = len(results)

    avg_score = round(
        sum(r["Score"] for r in results) / total_resumes,
        2
    )

    highest_score = results[0]["Score"]
    top_candidate = results[0]["Name"]

    # Dashboard Cards
    st.subheader("📊 ATS Dashboard")
    if st.button("📂 Saved Candidates"):
        st.session_state["show_saved"] = True

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📄 Total", total_resumes)
    col2.metric("⭐ Average", f"{avg_score}%")
    col3.metric("🏆 Top Candidate", top_candidate)
    col4.metric("📈 Highest", f"{highest_score}%")

    st.divider()

    # Search
    search = st.text_input(
        "🔍 Search Candidate"
    )

    st.subheader("🏆 Candidate Ranking")

    rank = 1

    for candidate in results:

        if search:

            if search.lower() not in candidate["Name"].lower():
                continue

        with st.container(border=True):

            c1, c2, c3, c4, c5 = st.columns([1,3,2,2,2])

            c1.markdown(f"### {rank}")

            c2.write(candidate["Name"])

            c3.write(f"**{candidate['Score']}%**")

            c4.write(candidate["Status"])

            if c5.button(
                "👁 View",
                key=f"view_{rank}"
            ):

                st.session_state["selected_candidate"] = candidate

            rank += 1

    # Candidate Profile
    if "selected_candidate" in st.session_state:

        c = st.session_state["selected_candidate"]

        st.divider()

        col1, col2 = st.columns([5, 1])

        with col1:
            st.subheader("👤 Candidate Profile")

        with col2:
            if st.button("❌ Close Profile"):
                del st.session_state["selected_candidate"]
                st.rerun()

        st.write(f"### {c['Name']}")

        info1, info2 = st.columns(2)

        with info1:
            st.info(f"📧 Email\n\n{c['Email']}")

        with info2:
            st.info(f"📱 Phone\n\n{c['Phone']}")

        st.subheader("🎓 Education")
        st.write(c["Education"])

        st.subheader("💼 Experience")
        st.write(c["Experience"])

        st.subheader("📂 Projects")
        st.write(c["Projects"])

        st.subheader("💻 Skills")
        st.success(c["Found Skills"])

        st.subheader("❌ Missing Skills")
        st.error(c["Missing Skills"])

        st.subheader("🔗 LinkedIn")
        st.write(c["LinkedIn"])

        st.subheader("🐙 GitHub")
        st.write(c["GitHub"])

        st.subheader("📊 ATS Score")

        st.progress(c["Score"] / 100)
        st.success(f"{c['Score']}% Match")
        st.divider()

        if st.button("📄 Export Candidate PDF"):

            pdf_file = f"reports/{c['Name']}_Report.pdf"

            generate_pdf(c, pdf_file)

            with open(pdf_file, "rb") as file:

                st.download_button(
                    label="⬇ Download PDF Report",
                    data=file,
                    file_name=f"{c['Name']}_Report.pdf",
                    mime="application/pdf"
            )
                
        st.divider()

        # st.subheader("🤖 AI Resume Analysis")

        # if st.button(
        #     "🤖 Analyze Resume",
        #     key=f"ai_{c['Email']}"
        # ):

        #     if not jd_text:
        #         st.warning("⚠️ Please upload Job Description first.")

        #     else:
        #         try:
        #             with st.spinner("AI is analyzing the resume..."):

        #                 analysis = analyze_resume(
        #                     c["Resume Text"],
        #                     jd_text
        #                 )

        #             st.success("✅ Analysis Complete")
        #             st.markdown(analysis)

        #         except Exception as e:
        #             st.error(f"AI Analysis failed: {e}")       

        st.write("### 📋 Resume Summary")

        summary = (
            f"{c['Name']} has an ATS score of {c['Score']}%. "
            f"The resume contains {c['Matched Skills']} matched skills."
        )

        st.info(summary)

        # Strengths
        st.write("### ✅ Strengths")

        if c["Found Skills"]:
            st.success(c["Found Skills"])
        else:
            st.warning("No skills detected.")

        # Missing Skills
        st.write("### ❌ Missing Skills")

        if c["Missing Skills"]:
            st.error(c["Missing Skills"])
        else:
            st.success("No missing skills.")

        # Suggestions
        st.write("### 💡 Suggestions")

        if c["Score"] >= 80:
            st.success("Excellent resume. Ready for interview.")

        elif c["Score"] >= 60:
            st.warning(
                "Improve missing skills and add more projects."
            )

        else:
            st.error(
                "Resume needs major improvements."
            )

        # Hiring Recommendation
        st.write("### 🎯 Hiring Recommendation")

        if c["Score"] >= 80:
            st.success("🟢 Recommended")

        elif c["Score"] >= 60:
            st.warning("🟡 Consider")

        else:
            st.error("🔴 Not Recommended")

            # ===========================
# Saved Candidates
# ===========================

if st.session_state.get("show_saved", False):

    st.divider()
    st.subheader("📂 Saved Candidates")

    saved = get_candidates()

    if len(saved) == 0:
        st.info("No candidates found.")

    else:

        for i, candidate in enumerate(saved, start=1):

            with st.expander(
                f"{i}. {candidate['Name']} | {candidate['Score']}% | {candidate['Status']}"
            ):

                st.write("**Email:**", candidate["Email"])
                st.write("**Phone:**", candidate["Phone"])
                st.write("**Education:**", candidate["Education"])
                st.write("**Experience:**", candidate["Experience"])
                st.write("**Projects:**", candidate["Projects"])
                st.write("**Skills:**", candidate["Found Skills"])
st.divider()

st.subheader("📥 Export Reports")

if st.button("📊 Export to Excel"):

    export_df = pd.DataFrame(results)

    file_path = "reports/ATS_Report.xlsx"

    export_df.to_excel(file_path, index=False)

    st.success("✅ Excel Report Generated Successfully!")

    with open(file_path, "rb") as file:

        st.download_button(
            label="⬇ Download Excel Report",
            data=file,
            file_name="ATS_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

st.divider()

st.caption(
    "© 2026 AI ATS Resume Screener | Developed by Sahil Ansari"
)        