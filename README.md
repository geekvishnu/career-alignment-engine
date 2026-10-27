# Career Alignment & Skill-Gap Analytics Engine

A student enters their skills (with levels) and interests. The system ranks matching careers, shows a skill-gap report
per career, suggests what to learn next, and can compare the profile against any pasted job description.

```
React + Recharts  --HTTP/JSON-->  FastAPI  -->  engine.py (pandas, NumPy, scikit-learn)
                                           -->  nlp.py    (spaCy PhraseMatcher)
                                           -->  db.py     (SQLite history)
```

## How the scoring works
1. **Skill normalisation**: "sklearn", "Scikit Learn" and "scikit-learn" all resolve to one skill (`skills.json` aliases).
2. **TF-IDF cosine similarity**: each career is a weighted skill vector (core=3, important=2, nice=1); TF-IDF makes rare skills count more. The student's vector uses level weights (beginner 0.4, intermediate 0.7, advanced 1.0).
3. **Weighted coverage**: share of a career's required skill weight the student already covers.
4. **Final score** = 55% coverage + 35% cosine + 10% interest match (weights are constants in `engine.py`).
5. **Skill gap**: each required skill is *have* (intermediate+), *partial* (beginner) or *missing*. The roadmap orders gaps by importance, then by how many careers need the skill.
6. **Job-description check**: spaCy finds known skills; sentences with cues like "preferred" or "plus" mark a skill optional.

Grades (CGPA) are displayed as context and never enter the score.

## Run locally
```bash
# backend  (http://localhost:8000/docs)
cd backend && python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest                                                           # run the tests

# frontend (http://localhost:5173)
cd frontend && cp .env.example .env && npm install && npm run dev
```

## API
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/meta` | skill catalogue, careers, interest tags |
| POST | `/api/analyze` | `{skills:[{name,level}], interests, cgpa, target_career}` -> ranked careers + gap reports |
| POST | `/api/jd-gap` | `{text, skills}` -> skills found in a job description + gap |
| GET | `/api/market` | top skills and salary ranges |
| GET | `/api/history` | recent analyses |

## Deploy
**1. GitHub**
```bash
git init && git add . && git commit -m "Career alignment engine"
git branch -M main
git remote add origin https://github.com/<you>/career-engine.git
git push -u origin main
```
**2. Backend on Render (free tier)**: New > Blueprint > pick the repo (it reads `render.yaml`), or create a Web Service with root
directory `backend`, build `pip install -r requirements.txt`, start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
Copy the URL it gives you, e.g. `https://career-engine-api.onrender.com`. Free instances sleep when idle, so the first request can take ~30 s.

**3. Frontend on Vercel**: Add New > Project > import the repo > set **Root Directory** to `frontend` (Vite is auto-detected).
Add env var `VITE_API_URL` = your Render URL (no trailing slash) > Deploy.

**4. Connect them**: in Render set `ALLOWED_ORIGINS` to your Vercel URL (comma-separate multiple), then redeploy the backend.

Why not the backend on Vercel? scikit-learn + pandas + spaCy are close to Vercel's 250 MB function size limit, and SQLite needs a
persistent disk. Render or Railway suit this better. For a persistent history, use a managed PostgreSQL and swap the connection in `db.py`.

## Replace the seed data with real data
`backend/make_data.py` holds the skill dictionary and career profiles. Salary ranges there are **illustrative placeholders**.
Edit, run `python make_data.py`, and for stronger results derive career skill weights from real postings
(count how often each skill appears per role in a cleaned jobs CSV loaded with pandas).
