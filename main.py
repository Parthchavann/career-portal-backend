from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from scoring import calculate_archetypes
from geminiai_helper import generate_cover_letter_from_quiz
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from ats import extract_text_from_pdf, compute_similarity
from adzuna import get_job_roles_and_salaries
import tempfile
import os

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
    archetype: dict


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
        letter = generate_cover_letter_from_quiz(request.user_info, request.archetype)
        return {"cover_letter": letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New endpoint for resume analysis + job role matching
@app.post("/analyze-resume")
async def analyze_resume(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as resume_tmp, tempfile.NamedTemporaryFile(delete=False) as jd_tmp:
            resume_tmp.write(await resume.read())
            jd_tmp.write(await jd.read())

        resume_text = extract_text_from_pdf(resume_tmp.name)
        jd_text = extract_text_from_pdf(jd_tmp.name)

        match_score = compute_similarity(resume_text, jd_text)

        # Simple keyword extraction 
        common_keywords = list(set(jd_text.lower().split()) & set(resume_text.lower().split()))
        top_keywords = list(dict.fromkeys(common_keywords))[:3]

        roles_with_salary = get_job_roles_and_salaries(top_keywords)

        os.unlink(resume_tmp.name)
        os.unlink(jd_tmp.name)

        return {
            "match_score": f"{match_score}%",
            "top_roles": roles_with_salary
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
