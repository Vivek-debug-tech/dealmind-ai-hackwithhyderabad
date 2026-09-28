export default function WhatChanged({ deal, comparison, activeMode, flashKey }) {
  if (!comparison) {
    const contradiction = deal.contradiction;
    return (
      <div className="section flash" key={flashKey}>
        <div className="section-title">
          <span className="icon">⚠</span> What changed
          <span className="change-range">{contradiction.detected_in} vs {contradiction.conflicts_with}</span>
        </div>
        <div className="change-box">
          <div className="change-line">
            <span className="was">"{contradiction.previous}"</span>
            <span className="arrow">→</span>
            <span className="now">"{contradiction.current}"</span>
          </div>
          <div className="change-meta">
            Detected in {contradiction.detected_in} · Contradicts statement from {contradiction.conflicts_with}
          </div>
        </div>
      </div>
    );
  }

  if (activeMode === 'without') return null;

  const changes = comparison.with_hindsight.changes_detected || [];
  const contradictions = comparison.with_hindsight.contradictions || [];

  if (changes.length === 0 && contradictions.length === 0) return null;

  const allChanges = [
    ...contradictions.map(c => ({ type: 'contradiction', ...c })),
    ...changes.map(c => ({ type: 'change', ...c }))
  ];

  const uniqueChanges = [];
  const seenTopics = new Set();
  for (const c of allChanges) {
    if (!seenTopics.has(c.topic.toLowerCase())) {
      seenTopics.add(c.topic.toLowerCase());
      uniqueChanges.push(c);
    }
  }

  const topChanges = uniqueChanges.slice(0, 2);

  return (
    <div className="section flash" key={flashKey}>
      <div className="section-title">
        <span className="icon">⚠</span> What changed
      </div>
      {topChanges.map((c, i) => (
        <div className="change-box" key={i} style={{ marginBottom: '8px', borderColor: c.type === 'contradiction' ? '#F7DFE1' : 'transparent', background: c.type === 'contradiction' ? '#FFF5F5' : '#F4F9F7' }}>
          <div style={{ fontSize: '11px', fontWeight: '700', marginBottom: '6px', color: c.type === 'contradiction' ? '#B83D4B' : 'var(--ink)' }}>
            {c.topic} {c.type === 'contradiction' ? '→ Historical contradiction detected ⚠' : '→ Position changed'}
          </div>
          <div className="change-line">
            <span className="was">Earlier: "{c.earlier_statement || c.previous_position}"</span>
            <span className="arrow">→</span>
            <span className="now">Now: "{c.later_statement || c.current_position}"</span>
          </div>
          <div className="change-meta" style={{ marginTop: '6px', color: 'var(--ink-soft)' }}>
            {c.why_it_matters || c.significance}
          </div>
        </div>
      ))}
    </div>
  );
}
