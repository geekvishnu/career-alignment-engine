import { useMemo, useState } from "react";

const LEVELS = ["beginner", "intermediate", "advanced"];

export default function ProfileForm({ meta, onSubmit, loading }) {
  const [skills, setSkills] = useState([]);        // [{ name, level }]
  const [query, setQuery] = useState("");
  const [interests, setInterests] = useState([]);
  const [cgpa, setCgpa] = useState("");
  const [target, setTarget] = useState("");

  const suggestions = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return [];
    const taken = new Set(skills.map((s) => s.name.toLowerCase()));
    return meta.skills.filter((s) => s.name.toLowerCase().includes(q) && !taken.has(s.name.toLowerCase())).slice(0, 6);
  }, [query, skills, meta]);

  const addSkill = (name) => {
    const clean = name.trim();
    if (clean && !skills.some((s) => s.name.toLowerCase() === clean.toLowerCase())) setSkills([...skills, { name: clean, level: "intermediate" }]);
    setQuery("");
  };
  const setLevel = (name, level) => setSkills(skills.map((s) => (s.name === name ? { ...s, level } : s)));
  const toggle = (t) => setInterests(interests.includes(t) ? interests.filter((x) => x !== t) : [...interests, t]);

  function submit(e) {
    e.preventDefault();
    onSubmit({ skills, interests, cgpa: cgpa === "" ? null : Number(cgpa), target_career: target || null });
  }

  return (
    <form onSubmit={submit} className="panel">
      <label htmlFor="skill">Your skills</label>
      <input id="skill" value={query} placeholder="Type a skill, e.g. Python" autoComplete="off"
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addSkill(suggestions[0]?.name ?? query); } }} />
      {suggestions.length > 0 && (
        <ul className="suggest">{suggestions.map((s) => (
          <li key={s.id}><button type="button" onClick={() => addSkill(s.name)}>{s.name}<span>{s.category}</span></button></li>
        ))}</ul>
      )}
      <ul className="chips">
        {skills.map((s) => (
          <li key={s.name} className="chip">
            <b>{s.name}</b>
            <select aria-label={`Level for ${s.name}`} value={s.level} onChange={(e) => setLevel(s.name, e.target.value)}>
              {LEVELS.map((l) => <option key={l}>{l}</option>)}
            </select>
            <button type="button" aria-label={`Remove ${s.name}`} onClick={() => setSkills(skills.filter((x) => x.name !== s.name))}>×</button>
          </li>
        ))}
      </ul>

      <label>Interests <span className="muted">(optional)</span></label>
      <div className="pills">{meta.interests.map((t) => (
        <button type="button" key={t} aria-pressed={interests.includes(t)} className={interests.includes(t) ? "pill on" : "pill"} onClick={() => toggle(t)}>{t}</button>
      ))}</div>

      <div className="row">
        <div><label htmlFor="cgpa">CGPA <span className="muted">(context only)</span></label>
          <input id="cgpa" type="number" min="0" max="10" step="0.01" value={cgpa} onChange={(e) => setCgpa(e.target.value)} /></div>
        <div><label htmlFor="target">Target role</label>
          <select id="target" value={target} onChange={(e) => setTarget(e.target.value)}>
            <option value="">Any</option>{meta.careers.map((c) => <option key={c.id} value={c.id}>{c.title}</option>)}
          </select></div>
      </div>
      <button className="primary" disabled={!skills.length || loading}>{loading ? "Analyzing..." : "Analyze my profile"}</button>
    </form>
  );
}
