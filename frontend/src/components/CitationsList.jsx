export default function CitationsList({ citations }) {
  return (
    <div className="citations-panel">
      <h2>Citations</h2>
      <ul>
        {citations.map((c) => (
          <li key={c.chunk_id}>
            <strong>{c.chapter_title}</strong>
            {c.section_title && <span> &mdash; {c.section_title}</span>}
            <span className="source-path">{c.source_path}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
