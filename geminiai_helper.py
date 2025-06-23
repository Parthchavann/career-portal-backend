from dotenv import load_dotenv
import google.generativeai as genai
import os
from scoring import calculate_archetypes  

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_document_from_quiz(user_info: dict, quiz_answers: dict, mode: str = "cover_letter") -> str:
    """
    Generates a personalized document (cover letter or resume) using Gemini based on user's quiz results and input.

    Parameters:
    - user_info (dict): User's name, job title, skills, and experience.
    - quiz_answers (dict): Dictionary of question-answer mappings.
    - mode (str): 'cover_letter' or 'resume'

    Returns:
    - str: Generated text from Gemini.
    """
    # Calculate archetypes from quiz
    archetypes_data = calculate_archetypes(quiz_answers)
    archetypes = archetypes_data.get("archetypes", {})

    primary = archetypes.get("Primary", [])
    secondary = archetypes.get("Secondary", [])
    wildcard = archetypes.get("Wildcard", [])

    # Base prompt components
    archetype_summary = f"""
    - Primary Archetype(s): {', '.join(primary) or 'N/A'}
    - Secondary Archetype(s): {', '.join(secondary) or 'N/A'}
    - Wildcard Archetype(s): {', '.join(wildcard) or 'N/A'}
    """

    user_summary = f"""
    - Name: {user_info.get('name', 'N/A')}
    - Job Title: {user_info.get('job_title', 'N/A')}
    - Key Skills: {', '.join(user_info.get('skills', [])) or 'N/A'}
    - Experience: {user_info.get('experience', 'N/A')}
    """

    # Choose prompt based on mode
    if mode == "resume":
        prompt = f"""
        Create a clean, modern resume for a job seeker using the following details.

        Archetype Assessment Results:
        {archetype_summary}

        User Information:
        {user_summary}

        Include:
        - Contact Info (name)
        - Professional Summary (based on archetypes and experience)
        - Skills
        - Work Experience
        - Customize the tone to reflect their archetype strengths.
        """
    else:  # Default to cover_letter
        prompt = f"""
        Write a personalized, professional, and motivational cover letter for a job seeker.

        Archetype Assessment Results:
        {archetype_summary}

        User Information:
        {user_summary}

        The tone should reflect the user's personality archetypes while staying engaging and suitable for job applications.
        """

    # Generate using Gemini
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text
