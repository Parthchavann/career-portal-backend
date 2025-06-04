from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_cover_letter(user_info: dict, archetype: str) -> str:
    prompt = f"""
Write a personalized, engaging cover letter for someone whose top archetype is '{archetype}'. 
Include elements from the user's info: {user_info}. Keep it professional yet inspirational.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert career advisor and resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=600
    )
    return response['choices'][0]['message']['content']