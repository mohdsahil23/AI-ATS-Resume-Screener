import sqlite3

conn = sqlite3.connect("candidates.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,
    email TEXT,
    phone TEXT,
    education TEXT,
    experience TEXT,
    projects TEXT,

    linkedin TEXT,
    github TEXT,

    score REAL,

    matched_skills INTEGER,
    found_skills TEXT,
    missing_skills TEXT,

    resume_text TEXT,

    status TEXT
)
""")

conn.commit()


def save_candidate(candidate):

    cursor.execute("""
    INSERT INTO candidates (

        name,
        email,
        phone,
        education,
        experience,
        projects,

        linkedin,
        github,

        score,

        matched_skills,
        found_skills,
        missing_skills,

        resume_text,

        status

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        candidate["Name"],
        candidate["Email"],
        candidate["Phone"],
        candidate["Education"],
        candidate["Experience"],
        candidate["Projects"],

        candidate["LinkedIn"],
        candidate["GitHub"],

        candidate["Score"],

        candidate["Matched Skills"],
        candidate["Found Skills"],
        candidate["Missing Skills"],

        candidate["Resume Text"],

        candidate["Status"]

    ))

    conn.commit()


def get_candidates():

    cursor.execute("""
    SELECT

        name,
        email,
        phone,
        education,
        experience,
        projects,

        linkedin,
        github,

        score,

        matched_skills,
        found_skills,
        missing_skills,

        resume_text,

        status

    FROM candidates

    ORDER BY score DESC
    """)

    rows = cursor.fetchall()

    candidates = []

    for row in rows:

        candidates.append({

            "Name": row[0],
            "Email": row[1],
            "Phone": row[2],
            "Education": row[3],
            "Experience": row[4],
            "Projects": row[5],

            "LinkedIn": row[6],
            "GitHub": row[7],

            "Score": row[8],

            "Matched Skills": row[9],
            "Found Skills": row[10],
            "Missing Skills": row[11],

            "Resume Text": row[12],

            "Status": row[13]

        })

    return candidates