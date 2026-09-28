import { useState } from 'react';

export default function MemoryTimeline({ deal, comparison, activeMode, flashKey }) {
  const [expanded, setExpanded] = useState(false);
  let items = deal.timeline;
  let similarCount = 0;
  let totalMemories = 0;

  if (comparison && activeMode === 'without') return null;

  if (comparison) {
    const hw = comparison.with_hindsight;
    const mems = hw.memories_used || [];
    totalMemories = mems.length;
    similarCount = hw.similar_deals?.count || 0;
    const unique = [];
    const seen = new Set();
    
    mems.forEach(m => {
      const dateMatch = m.text.match(/\d{4}-\d{2}-\d{2}/);
      const dateStr = dateMatch ? dateMatch[0] : "Unknown Date";
      
      let summary = m.text.replace(/\[Deal: DEAL-\d+\] /, '').trim();
      if (summary.startsWith("Call ")) {
        summary = summary.replace(/^Call \d+ - [A-Za-z]+ \(\d{4}-\d{2}-\d{2}\) \| [^\|]+\| /, '');
      }
      
      let shortSummary = summary.split('.')[0] + '.';
      if (shortSummary.length > 80) shortSummary = shortSummary.substring(0, 80) + '...';

      if (!seen.has(shortSummary)) {
        seen.add(shortSummary);
        unique.push({
          call: dateStr !== "Unknown Date" ? dateStr : m.source,
          summary: shortSummary,
          full_text: summary,
          flag: summary.toLowerCase().includes('budget') || summary.toLowerCase().includes('contradiction')
        });
      }
    });

    unique.sort((a, b) => a.call.localeCompare(b.call));
    items = unique;
  } else {
    totalMemories = items.length;
  }

  return (
    <div className="section flash" key={flashKey}>
      <div className="section-title"><span className="icon">◆</span> Hindsight memory timeline</div>
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '12px' }}>
        {items.slice(0, expanded ? items.length : 3).map((item, i) => (
          <div key={i} style={{ display: 'flex', gap: '8px', fontSize: '11px' }}>
            <span style={{ color: item.flag ? '#C78631' : '#708484', marginTop: '1px' }}>●</span>
            <div>
              <span style={{ fontWeight: '650', color: 'var(--ink)' }}>{item.call}</span> <span style={{ color: 'var(--ink-soft)' }}>— {item.summary}</span>
              {expanded && (
                <div style={{ marginTop: '4px', fontSize: '10px', color: 'var(--ink-soft)', padding: '6px 8px', background: '#F8F9FF', borderRadius: '4px', border: '1px solid #E3E6F6' }}>
                  {item.full_text || item.summary}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '10px', color: 'var(--ink-soft)', borderTop: '1px solid var(--line)', paddingTop: '10px' }}>
        <span>{totalMemories} memories recalled {similarCount > 0 ? `· ${similarCount} similar closed deals` : ''}</span>
        <button onClick={() => setExpanded(!expanded)} style={{ background: 'transparent', border: 'none', color: 'var(--teal)', cursor: 'pointer', textDecoration: 'none', fontWeight: '650', marginLeft: 'auto' }}>
          {expanded ? 'Hide evidence' : 'View evidence'}
        </button>
      </div>
    </div>
  );
}
