// One place for all backend calls. Set VITE_API_URL in Vercel to your deployed backend URL.
const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, body) {
  let res;
  try {
    res = await fetch(`${BASE}${path}`, {
      method: body ? "POST" : "GET",
      headers: body ? { "Content-Type": "application/json" } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch {
    throw new Error("Cannot reach the server. Check that the backend is running and VITE_API_URL is correct.");
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(typeof data.detail === "string" ? data.detail : "Please check your input and try again.");
  return data;
}

export const getMeta = () => request("/api/meta");
export const analyze = (payload) => request("/api/analyze", payload);
export const checkJobDescription = (payload) => request("/api/jd-gap", payload);
export const getMarket = () => request("/api/market");
