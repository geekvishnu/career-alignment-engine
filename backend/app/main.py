import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import db, engine
from .nlp import extract_requirements
from .schemas import AnalyzeRequest, JDRequest


@asynccontextmanager
async def lifespan(_: FastAPI):
    db.init()
    yield


app = FastAPI(title="Career Alignment & Skill-Gap Analytics Engine", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_methods=["*"], allow_headers=["*"],
                   allow_origins=[o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")])


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/meta")
def meta():
    """Everything the form needs: skill catalogue, careers and interest tags."""
    return {"skills": [{"id": k, "name": v["name"], "category": v["category"]} for k, v in engine.SKILLS.items()],
            "careers": [{"id": c["id"], "title": c["title"]} for c in engine.CAREERS],
            "interests": sorted({t for c in engine.CAREERS for t in c["tags"]})}


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    have, unknown = engine.resolve_profile(req.skills)
    if not have:
        raise HTTPException(422, "None of the skills were recognised. Pick skills from the suggestion list.")
    matches = engine.analyze(have, req.interests, req.target_career)
    db.save("analyze", sorted(have), matches[0]["title"], matches[0]["score"])
    return {"matches": matches, "unrecognized": unknown, "cgpa": req.cgpa, "note": engine.DATA_NOTE}


@app.post("/api/jd-gap")
def jd_gap(req: JDRequest):
    """Extract skills from a pasted job description and compare them with the student's skills."""
    found = extract_requirements(req.text)
    if not found:
        raise HTTPException(422, "No known skills were found in this job description.")
    required = {s: (3.0 if kind == "required" else 1.0) for s, kind in found.items()}
    have, _ = engine.resolve_profile(req.skills)
    gap = engine.gap_report(required, have)
    for row in gap["skills"]:
        row["kind"] = found[row["skill"]]
    return gap


@app.get("/api/market")
def market():
    return engine.market_summary()


@app.get("/api/history")
def history():
    return db.recent()
