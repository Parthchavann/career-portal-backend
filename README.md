# career-portal-backend
Final Data Flow:
1. User Takes Assessment (Frontend)
•	57 questions (pulled from the PDF)
•	Each question has 4 choices → each choice maps to one or more archetypes
•	Answers submitted → sent to backend
2. Backend Evaluation (FastAPI)
•	scoring.py uses a mapping dictionary to evaluate the score across 8 archetypes
•	Highest scores determine top 2 archetypes for the user
3. Result Display (Frontend)
•	User sees:
o	Top 2 Archetypes (e.g., "Creative Maverick", "Visionary Coach")
o	Associated roles (e.g., UX Designer, Career Counselor)
o	Chart.js visual showing score breakdown
o	Download as PDF (frontend-generated, e.g., using jspdf)
4. Salary + Job Role Info
•	Use Piloterr Glassdoor API 
•	Fetch:
o	Job Titles based on archetypes
o	Average salary ranges
o	Skills required (optional enhancement)
5. Resume Upload & JD Upload
•	User uploads resume + sample job description
•	ats.py compares both using TfidfVectorizer + cosine similarity
•	Return match score (%) and suggestions

6. Cover Letter Generator
•	openai_helper.py takes:
o	Resume text
o	Job Description
o	User archetype/personality
•	Returns a custom GPT-generated cover letter
7. Chatbot Support
•	Small FAQ bot (can be rule-based or GPT-powered)
•	Users can ask:
o	"What is this quiz for?"
o	"What does a Grounded Architect do?"
________________________________________

Tools & Tech Stack:
Feature	Tools
Frontend	React.js, Tailwind CSS
Backend API	FastAPI
Archetype Scoring	Python, Pandas
Resume Analysis	TfidfVectorizer, cosine
Cover Letter	OpenAI API (gpt-4/gpt-3.5)
Job/Salary Info	Piloterr Glassdoor API
PDF Export	jsPDF, html2canvas
Deployment	Vercel (Frontend), Render (Backend)

Which Tasks Should Be Done First (Stepwise / Sequential):
These are core foundation tasks that need to be done in order:
1.	GitHub repo setup & folder structure (Tech Lead)
2.	Design data flow & finalize API structure (Tech Lead)
3.	Backend API routes scaffolding (Backend 1 & 2)
o	Define the quiz scoring endpoint, resume analysis, cover letter, and chatbot routes (even if logic is not final yet).
4.	Frontend React setup + basic routing (Frontend 1 & 2)
o	Just creating working React pages and connecting to test backend endpoints.
Which Tasks Can Be Done in Parallel (Randomly or Independently):
Once the above is done, most tasks can run in parallel:
•	Quiz logic (Backend 1) and Quiz UI (Frontend 1) can work independently if API contract is defined.
•	Resume + JD analysis (Backend 2) can be built while Frontend 2 builds upload UI.
•	Cover letter GPT logic (Backend 2) and UI rendering (Frontend 2) can be done side by side.
•	Chatbot API (Backend 2) and Chatbot widget UI (Frontend 2) can proceed independently.
•	Salary/job role API (Tech Lead) and display integration (Frontend 1) can be done after quiz results are ready.
Final Integration (Should Be Stepwise):
1.	Connect quiz UI → backend scoring API.
2.	Connect resume/JD upload → similarity + GPT cover letter.
3.	Connect job role display → salary API.
4.	Add chatbot.
5.	Enable PDF export.
6.	Deploy (Vercel + Render/Heroku).

👨‍💻 Backend Developer 1 (Taylor)
Focus: Quiz scoring + cover letter generation
🧠 Tasks:
•	scoring.py:
o	Implement scoring logic (57 questions → archetype)
•	openai_helper.py:
o	GPT-based cover letter generator (basic prompt logic)
•	API routes:
o	/submit-quiz → returns archetype
o	/generate-cover-letter → returns GPT output
________________________________________
👨‍💻 Backend Developer 2 
Focus: Resume analysis + job role matching
🧠 Tasks:
•	ats.py:
o	Extract text from resume & JD (use PyMuPDF)
o	Compare using TfidfVectorizer + cosine similarity
•	/analyze-resume route → returns % match
•	Integrate Piloterr API for job roles/salaries
•	Return top 3 matched roles with salary info

