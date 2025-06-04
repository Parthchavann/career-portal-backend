# P2P Assessment API

FastAPI backend for quiz scoring and GPT-based cover letter generation.

## Endpoints

- `POST /submit-quiz`: Returns primary, secondary, and wildcard archetypes.
- `POST /generate-cover-letter`: Returns a GPT-generated cover letter.

## Deployment

Deploy on Render. Make sure to set `OPENAI_API_KEY` as an environment variable.

## Frontend

Use jsPDF to export the generated letter to PDF.