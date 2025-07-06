from supabase import create_client
from dotenv import load_dotenv
from fastapi import HTTPException
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("Supabase credentials are missing in .env")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def signup_user(email: str, password: str, username: str):
    try:
        # Create auth user
        response = supabase.auth.sign_up({"email": email, "password": password})

        if response.error:
            raise HTTPException(status_code=400, detail=response.error.message)

        user = response.user
        if not user:
            raise HTTPException(status_code=400, detail="Failed to create user.")

        user_id = user.id

        # Insert initial profile
        insert_response = supabase.table("user_info_and_history").insert({
            "user_id": user_id,
            "username": username,
            "email": email,
            "answers": {},         # empty JSON object
            "archetypes": {},      # empty JSON object
            "location": None,
            "bio": None,
            "education": None,
            "links": None
        }).execute()

        if insert_response.error:
            raise HTTPException(status_code=500, detail=insert_response.error.message)

        return {"message": "User created successfully.", "user_id": user_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def login_user(email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})

        if response.error:
            raise HTTPException(status_code=401, detail=response.error.message)

        session = response.session
        user = response.user

        if not session or not user:
            raise HTTPException(status_code=401, detail="Login failed.")

        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "user": {
                "id": user.id,
                "email": user.email
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
