import { useEffect, useState } from "react";
import { analyze, getMeta } from "./api";
import ProfileForm from "./components/ProfileForm.jsx";
import Results from "./components/Results.jsx";
import JDAnalyzer from "./components/JDAnalyzer.jsx";
import MarketPanel from "./components/MarketPanel.jsx";

const TABS = [["match", "Career match"], ["jd", "Check a job description"], ["market", "Market view"]];

export default function App() {
  const [meta, setMeta] = useState(null);
  const [profile, setProfile] = useState(null);   // last submitted payload, reused by the JD tab
  const [result, setResult] = useState(null);
  const [tab, setTab] = useState("match");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => { getMeta().then(setMeta).catch((e) => setError(e.message)); }, []);

  async function run(payload) {
    setLoading(true); setError("");
    try {
      setResult(await analyze(payload));
      setProfile(payload);
      setTab("match");
    } catch (e) { setError(e.message); }
    setLoading(false);
  }

  return (
    <div className="shell">
      <header>
        <h1>Career Alignment Engine</h1>
        <p>Enter what you know. See which roles fit, what is missing, and what to learn next.</p>
      </header>
      <div className="layout">
        <aside>{meta ? <ProfileForm meta={meta} onSubmit={run} loading={loading} /> : <p className="muted">{error || "Loading..."}</p>}</aside>
        <main>
          <nav role="tablist">
            {TABS.map(([id, label]) => (
              <button key={id} role="tab" aria-selected={tab === id} className={tab === id ? "tab on" : "tab"} onClick={() => setTab(id)}>{label}</button>
            ))}
          </nav>
          {error && <p className="error" role="alert">{error}</p>}
          {tab === "match" && (result ? <Results data={result} /> : <p className="empty">Add at least one skill on the left, then choose Analyze my profile.</p>)}
          {tab === "jd" && <JDAnalyzer profile={profile} />}
          {tab === "market" && <MarketPanel />}
        </main>
      </div>
    </div>
  );
}
