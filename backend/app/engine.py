"""Core analytics: skill resolution, TF-IDF + cosine career matching, skill-gap analysis, market summary."""
import json
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

DATA = Path(__file__).parent / "data"
SKILLS: dict = json.loads((DATA / "skills.json").read_text())
_raw = json.loads((DATA / "careers.json").read_text())
CAREERS: list[dict] = _raw["careers"]
DATA_NOTE: str = _raw["_note"]

LEVELS = {"beginner": 0.4, "intermediate": 0.7, "advanced": 1.0}
HAVE_THRESHOLD = 0.7                      # intermediate or better counts as "have"
W_COVERAGE, W_COSINE, W_INTEREST = 0.55, 0.35, 0.10

# alias -> canonical skill id ("sklearn" -> "scikit-learn")
ALIASES = {a.lower(): sid for sid, m in SKILLS.items() for a in [sid, m["name"], *m["aliases"]]}

# --- Career x skill matrix, converted to TF-IDF so rare skills count for more -----------------
SKILL_IDS = list(SKILLS)
_IDX = {s: i for i, s in enumerate(SKILL_IDS)}
_M = np.zeros((len(CAREERS), len(SKILL_IDS)))
for r, c in enumerate(CAREERS):
    for s, w in c["skills"].items():
        _M[r, _IDX[s]] = w
_USED = _M.sum(axis=0) > 0                # skills no career asks for must not dilute the vector
_TFIDF = TfidfTransformer().fit(_M)
_CAREER_VECS = _TFIDF.transform(_M)
# how many careers ask for each skill (used to prioritise what to learn)
FREQ = {s: int((_M[:, _IDX[s]] > 0).sum()) for s in SKILL_IDS}


def resolve(name: str) -> str | None:
    return ALIASES.get(name.strip().lower())


def resolve_profile(skills) -> tuple[dict[str, float], list[str]]:
    """[{name, level}] -> ({canonical_skill: 0..1}, [unrecognised names]). Keeps the highest level on duplicates."""
    have, unknown = {}, []
    for s in skills:
        sid = resolve(s.name)
        if sid is None:
            unknown.append(s.name)
        else:
            have[sid] = max(have.get(sid, 0), LEVELS[s.level])
    return have, unknown


def _cosine(have: dict[str, float]) -> np.ndarray:
    v = np.zeros((1, len(SKILL_IDS)))
    for s, lvl in have.items():
        if _USED[_IDX[s]]:
            v[0, _IDX[s]] = lvl
    if not v.any():
        return np.zeros(len(CAREERS))
    return cosine_similarity(_TFIDF.transform(v), _CAREER_VECS)[0]


def gap_report(required: dict[str, float], have: dict[str, float]) -> dict:
    """Compare required skills {skill: weight} with the student's {skill: level}."""
    total = sum(required.values()) or 1.0
    rows = []
    for s, w in sorted(required.items(), key=lambda kv: (-kv[1], kv[0])):
        lvl = have.get(s, 0.0)
        status = "have" if lvl >= HAVE_THRESHOLD else "partial" if lvl > 0 else "missing"
        rows.append({"skill": s, "name": SKILLS[s]["name"], "category": SKILLS[s]["category"],
                     "weight": w, "level": lvl, "status": status})
    coverage = sum(r["weight"] * min(r["level"], 1) for r in rows) / total

    cats = defaultdict(lambda: [0.0, 0.0])           # category -> [earned, possible]
    for r in rows:
        cats[r["category"]][0] += r["weight"] * r["level"]
        cats[r["category"]][1] += r["weight"]
    radar = [{"category": c, "you": round(e / p * 100), "required": 100} for c, (e, p) in cats.items()]

    todo = [r for r in rows if r["status"] != "have"]
    todo.sort(key=lambda r: (-r["weight"], r["status"] != "missing", -FREQ[r["skill"]]))
    roadmap = [{"skill": r["skill"], "name": r["name"],
                "reason": ("Core requirement" if r["weight"] >= 3 else "Important" if r["weight"] == 2 else "Nice to have")
                          + (" - strengthen your current level" if r["status"] == "partial" else " - not yet in your profile")}
               for r in todo[:6]]
    return {"coverage": round(coverage * 100), "have": sum(r["status"] == "have" for r in rows),
            "total": len(rows), "skills": rows, "radar": radar, "roadmap": roadmap}


def analyze(have: dict[str, float], interests: list[str], target: str | None = None, top_n: int = 5) -> list[dict]:
    """Rank careers. score = 55% weighted coverage + 35% TF-IDF cosine + 10% interest match."""
    cos = _cosine(have)
    out = []
    for i, c in enumerate(CAREERS):
        gap = gap_report(c["skills"], have)
        interest = 1.0 if set(interests) & set(c["tags"]) else 0.0
        if interests:
            score = W_COVERAGE * gap["coverage"] / 100 + W_COSINE * cos[i] + W_INTEREST * interest
        else:                                         # no interests given: renormalise the other two weights
            score = (W_COVERAGE * gap["coverage"] / 100 + W_COSINE * cos[i]) / (W_COVERAGE + W_COSINE)
        out.append({"id": c["id"], "title": c["title"], "description": c["description"],
                    "score": round(score * 100), "coverage": gap["coverage"], "similarity": round(float(cos[i]) * 100),
                    "interest_match": bool(interest), "salary_lpa": c["salary_lpa"], "gap": gap})
    out.sort(key=lambda m: -m["score"])
    keep = out[:top_n]
    if target and all(m["id"] != target for m in keep):
        keep += [m for m in out if m["id"] == target]
    return keep


def market_summary() -> dict:
    """Descriptive market view from the dataset (pandas). Swap the source for real postings when available."""
    rows = [{"skill": s, "career": c["id"], "weight": w} for c in CAREERS for s, w in c["skills"].items()]
    df = pd.DataFrame(rows)
    top = (df.groupby("skill").agg(careers=("career", "nunique"), weight=("weight", "sum"))
             .sort_values(["careers", "weight"], ascending=False).head(10).reset_index())
    top["name"] = top["skill"].map(lambda s: SKILLS[s]["name"])
    sal = pd.DataFrame([{"title": c["title"], "min": c["salary_lpa"][0], "max": c["salary_lpa"][1]} for c in CAREERS])
    return {"top_skills": top[["name", "careers", "weight"]].to_dict("records"),
            "salaries": sal.sort_values("max", ascending=False).to_dict("records"), "note": DATA_NOTE}
