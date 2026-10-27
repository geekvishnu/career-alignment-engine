import { useState } from "react";
import { checkJobDescription } from "../api";
import { GapRadar, Roadmap, SkillTable } from "./Results.jsx";

export default function JDAnalyzer({ profile }) {
  const [text, setText] = useState("");
  const [gap, setGap] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function run() {
    setBusy(true); setError(""); setGap(null);
    try { setGap(await checkJobDescription({ text, skills: profile?.skills ?? [] })); }
    catch (e) { setError(e.message); }
    setBusy(false);
  }

  return (
    <section className="panel">
      <h2>Check a job description</h2>
      <p className="muted">{profile ? "Paste any posting. We extract its skills and compare them with your profile." : "Analyze your profile first so we can compare it. Without one, every skill shows as missing."}</p>
      <textarea rows={9} value={text} onChange={(e) => setText(e.target.value)} placeholder="Paste the job description here..." />
      <button className="primary" disabled={text.trim().length < 20 || busy} onClick={run}>{busy ? "Reading..." : "Extract skills and compare"}</button>
      {error && <p className="error" role="alert">{error}</p>}
      {gap && (<>
        <p className="facts">You cover <b>{gap.have} of {gap.total}</b> skills found in this posting ({gap.coverage}% weighted).</p>
        <GapRadar data={gap.radar} />
        <h3>What to learn next</h3><Roadmap items={gap.roadmap} />
        <h3>Skills found</h3><SkillTable rows={gap.skills} />
      </>)}
    </section>
  );
}
