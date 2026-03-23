import { useState, useEffect } from "react";

export default function ChapterDetail({ chapterNumber, onBack }) {
  const [chapter, setChapter] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    setChapter(null);

    fetch(`/api/chapters/${chapterNumber}`)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load chapter (${res.status})`);
        return res.json();
      })
      .then((data) => setChapter(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [chapterNumber]);

  if (loading) return <p>Loading chapter...</p>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="chapter-detail">
      <button className="back-btn" onClick={onBack}>
        Back to chapters
      </button>
      <h2>
        Chapter {chapter.chapter_number}: {chapter.chapter_title}
      </h2>
      <pre className="chapter-content">{chapter.text}</pre>
    </div>
  );
}
