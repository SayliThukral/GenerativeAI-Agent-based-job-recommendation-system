import re
from src.services.job_agent_tools import search_jobs_structured
from dotenv import load_dotenv
from src.services.job_agent_tools import search_jobs_structured, search_jobs_structured_custom_query

load_dotenv()

def clean_experience_string(exp_string: str) -> str:
    """Extracts just the years of experience or simplifies the string."""
    # Example: Grabs just the "0-2 years" or "entry-level" part
    # A simple split to remove the actionable advice after the hyphen
    clean_str = exp_string.split(" - ")[0].strip()
    return clean_str

def get_job_recommendations(skills: list, experience: list) -> list:
    # 1. Clean the skills
    skills_str = ", ".join(skills) if skills else "software developer"
    
    # 2. Extract a safe experience term (fallback to empty string if it's weird)
    exp_term = ""
    if experience:
        first_exp = experience[0].split(" - ")[0].strip().lower()
        # Only use it if it contains words like 'year', 'month', 'entry', 'senior', 'junior'
        if any(keyword in first_exp for keyword in ['year', 'month', 'entry', 'junior', 'senior', 'level']):
            exp_term = first_exp
    
    # 3. Construct a smarter query
    if exp_term:
        query = f"{skills_str} jobs {exp_term} experience"
    else:
        # If the LLM gave us garbage like "Master's degree", just search by skills
        query = f"{skills_str} jobs" 
        
    return search_jobs_structured_custom_query(query)