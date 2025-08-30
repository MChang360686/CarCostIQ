"use client";
import Link from "next/link";

import { useState } from "react";

type Reco = {
  id: number;
  label: string;
  score: number;
  price: number;
  insuranceEstimate: number;
};

export default function Page() {
  const [text, setText] = useState("");
  const [results, setResults] = useState<Reco[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function submit() {
    setLoading(true);
    setError(null);
    setResults(null);
    try {
      const r = await fetch("http://localhost:8000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: text, userId: "demo-user-1" })
      });
      if (!r.ok) throw new Error(`Server returned ${r.status}`);
      const json = await r.json();
      setResults(json.recommendations);
    } catch (e: any) {
      setError(e.message ?? "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-bold mb-4">Car & Insurance Recommender</h1>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="w-full border rounded p-3"
        rows={6}
        placeholder="Describe your situation: budget, family, snow, commute, preferences..."
      />

      <div className="mt-3 flex gap-3">
        <button
          onClick={submit}
          disabled={!text.trim() || loading}
          className="px-4 py-2 rounded bg-black text-white disabled:opacity-50"
        >
          {loading ? "Thinking…" : "Get recommendations"}
        </button>
        <button
          onClick={() => setText("")}
          className="px-4 py-2 rounded border"
        >
          Clear
        </button>
        <Link href="/help">
          <button className="px-4 py-2 rounded border">
            Help
          </button>
        </Link>
        <Link href="/listings">
          <button className="px-4 py-2 rounded border">
            Post a Listing
          </button>
        </Link>
      </div>

      {error && <div className="mt-4 text-red-600">Error: {error}</div>}

      {results && (
        <section className="mt-6">
          <h2 className="text-xl mb-2">Top picks</h2>
          <ul className="space-y-3">
            {results.map(r => (
              <li key={r.id} className="p-3 border rounded">
                <div className="font-medium">{r.label}</div>
                <div className="text-sm opacity-80">
                  Score: {r.score.toFixed(2)} · Est. price: ${r.price.toLocaleString()} · Est. insurance: ${r.insuranceEstimate}/mo
                </div>
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}
