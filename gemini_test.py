from dotenv import load_dotenv
import google.generativeai as genai
from scoring import calculate_archetypes
import os

# Load .env and configure Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Simulated quiz answers (change as needed for testing)
quiz_answers = {
    "Q1": "A",
    "Q2": "C",
    "Q3": "B",
    "Q4": "D",
    "Q5": "A"
}

def get_user_info():
    """Collect user info from terminal input."""
    print("\n🔧 Please enter your information:\n")
    name = input("👤 Name: ")
    job_title = input("💼 Job Title: ")
    skills = input("🛠️  Key Skills (comma-separated): ").split(",")
    experience = input("📘 Experience (summary): ")

    return {
        "name": name.strip(),
        "job_title": job_title.strip(),
        "skills": [s.strip() for s in skills],
        "experience": experience.strip()
    }

def calculate_and_display_archetypes(quiz_answers):
    """Calculates and prints archetypes."""
    archetypes_data = calculate_archetypes(quiz_answers)
    archetypes = archetypes_data.get("archetypes", {})

    print("\n🧠 Archetypes Identified:")
    print(f"🔹 Primary  : {', '.join(archetypes.get('Primary', [])) or 'N/A'}")
    print(f"🔹 Secondary: {', '.join(archetypes.get('Secondary', [])) or 'N/A'}")
    print(f"🔹 Wildcard : {', '.join(archetypes.get('Wildcard', [])) or 'N/A'}\n")

    return archetypes

def generate_cover_letter(user_info: dict, archetypes: dict) -> str:
    """Generate cover letter using Gemini API."""
    prompt = f"""
    Write a personalized, professional, and motivational cover letter for a job seeker.

    Their career assessment results include:
    - Primary Archetype(s): {', '.join(archetypes.get("Primary", [])) or 'N/A'}
    - Secondary Archetype(s): {', '.join(archetypes.get("Secondary", [])) or 'N/A'}
    - Wildcard Archetype(s): {', '.join(archetypes.get("Wildcard", [])) or 'N/A'}

    Here is their user information:
    - Name: {user_info['name']}
    - Job Title: {user_info['job_title']}
    - Key Skills: {', '.join(user_info['skills'])}
    - Experience: {user_info['experience']}

    Make it authentic, engaging, and suitable for a job application.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

def generate_resume(user_info: dict, archetypes: dict) -> str:
    """Generate resume using Gemini API."""
    prompt = f"""
    Create a clean, professional resume for a job seeker.

    Include the following sections:
    - Contact Info (Name)
    - Professional Summary (based on archetype and experience)
    - Skills
    - Work Experience (based on input)
    - Optional: Tailor tone and strengths to match their archetypes

    Their archetype assessment results:
    - Primary Archetype(s): {', '.join(archetypes.get("Primary", [])) or 'N/A'}
    - Secondary Archetype(s): {', '.join(archetypes.get("Secondary", [])) or 'N/A'}
    - Wildcard Archetype(s): {', '.join(archetypes.get("Wildcard", [])) or 'N/A'}

    User Info:
    - Name: {user_info['name']}
    - Job Title: {user_info['job_title']}
    - Key Skills: {', '.join(user_info['skills'])}
    - Experience: {user_info['experience']}
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    user_info = get_user_info()
    archetypes = calculate_and_display_archetypes(quiz_answers)

    print("📄 What would you like to generate?")
    print("1. Cover Letter")
    print("2. Resume")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        print("\n✍️ Generating Cover Letter...\n")
        result = generate_cover_letter(user_info, archetypes)
    elif choice == "2":
        print("\n📃 Generating Resume...\n")
        result = generate_resume(user_info, archetypes)
    else:
        print("❌ Invalid choice. Exiting.")
        exit()

    print("✅ Output:\n")
    print(result)
