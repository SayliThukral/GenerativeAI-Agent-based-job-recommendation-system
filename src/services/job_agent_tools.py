import requests
import os


# ─────────────────────────────────────────────
#  Internal helper — single source of truth
#  for all JSearch calls.
# ─────────────────────────────────────────────
def _jsearch(query: str, num_results: int = 5) -> list:
    """
    Call JSearch with a pre-built query string and return a clean list of jobs.
    Returns [] on any error or empty result — never raises.
    """
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key":  os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }
    params = {"query": query, "num_pages": "1"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"JSEARCH QUERY : {query!r}")
        print(f"JSEARCH STATUS: {response.status_code}")
        print(f"JSEARCH SNIPPET: {response.text[:300]}")

        if response.status_code != 200:
            return []

        jobs = response.json().get("data", [])
        result = [
            {
                "title":    job.get("job_title",      "N/A"),
                "company":  job.get("employer_name",  "N/A"),
                "location": job.get("job_city",       "N/A"),
                "link":     job.get("job_apply_link", "#"),
            }
            for job in jobs[:num_results]
        ]
        print(f"JSEARCH RESULTS ({len(result)}): {result}")
        return result

    except Exception as e:
        print(f"JSEARCH ERROR: {e}")
        return []


# ─────────────────────────────────────────────
#  Public API
# ─────────────────────────────────────────────

def search_jobs_by_domain(domain: str, location: str = "") -> list:
    """
    PRIMARY function — search by professional domain (e.g. 'ML Engineer').
    This produces the most relevant results and should be the first call.

    Falls back to a broader query if the first attempt returns nothing.

    Args:
        domain   : The candidate's domain from resume parsing, e.g. "ML Engineer".
        location : Optional city/country string to narrow results.

    Returns:
        List of job dicts with keys: title, company, location, link.
    """
    # Build a clean, natural-language query JSearch handles well
    base_query = f"{domain} jobs"
    query = f"{base_query} in {location}" if location else base_query

    jobs = _jsearch(query)

    # Fallback 1: drop location if it was set and returned nothing
    if not jobs and location:
        print("JSEARCH FALLBACK: dropping location filter")
        jobs = _jsearch(base_query)

    # Fallback 2: strip sub-specialisation (e.g. "ML Engineer" → "Engineer")
    if not jobs and " " in domain:
        broad = domain.split()[-1] + " jobs"
        print(f"JSEARCH FALLBACK: broadening to {broad!r}")
        jobs = _jsearch(broad)

    return jobs


def search_jobs_structured(skills: list | str, experience: str, domain: str = "") -> list:
    """
    Search by domain first (best results), then fall back to skills-based query.

    Args:
        skills     : List of skill strings, or a comma-separated string.
        experience : Experience level string, e.g. "2 years".
        domain     : Optional domain hint (e.g. "ML Engineer"). Preferred over raw skills.

    Returns:
        List of job dicts with keys: title, company, location, link.
    """
    # ── Normalise skills to a clean string ──────────────────────────────────
    if isinstance(skills, list):
        skills_str = ", ".join(s.strip() for s in skills if s.strip())
    else:
        skills_str = str(skills).strip()

    # ── Domain-first strategy (most reliable) ───────────────────────────────
    if domain:
        jobs = search_jobs_by_domain(domain)
        if jobs:
            return jobs

    # ── Skills-based fallback (use only first 2 skills to keep query clean) ─
    top_skills = [s.strip() for s in skills_str.split(",")][:2]
    query = " ".join(top_skills) + " developer jobs"
    return _jsearch(query)


def search_jobs_structured_custom_query(query: str) -> list:
    """
    Search with a fully custom, pre-built query string.
    Use this when you want complete control over what is sent to JSearch.

    Args:
        query: Any natural-language query, e.g. "Python backend engineer remote".

    Returns:
        List of job dicts with keys: title, company, location, link.
    """
    return _jsearch(query)


def search_jobs(skills: list | str, experience: str, domain: str = "") -> str:
    """
    Human-readable formatted job search (used for plain-text display).
    Delegates to search_jobs_structured internally.

    Returns:
        Formatted string of jobs, or an error message.
    """
    jobs = search_jobs_structured(skills, experience, domain)

    if not jobs:
        return "❌ No jobs found. Try broadening your search or check your API key."

    lines = []
    for job in jobs:
        lines.append(
            f"🔹 {job['title']}\n"
            f"🏢 {job['company']}\n"
            f"📍 {job['location']}\n"
            f"🔗 Apply: {job['link']}\n"
        )
    return "\n".join(lines)