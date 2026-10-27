"""Skill extraction from job-description text: spaCy tokenizer + PhraseMatcher over the skill dictionary."""
import spacy
from spacy.matcher import PhraseMatcher

from .engine import ALIASES

_nlp = spacy.blank("en")                 # tokenizer + sentencizer only: no model download, small deploy size
_nlp.add_pipe("sentencizer")
_matcher = PhraseMatcher(_nlp.vocab, attr="LOWER")
for _sid in {sid for sid in ALIASES.values()}:
    _matcher.add(_sid, [_nlp.make_doc(a) for a, s in ALIASES.items() if s == _sid])

# A sentence containing one of these cues mentions a skill as optional, not required.
_OPTIONAL = ("nice to have", "preferred", "bonus", "plus", "good to have", "desirable", "familiarity", "exposure to", "an advantage")


def extract_requirements(text: str) -> dict[str, str]:
    """Return {skill_id: 'required' | 'preferred'}. A skill seen in any non-optional sentence is required."""
    found: dict[str, str] = {}
    for sent in _nlp(text).sents:
        lowered = sent.text.lower()
        level = "preferred" if any(cue in lowered for cue in _OPTIONAL) else "required"
        for match_id, _, _ in _matcher(sent):
            sid = _nlp.vocab.strings[match_id]
            if found.get(sid) != "required":
                found[sid] = level
    return found
