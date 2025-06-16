from dotenv import load_dotenv
import os
import requests

load_dotenv()
api_key = os.getenv("PILOTERR_API_KEY")

def get_job_roles_and_salaries(keywords):
    url = 'https://piloterr.com/api/v2/glassdoor/job-search'
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }
    results = []

    for keyword in keywords:
        params = {"query": keyword, "limit": 1}
        res = requests.get(url, headers=headers, params=params)
        
        if res.status_code == 200:
            jobs = res.json().get("jobs", [])
            if jobs:
                job = jobs[0]
                results.append({
                    "role": keyword,
                    "company": job.get("company_name"),
                    "location": job.get("location"),
                    "salary": job.get("salary", "N/A")
                })
    
    return results