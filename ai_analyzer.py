import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read API Key
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Model
model = genai.GenerativeModel("gemini-2.0-flash")

def analyze_resume(resume_text, jd_text):

    prompt = f"""
You are an expert ATS recruiter.

Job Description:
{jd_text}

Candidate Resume:
{resume_text}

Analyze the resume and provide:

1. Resume Summary
2. Strengths
3. Weaknesses
4. Missing Skills
5. Interview Recommendation
6. ATS Improvement Tips

Keep the response professional and easy to read.
"""

    response = model.generate_content(prompt)

    return response.text