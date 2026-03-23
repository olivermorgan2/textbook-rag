import { useState, useEffect } from "react";

export default function ChapterBrowser({ onSelectChapter }) {
  const [chapters, setChapters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/api/chapters")
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load chapters (${res.status})`);
        return res.json();
      })
      .then((data) => setChapters(data.chapters))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading chapters...</p>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="chapter-list">
      <h2>Chapters</h2>
      <ul>
        {chapters.map((ch) => (
          <li key={ch.chapter_number}>
            <button onClick={() => onSelectChapter(ch.chapter_number)}>
              <span className="chapter-num">Ch. {ch.chapter_number}</span>
              <span className="chapter-title">{ch.chapter_title}</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
