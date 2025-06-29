from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from fastapi import Query
from scoring import calculate_archetypes
from geminiai_helper import generate_document_from_quiz
from fastapi.middleware.cors import CORSMiddleware
from ats import extract_text_from_pdf, compute_similarity
from adzuna import get_job_roles_and_salaries
from supabase import create_client
from dotenv import load_dotenv
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ======== Data Models ========
class QuizSubmission(BaseModel):
    answers: dict

class DocumentRequest(BaseModel):
    user_info: dict
    quiz_answers: dict

class JobSearchRequest(BaseModel):
    keywords: list[str]
    archetype: str | None = None
    location: str | None = "United States"

# ======== Routes ========

@app.post("/submit-quiz")
def submit_quiz(submission: QuizSubmission, user_id: str = "guest_user"):
    try:
        result = calculate_archetypes(submission.answers, user_id=user_id)
        return {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-cover-letter")
def generate_cover_letter(request: DocumentRequest):
    try:
        letter = generate_document_from_quiz(request.user_info, request.quiz_answers, mode="cover_letter")
        return {"cover_letter": letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-resume")
def generate_resume(request: DocumentRequest):
    try:
        resume = generate_document_from_quiz(request.user_info, request.quiz_answers, mode="resume")
        return {"resume": resume}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-resume")
async def analyze_resume(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as resume_tmp, tempfile.NamedTemporaryFile(delete=False) as jd_tmp:
            resume_tmp.write(await resume.read())
            jd_tmp.write(await jd.read())

        resume_text = extract_text_from_pdf(resume_tmp.name)
        jd_text = extract_text_from_pdf(jd_tmp.name)

        match_score = compute_similarity(resume_text, jd_text)
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

@app.post("/search-jobs")
def search_jobs(request: JobSearchRequest):
    try:
        results = get_job_roles_and_salaries(
            keywords=request.keywords,
            archetype=request.archetype,
            location=request.location
        )
        return {"jobs": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/quiz-history")
def get_quiz_history(user_id: str = Query(..., description="User ID or email to fetch quiz results for")):
    try:
        response = supabase.table("quiz_results") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .limit(10) \
            .execute()

        results = response.data or []

        return {
            "user_id": user_id,
            "history_count": len(results),
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
