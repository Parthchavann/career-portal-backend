from scoring import calculate_archetypes
from adzuna import get_job_roles_and_salaries
import os
from dotenv import load_dotenv

# Load API credentials
load_dotenv()

# Example quiz answers (mocked like user selected options from a quiz)
quiz_answers = {
    "Q1": "A",
    "Q2": "C",
    "Q3": "D",
    "Q4": "B",
    "Q5": "A"
}

def main():
    print("🔎 Adzuna Job Search Test\n")

    # Step 1: Calculate archetypes from quiz answers
    print("Calculating career archetype...")
    result = calculate_archetypes(quiz_answers)
    archetypes = result.get("archetypes", {})
    primary = archetypes.get("Primary", ["N/A"])[0]
    print(f"Your primary archetype is: {primary}\n")

    # Step 2: Ask user for job keyword
    keyword = input("Enter a job title or keyword to search on Adzuna (e.g., 'data analyst', 'software engineer'): ").strip()
    if not keyword:
        print("❌ No keyword entered. Exiting.")
        return

    # Step 3: Search Adzuna
    print(f"\n🔍 Searching top 3 jobs for '{keyword}' with archetype '{primary}'...\n")
    jobs = get_job_roles_and_salaries([keyword], archetype=primary)

    if not jobs:
        print("⚠️ No jobs found for your input.")
    else:
        top_jobs = jobs[:3]  # Explicitly limit to top 3 results
        for idx, job in enumerate(top_jobs, 1):
            print(f"🔸 Job #{idx}")
            print(f"   🏷️  Title   : {job.get('title')}")
            print(f"   🏢 Company : {job.get('company')}")
            print(f"   📍 Location: {job.get('location')}")
            print(f"   💰 Salary  : {job.get('salary')}")
            print(f"   🔗 Link    : {job.get('redirect_url')}")
            print("-" * 50)

if __name__ == "__main__":
    main()
