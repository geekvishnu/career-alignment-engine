import pytest

from app import engine
from app.schemas import SkillIn


def profile(*pairs):
    return engine.resolve_profile([SkillIn(name=n, level=l) for n, l in pairs])


def test_aliases_resolve():
    assert engine.resolve("Sklearn") == "scikit-learn" and engine.resolve("PowerBI") == "power bi"
    assert engine.resolve("underwater basket weaving") is None


def test_data_profile_ranks_data_roles_first():
    have, _ = profile(("SQL", "advanced"), ("Excel", "advanced"), ("Power BI", "intermediate"),
                      ("Tableau", "intermediate"), ("Statistics", "intermediate"), ("Data Visualization", "advanced"))
    top = [m["id"] for m in engine.analyze(have, [])[:2]]
    assert set(top) <= {"data-analyst", "bi-developer"}


def test_web_profile_ranks_frontend_first():
    have, _ = profile(("HTML", "advanced"), ("CSS", "advanced"), ("JavaScript", "advanced"), ("React", "advanced"), ("Git", "intermediate"))
    assert engine.analyze(have, ["frontend"])[0]["id"] == "frontend"


def test_gap_report_math_and_priority():
    required = {"python": 3, "sql": 3, "excel": 2, "power bi": 2}
    have, _ = profile(("Python", "advanced"), ("SQL", "advanced"), ("Excel", "advanced"))
    g = engine.gap_report(required, have)
    assert g["coverage"] == 80 and g["have"] == 3 and g["roadmap"][0]["skill"] == "power bi"


def test_beginner_counts_as_partial():
    g = engine.gap_report({"python": 3}, profile(("Python", "beginner"))[0])
    assert g["skills"][0]["status"] == "partial" and g["coverage"] == 40


def test_more_skills_never_lower_coverage():
    a = engine.gap_report(engine.CAREERS[0]["skills"], profile(("Python", "advanced"))[0])["coverage"]
    b = engine.gap_report(engine.CAREERS[0]["skills"], profile(("Python", "advanced"), ("SQL", "advanced"))[0])["coverage"]
    assert b > a


def test_extraction_marks_optional_skills():
    pytest.importorskip("spacy")
    from app.nlp import extract_requirements
    r = extract_requirements("You must know SQL and Python. Knowledge of Tableau is a plus. We use React.js and C++.")
    assert r["sql"] == r["python"] == "required" and r["tableau"] == "preferred" and r["react"] == "required" and r["c++"] == "required"


def test_market_summary_shape():
    m = engine.market_summary()
    assert len(m["top_skills"]) == 10 and m["salaries"][0]["max"] >= m["salaries"][-1]["max"]
