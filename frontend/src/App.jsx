import { useState } from "react";
import CitationsList from "./components/CitationsList";

export default function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState(null);
  const [citations, setCitations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    const trimmed = query.trim();
    if (!trimmed) return;

    setLoading(true);
    setError(null);
    setAnswer(null);
    setCitations([]);

    try {
      const res = await fetch("/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: trimmed, top_k: 5 }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.detail || `Request failed (${res.status})`);
      }

      const data = await res.json();
      setAnswer(data.answer);
      setCitations(data.citations);
    } catch (err) {
      setError(err.message || "Something went wrong. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <h1>Textbook RAG</h1>
      <form onSubmit={handleSubmit} className="query-form">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask a question about the textbook..."
          rows={3}
          disabled={loading}
        />
        <button type="submit" disabled={loading || !query.trim()}>
          {loading ? "Searching..." : "Ask"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {answer && (
        <div className="answer-panel">
          <h2>Answer</h2>
          <p>{answer}</p>
        </div>
      )}

      {citations.length > 0 && <CitationsList citations={citations} />}
    </div>
  );
}
