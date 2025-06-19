from dotenv import load_dotenv
import google.generativeai as genai
import os
from scoring import calculate_archetypes  

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_cover_letter_from_quiz(user_info: dict, quiz_answers: dict) -> str:
    """
    Calculates the user's archetypes from quiz answers and generates a Gemini-powered cover letter.

    Parameters:
    - user_info (dict): Dictionary with user's name, job title, skills, and experience.
    - quiz_answers (dict): Dictionary of quiz question-answer mappings.

    Returns:
    - str: Generated cover letter text.
    """
    # Calculate archetypes
    archetypes_data = calculate_archetypes(quiz_answers)
    archetypes = archetypes_data.get("archetypes", {})

    primary = archetypes.get("Primary", [])
    secondary = archetypes.get("Secondary", [])
    wildcard = archetypes.get("Wildcard", [])

    # Construct the Gemini prompt
    prompt = f"""
    Write a personalized, professional, and motivational cover letter for a job seeker.

    Their career assessment results include:
    - Primary Archetype(s): {', '.join(primary) or 'N/A'}
    - Secondary Archetype(s): {', '.join(secondary) or 'N/A'}
    - Wildcard Archetype(s): {', '.join(wildcard) or 'N/A'}

    Incorporate this archetype blend into the tone, phrasing, and positioning of the letter.

    Here is their user information:
    - Name: {user_info.get('name') or 'N/A'}
    - Job Title: {user_info.get('job_title') or 'N/A'}
    - Key Skills: {', '.join(user_info.get('skills') or []) or 'N/A'}
    - Experience: {user_info.get('experience') or 'N/A'}

    Make it authentic, engaging, and suitable for a job application.
    """

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text
