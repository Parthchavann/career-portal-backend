import os
import requests
from dotenv import load_dotenv
from typing import List, Dict
from scoring import calculate_archetypes

load_dotenv()
ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"

def get_job_roles_and_salaries(keywords: List[str], archetype: str = None) -> List[Dict]:
    """
    Fetches top 3 job roles and salary data using the Adzuna API based on provided keywords.
    Optionally includes a user's archetype to tailor the search further.

    Parameters:
    - keywords (List[str]): List of job-related keywords or skills.
    - archetype (str, optional): User's archetype to add as an additional context keyword.

    Returns:
    - List[Dict]: List of job info including title, company, location, salary, and job link.
    """
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise ValueError("Missing Adzuna API credentials. Check your .env file.")

    results = []
    search_terms = keywords.copy()

    if archetype:
        search_terms.append(archetype)

    for keyword in search_terms:
        params = {
            "app_id": ADZUNA_APP_ID,
            "app_key": ADZUNA_APP_KEY,
            "what": keyword,
            "results_per_page": 3,
            "content-type": "application/json"
        }

        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            for job in data.get("results", [])[:3]:
                results.append({
                    "role": keyword,
                    "title": job.get("title"),
                    "company": job.get("company", {}).get("display_name", "N/A"),
                    "location": job.get("location", {}).get("display_name", "N/A"),
                    "salary": job.get("salary_is_predicted", "0") == "1" and f"~${job.get('salary_min', 'N/A')}" or "N/A",
                    "redirect_url": job.get("redirect_url")
                })

    return results
