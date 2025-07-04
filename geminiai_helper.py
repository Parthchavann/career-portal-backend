from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_document_from_quiz(user_info: dict, quiz_answers: dict = {}, mode: str = "cover_letter") -> str:
    """
    Generates a personalized document (cover letter or resume) using Gemini based on user's input.

    Parameters:
    - user_info (dict): User's name, job title, skills, and experience.
    - quiz_answers (dict): Optional; kept for compatibility but not used.
    - mode (str): 'cover_letter' or 'resume'

    Returns:
    - str: Generated text from Gemini.
    """

    user_summary = f"""
    - Name: {user_info.get('name', 'N/A')}
    - Job Title: {user_info.get('job_title', 'N/A')}
    - Key Skills: {', '.join(user_info.get('skills', [])) or 'N/A'}
    - Experience: {user_info.get('experience', 'N/A')}
    """

    if mode == "resume":
        prompt = f"""
        Create a clean, modern resume for a job seeker using the following details.

        User Information:
        {user_summary}

        Include:
        - Contact Info (name)
        - Professional Summary
        - Skills
        - Work Experience
        - Customize the tone to reflect the user's strengths.
        """
    else:  # Default to cover_letter
        prompt = f"""
        Write a personalized, professional, and motivational cover letter for a job seeker.

        User Information:
        {user_summary}

        The tone should reflect the user's personality and experience while staying engaging and suitable for job applications.
        """

    # Generate using Gemini
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text
