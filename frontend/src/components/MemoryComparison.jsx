import { useState } from 'react';

function getApiSignals(apiData) {
  if (!apiData || apiData.error) {
    return ['Click "Prepare for call" to generate AI insights'];
  }
  
  const signals = [];
  
  if (apiData.risk?.level) {
    signals.push(`${apiData.risk.level.toUpperCase()} RISK: ${apiData.risk.reason || ''}`);
  }
  
  if (apiData.changes_detected && apiData.changes_detected.length > 0) {
    const c = apiData.changes_detected[0];
    signals.push(`Change in ${c.topic}: ${c.previous_position} → ${c.current_position}.`);
  } else if (apiData.key_concerns) {
    signals.push('No historical change detected.');
  }

  if (apiData.contradictions && apiData.contradictions.length > 0) {
    const c = apiData.contradictions[0];
    signals.push(`Contradiction regarding ${c.topic}: Earlier "${c.earlier_statement}", but later "${c.later_statement}".`);
  } else if (apiData.key_concerns) {
    signals.push('No historical contradiction detected.');
  }
  
  if (apiData.key_concerns && apiData.key_concerns.length > 0) {
    signals.push(`Key concern: ${apiData.key_concerns[0]}`);
  }

  if (apiData.recommended_questions && apiData.recommended_questions.length > 0) {
    signals.push(`Recommended question: "${apiData.recommended_questions[0]}"`);
  }

  if (apiData.recommended_actions && apiData.recommended_actions.length > 0) {
    signals.push(`Suggested action: ${apiData.recommended_actions[0]}`);
  }
  
  return signals;
}

export default function MemoryComparison({ comparison, activeMode, onModeSelect, isLoading }) {
  if (!comparison) {
    return (
      <section className="section memory-comparison">
        <div className="comparison-head">
          <div>
            <div className="section-title"><span className="icon">◌</span> Memory impact</div>
            <p className="comparison-subtitle">The difference Hindsight makes to deal intelligence.</p>
          </div>
          <div className="memory-toggle" role="group" aria-label="Memory comparison">
            <button className="active">Without memory</button>
            <button disabled>With Hindsight</button>
          </div>
        </div>
        <div className="comparison-columns" style={{ gridTemplateColumns: '1fr', marginTop: '14px' }}>
          <div className="comparison-panel without-memory selected">
            <div className="comparison-label">WITHOUT MEMORY</div>
            <ul>
              <li>Click "Prepare for call" to generate AI insights</li>
            </ul>
          </div>
        </div>
      </section>
    );
  }

  const withoutMemory = getApiSignals(comparison.without_memory);
  const withMemory = getApiSignals(comparison.with_hindsight);

  return (
    <section className="section memory-comparison">
      <div className="comparison-head">
        <div>
          <div className="section-title"><span className="icon">◌</span> Memory impact</div>
          <p className="comparison-subtitle">The difference Hindsight makes to deal intelligence.</p>
        </div>
        <div className="memory-toggle" role="group" aria-label="Memory comparison">
          <button
            className={activeMode === 'without' ? 'active' : ''}
            onClick={() => onModeSelect('without')}
          >
            Without memory
          </button>
          <button
            className={activeMode === 'with' ? 'active' : ''}
            onClick={() => onModeSelect('with')}
            disabled={isLoading && activeMode === 'without'}
          >
            With Hindsight {isLoading && activeMode === 'without' ? '...' : ''}
          </button>
        </div>
      </div>

      <div className="comparison-columns" style={{ gridTemplateColumns: '1fr', marginTop: '14px' }}>
        {activeMode === 'without' ? (
          <div className="comparison-panel without-memory selected">
            <div className="comparison-label">WITHOUT MEMORY</div>
            <ul>
              {withoutMemory.map((signal, i) => <li key={i}>{signal}</li>)}
            </ul>
          </div>
        ) : (
          <div className="comparison-panel with-memory selected">
            <div className="comparison-label">WITH HINDSIGHT</div>
            <ul>
              {withMemory.map((signal, i) => <li key={i}>{signal}</li>)}
            </ul>
          </div>
        )}
      </div>
    </section>
  );
}
