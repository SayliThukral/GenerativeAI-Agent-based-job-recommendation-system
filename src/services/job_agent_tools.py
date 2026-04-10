import requests
import os


def search_jobs_structured(skills: str, experience: str) -> list:
    query = f"{skills} jobs with {experience} experience"
    url   = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key":  os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {"query": query, "num_pages": "1"}

    try:
        response = requests.get(url, headers=headers, params=params)

        print("JSEARCH STATUS:", response.status_code)
        print("JSEARCH RESPONSE:", response.text[:500])  # first 500 chars

        if response.status_code != 200:
            return []

        jobs = response.json().get("data", [])

        result = []
        for job in jobs[:5]:
            result.append({
                "title":   job.get("job_title",       "N/A"),
                "company": job.get("employer_name",   "N/A"),
                "location":job.get("job_city",        "N/A"),
                "link":    job.get("job_apply_link",  "#")
            })

        print("STRUCTURED JOBS:", result)
        return result

    except Exception as e:
        print("JSEARCH ERROR:", e)
        return []
    

def search_jobs_structured_custom_query(query: str) -> list:
    url   = "https://jsearch.p.rapidapi.com/search"

    headers = {
        "X-RapidAPI-Key":  os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    # Pass the raw query straight to the API
    params = {"query": query, "num_pages": "1"}

    try:
        response = requests.get(url, headers=headers, params=params)

        print("JSEARCH STATUS:", response.status_code)
        print("JSEARCH RESPONSE:", response.text[:500])  # first 500 chars

        if response.status_code != 200:
            return []

        jobs = response.json().get("data", [])

        result = []
        for job in jobs[:5]:
            result.append({
                "title":   job.get("job_title",       "N/A"),
                "company": job.get("employer_name",   "N/A"),
                "location":job.get("job_city",        "N/A"),
                "link":    job.get("job_apply_link",  "#")
            })

        print("STRUCTURED JOBS:", result)
        return result

    except Exception as e:
        print("JSEARCH ERROR:", e)
        return []

def search_jobs(skills: str, experience: str) -> str:
    # 🔹 Create query from user input
    query = f"{skills} jobs with {experience} experience"

    # 🔹 API endpoint
    url = "https://jsearch.p.rapidapi.com/search"

    # 🔹 Headers (API key from .env)
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    # 🔹 Query parameters
    params = {
        "query": query,
        "num_pages": "1"
    }

    try:
        # 🔹 API call
        response = requests.get(url, headers=headers, params=params)

        # 🔹 Check if request successful
        if response.status_code != 200:
            return "❌ Error fetching jobs from API"

        # 🔹 Convert response to JSON
        data = response.json()

        # 🔹 Extract job list
        jobs = data.get("data", [])

        # 🔹 If no jobs found
        if not jobs:
            return "❌ No jobs found"

        # 🔹 Format results
        result = []
        for job in jobs[:5]:  # top 5 jobs
            title = job.get("job_title", "N/A")
            company = job.get("employer_name", "N/A")
            location = job.get("job_city", "N/A")
            apply_link = job.get("job_apply_link", "N/A")

            result.append(
                f"🔹 {title}\n🏢 {company}\n📍 {location}\n🔗 Apply here: {apply_link}\n"
            )

        # 🔹 Return final output
        return "\n".join(result)

    except Exception as e:
        return f"❌ Something went wrong: {str(e)}"