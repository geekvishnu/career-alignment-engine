import { useState } from "react";
import { PolarAngleAxis, PolarGrid, Radar, RadarChart, ResponsiveContainer, Tooltip } from "recharts";

const LABEL = { have: "Have", partial: "Partial", missing: "Missing" };

export function SkillTable({ rows }) {
  return (
    <table>
      <thead><tr><th>Skill</th><th>Importance</th><th>Your level</th></tr></thead>
      <tbody>{rows.map((r) => (
        <tr key={r.skill}>
          <td>{r.name}{r.kind === "preferred" && <span className="muted"> (preferred)</span>}</td>
          <td>{r.weight >= 3 ? "Core" : r.weight === 2 ? "Important" : "Nice to have"}</td>
          <td><span className={`tag ${r.status}`}>{LABEL[r.status]}</span></td>
        </tr>
      ))}</tbody>
    </table>
  );
}

export function GapRadar({ data }) {
  return (
    <div className="chart" aria-label="Skill coverage by category">
      <ResponsiveContainer width="100%" height={260}>
        <RadarChart data={data}>
          <PolarGrid /><PolarAngleAxis dataKey="category" tick={{ fontSize: 12 }} />
          <Radar name="Required" dataKey="required" stroke="#9AA9A6" fill="#9AA9A6" fillOpacity={0.15} />
          <Radar name="You" dataKey="you" stroke="#0E6B6B" fill="#0E6B6B" fillOpacity={0.45} />
          <Tooltip />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function Roadmap({ items }) {
  if (!items.length) return <p className="muted">No gaps. You meet the requirements for this role.</p>;
  return <ol className="roadmap">{items.map((i) => <li key={i.skill}><b>{i.name}</b><span>{i.reason}</span></li>)}</ol>;
}

export default function Results({ data }) {
  const [picked, setPicked] = useState(null);
  const current = data.matches.find((m) => m.id === picked) ?? data.matches[0];
  const [lo, hi] = current.salary_lpa;

  return (
    <div className="results">
      {data.unrecognized.length > 0 && <p className="warn">Not recognised and left out: {data.unrecognized.join(", ")}. Pick skills from the suggestions.</p>}
      <ul className="ranking">
        {data.matches.map((m) => (
          <li key={m.id}>
            <button className={m.id === current.id ? "rank on" : "rank"} onClick={() => setPicked(m.id)} aria-pressed={m.id === current.id}>
              <span className="score">{m.score}<small>%</small></span>
              <span className="rtitle">{m.title}</span>
              <span className="bar"><i style={{ width: `${m.score}%` }} /></span>
            </button>
          </li>
        ))}
      </ul>

      <section className="panel detail">
        <h2>{current.title}</h2>
        <p className="muted">{current.description}</p>
        <p className="facts">
          You cover <b>{current.gap.have} of {current.gap.total}</b> required skills ({current.coverage}% weighted).
          Profile similarity {current.similarity}%. {current.interest_match && "Matches your interests. "}
          Typical entry-level pay: {lo}-{hi} LPA.
        </p>
        <GapRadar data={current.gap.radar} />
        <h3>What to learn next</h3>
        <Roadmap items={current.gap.roadmap} />
        <h3>Skill breakdown</h3>
        <SkillTable rows={current.gap.skills} />
      </section>
      <p className="muted small">A match score shows how well your skills align with a role. It is not a chance of getting hired. {data.note}</p>
    </div>
  );
}
