SYSTEM_PROMPT = """
You are an expert Resume Parsing AI.
Extract ONLY technical skills from the resume.
Return output strictly as a Python list.
"""

def build_skills_prompt(raw_text: str):
    return f"""
Extract ONLY technical skills from the following resume.
Do not include name, email, phone.
Return strictly as a Python list.

Resume Text:
\"\"\"{raw_text}\"\"\"
"""