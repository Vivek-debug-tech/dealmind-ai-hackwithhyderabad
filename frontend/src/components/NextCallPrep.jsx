export default function NextCallPrep({
  deal,
  comparison,
  activeMode,
  onPrepare,
  isLoading,
  statusText,
  isDone,
  flashKey,
}) {
  let rec = deal.recommendation;
  let similarDeal = null;
  const isWithMode = activeMode === 'with';

  if (comparison) {
    const activeData = isWithMode ? comparison.with_hindsight : comparison.without_memory;
    if (activeData) {
      rec = {
        key_concern: activeData.key_concerns?.[0] || 'None',
        suggested_question: activeData.recommended_questions?.[0] || 'None',
        action: activeData.recommended_actions?.[0] || 'None',
      };
      if (isWithMode && activeData.similar_deals && activeData.similar_deals.count > 0 && activeData.similar_deals.deals?.length > 0) {
        similarDeal = activeData.similar_deals;
      }
    }
  }

  return (
    <div className="section flash" key={flashKey}>
      <div className="prep-head" style={{ marginBottom: '14px' }}>
        <div>
          <div className="section-title" style={{ marginBottom: '2px' }}>
            <span className="icon">→</span> REP BRIEF
            {comparison && isWithMode && (
              <span style={{ fontSize: '9px', backgroundColor: '#F0F9F6', color: 'var(--teal)', padding: '3px 8px', borderRadius: '12px', marginLeft: '10px', fontWeight: '700', border: '1px solid #D3EAE3' }}>
                ✦ Hindsight Intelligence
              </span>
            )}
          </div>
          <div style={{ fontSize: '10px', color: 'var(--ink-soft)' }}>What the rep needs to know before the next call</div>
        </div>
        <div className="prep-action">
          <div className="cta-row">
            <button className="prepare-btn" onClick={onPrepare} disabled={isLoading}>
              {isLoading && <span className="spinner show"></span>}
              <span>{isLoading ? 'Analyzing…' : 'Prepare for call'}</span>
            </button>
            <div className={`status-line ${isDone ? 'done' : ''}`}>{statusText}</div>
          </div>
        </div>
      </div>

      <div className="prep-grid" style={{ gridTemplateColumns: '1fr', marginBottom: '10px' }}>
        <div className="prep-row">
          <div className="label">KEY SITUATION</div>
          <div className="value" style={{ fontSize: '11px', fontWeight: '500' }}>{rec.key_concern}</div>
        </div>
      </div>

      <div className="prep-grid-2cols" style={{ marginBottom: '10px' }}>
        <div className="prep-row" style={{ background: 'var(--teal-soft)', borderColor: 'var(--line-strong)' }}>
          <div className="label">RECOMMENDED ACTION</div>
          <div className="value" style={{ fontSize: '12px', fontWeight: '700' }}>{rec.action}</div>
        </div>

        <div className="prep-row" style={{ background: '#F8F9FF', borderColor: '#E3E6F6' }}>
          <div className="label" style={{ color: '#4B5C94' }}>ASK THIS</div>
          <div className="question-box" style={{ fontSize: '12px', fontWeight: '700', color: '#2C3A66' }}>"{rec.suggested_question}"</div>
        </div>
      </div>

      {similarDeal && (
        <div className="prep-grid" style={{ gridTemplateColumns: '1fr' }}>
          <div className="prep-row" style={{ background: '#FFFFFF', borderColor: '#E5EFEB', padding: '10px 14px' }}>
            <div className="label" style={{ color: 'var(--teal)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
              <span>WHY THIS RECOMMENDATION?</span>
              <span style={{ fontSize: '9px', color: 'var(--ink-soft)', background: '#F4F9F7', padding: '2px 6px', borderRadius: '4px', border: '1px solid var(--line)' }}>✦ Retrieved from Hindsight</span>
            </div>
            
            {similarDeal.evidence && (
              <div style={{ fontSize: '11px', color: 'var(--ink)', marginBottom: '10px', paddingBottom: '10px', borderBottom: '1px dashed #E0ECE8' }}>
                {similarDeal.evidence}
              </div>
            )}
            
            {similarDeal.deals.map((d, idx) => {
              const isWon = d.outcome === "WON";
              return (
                <div key={idx} style={{ marginTop: idx === 0 ? '0' : '10px', paddingTop: idx === 0 ? '0' : '10px', borderTop: idx === 0 ? 'none' : '1px dashed #E0ECE8', display: 'flex', flexDirection: 'column', gap: '2px' }}>
                  <div style={{ color: isWon ? 'var(--teal)' : '#B83D4B', fontWeight: '800', fontSize: isWon ? '11px' : '9px', opacity: isWon ? 1 : 0.85 }}>
                    {isWon ? `✓ ${d.deal_id} · ${d.outcome}` : `◇ ${d.deal_id} · ${d.outcome}`}
                  </div>
                  <div style={{ fontSize: '10px', color: 'var(--ink-soft)', marginTop: '2px' }}>
                    {isWon ? 'Tactic: ' : 'Counterexample: '}
                    <span style={{ fontWeight: '650', color: 'var(--ink)' }}>{d.tactic}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

    </div>
  );
}
