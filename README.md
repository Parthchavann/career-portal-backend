# P2P Assessment API

FastAPI backend for:
- Archetype-based quiz scoring  
- GPT-powered cover letter and resume generator  
- Resume analysis and job-role matching using TF-IDF and ADZUNA

## Endpoints

- `POST /submit-quiz`:  
  Returns primary, secondary, and wildcard archetypes based on answers.

- `POST /generate-resume`:  
  Returns a GPT-generated resume based on user info and archetype.

- `POST /generate-cover-letter`:  
  Returns a GPT-generated cover letter based on user info and archetype.

- `POST /analyze-resume`:  
  Accepts resume and job description files (PDF).  
  Uses PyMuPDF, TF-IDF, and cosine similarity to return a percentage match score.

- `GET /search-jobs=`:  
  Integrates with the Adzuna API to return the top 3 job roles and average salary based on the user's archetype.


## Tech Stack

- **FastAPI** for backend API
- **PyMuPDF** for PDF text extraction
- **scikit-learn** for TF-IDF vectorization and cosine similarity
- **Gemini-2.0-Flash API** for LLM-based cover letter generation
- **ADZUNA API** for real-time job role and salary insights

## Deployment

Make sure to set the following environment variables:

- `GEMINI_API_KEY`
- `ADZUN_APP_ID`
- `ADZUNA_API_KEY`

- Use **jsPDF** or browser print tools to export the generated cover letter to PDF.



