from dotenv import load_dotenv
import google.generativeai as genai
from scoring import calculate_archetypes
import os

# Load .env and configure Gemini API
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Sample quiz answers for archetype test (replace or expand as needed)
quiz_answers = {
    "Q1": "A",
    "Q2": "C",
    "Q3": "B",
    "Q4": "D",
    "Q5": "A"
}

def get_user_info():
    """Collect user info from terminal input."""
    print("\nPlease enter your information for the cover letter:\n")
    name = input("Name: ")
    job_title = input("Job Title: ")
    skills = input("Key Skills (comma-separated): ").split(",")
    experience = input("Experience (summary): ")

    return {
        "name": name.strip(),
        "job_title": job_title.strip(),
        "skills": [s.strip() for s in skills],
        "experience": experience.strip()
    }

def generate_cover_letter_from_quiz(user_info: dict, quiz_answers: dict) -> str:
    """Generate a Gemini-based cover letter using quiz answers and user info."""
    archetypes_data = calculate_archetypes(quiz_answers)
    archetypes = archetypes_data.get("archetypes", {})

    primary = archetypes.get("Primary", [])
    secondary = archetypes.get("Secondary", [])
    wildcard = archetypes.get("Wildcard", [])

    print("\n🧠 Archetypes Identified:")
    print(f"🔹 Primary  : {', '.join(primary) or 'N/A'}")
    print(f"🔹 Secondary: {', '.join(secondary) or 'N/A'}")
    print(f"🔹 Wildcard : {', '.join(wildcard) or 'N/A'}\n")

    prompt = f"""
    Write a personalized, professional, and motivational cover letter for a job seeker.

    Their career assessment results include:
    - Primary Archetype(s): {', '.join(primary) or 'N/A'}
    - Secondary Archetype(s): {', '.join(secondary) or 'N/A'}
    - Wildcard Archetype(s): {', '.join(wildcard) or 'N/A'}

    Incorporate this archetype blend into the tone, phrasing, and positioning of the letter.

    Here is their user information:
    - Name: {user_info.get('name')}
    - Job Title: {user_info.get('job_title')}
    - Key Skills: {', '.join(user_info.get('skills', []))}
    - Experience: {user_info.get('experience')}

    Make it authentic, engaging, and suitable for a job application.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    user_info = get_user_info()
    print("\n📝 Generating your cover letter...\n")
    letter = generate_cover_letter_from_quiz(user_info, quiz_answers)
    print("📄 Cover Letter:\n")
    print(letter)
