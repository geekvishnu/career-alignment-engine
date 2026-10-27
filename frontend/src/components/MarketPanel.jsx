import { useEffect, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getMarket } from "../api";

export default function MarketPanel() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => { getMarket().then(setData).catch((e) => setError(e.message)); }, []);
  if (error) return <p className="error">{error}</p>;
  if (!data) return <p className="muted">Loading...</p>;

  // floating bar: an invisible "min" segment, then a visible "max - min" segment
  const salaries = data.salaries.map((s) => ({ title: s.title, min: s.min, range: +(s.max - s.min).toFixed(1), max: s.max }));
  return (
    <div className="results">
      <section className="panel">
        <h2>Skills that open the most roles</h2>
        <div className="chart"><ResponsiveContainer width="100%" height={300}>
          <BarChart data={data.top_skills} layout="vertical" margin={{ left: 30 }}>
            <CartesianGrid horizontal={false} /><XAxis type="number" allowDecimals={false} /><YAxis type="category" dataKey="name" width={140} />
            <Tooltip /><Bar dataKey="careers" name="Roles requiring it" fill="#0E6B6B" />
          </BarChart></ResponsiveContainer></div>
      </section>
      <section className="panel">
        <h2>Entry-level salary range (LPA)</h2>
        <div className="chart"><ResponsiveContainer width="100%" height={320}>
          <BarChart data={salaries} layout="vertical" margin={{ left: 30 }}>
            <CartesianGrid horizontal={false} /><XAxis type="number" /><YAxis type="category" dataKey="title" width={170} />
            <Tooltip formatter={(v, n, p) => (n === "Range" ? `${p.payload.min} to ${p.payload.max} LPA` : v)} />
            <Bar dataKey="min" stackId="s" fill="transparent" legendType="none" name="Min" />
            <Bar dataKey="range" stackId="s" fill="#E7A33E" name="Range" />
          </BarChart></ResponsiveContainer></div>
        <p className="muted small">{data.note}</p>
      </section>
    </div>
  );
}
