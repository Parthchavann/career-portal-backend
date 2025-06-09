from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scoring import calculate_archetypes
from openai_helper import generate_cover_letter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizSubmission(BaseModel):
    answers: dict

class CoverLetterRequest(BaseModel):
    user_info: dict
    archetype: str

@app.post("/submit-quiz")
def submit_quiz(submission: QuizSubmission):
    try:
        result = calculate_archetypes(submission.answers)
        return  {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-cover-letter")
def generate_letter(request: CoverLetterRequest):
    try:
        letter = generate_cover_letter(request.user_info, request.archetype)
        return {"cover_letter": letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
