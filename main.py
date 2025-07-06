from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, EmailStr
from fastapi import Query
from typing import Optional, Dict
from auth import signup_user, login_user
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
    answers: Dict[str, str]
    email: str
    username: str
    location: Optional[str] = None
    bio: Optional[str] = None
    education: Optional[str] = None
    links: Optional[str] = None

class DocumentRequest(BaseModel):
    user_info: dict
    # quiz_answers: dict

class JobSearchRequest(BaseModel):
    keywords: list[str]
    archetype: str | None = None
    location: str | None = "United States"

class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    username: str

class SignInRequest(BaseModel):
    email: str
    password: str


class UpdateProfileRequest(BaseModel):
    user_id: str
    email: Optional[str]
    username: Optional[str]
    location: Optional[str]
    bio: Optional[str]
    education: Optional[str]
    links: Optional[str]

# ======== Routes ========

@app.get("/")
def read_root():
    return {"message": "Career Portal API is live 🚀"}

@app.post("/submit-quiz")
def submit_quiz(submission: QuizSubmission, user_id: str = Query(..., description="User ID of the quiz taker")):
    try:
        result = calculate_archetypes(submission.answers, user_id=user_id)

        # Update existing user profile, not insert new
        response = supabase.table("user_info_and_history") \
            .update({
                "answers": submission.answers,
                "archetypes": result["archetypes"],
                "location": submission.location,
                "bio": submission.bio,
                "education": submission.education,
                "links": submission.links
            }) \
            .eq("user_id", user_id) \
            .execute()

        if response.get("error"):
            raise HTTPException(status_code=500, detail=response["error"]["message"])

        return {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-cover-letter")
def generate_cover_letter(request: DocumentRequest):
    try:
        letter = generate_document_from_quiz(request.user_info, mode="cover_letter") # removed request.quiz_answers,
        return {"cover_letter": letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-resume")
def generate_resume(request: DocumentRequest):
    try:
        resume = generate_document_from_quiz(request.user_info, mode="resume")  # removed request.quiz_answers,
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
            #archetype=request.archetype,
            location=request.location
        )
        return {"jobs": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/signup")
def signup(request: SignUpRequest):
    try:
        return signup_user(request.email, request.password, request.username)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/signin")
def signin(request: SignInRequest):
    try:
        return login_user(request.email, request.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/update_profile")
def update_profile(data: UpdateProfileRequest):
    try:
        update_data = {k: v for k, v in data.dict().items() if k != "user_id" and v is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="No update fields provided.")

        response = supabase.table("user_info_and_history") \
            .update(update_data) \
            .eq("user_id", data.user_id) \
            .execute()

        if response.get("error"):
            raise HTTPException(status_code=500, detail=response["error"]["message"])

        return {"message": "Profile updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/quiz-history")
def get_quiz_history(user_id: str = Query(..., description="User ID to fetch quiz results for")):
    try:
        response = supabase.table("user_info_and_history") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()

        results = response.data or []

        return {
            "user_id": user_id,
            "history_count": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
