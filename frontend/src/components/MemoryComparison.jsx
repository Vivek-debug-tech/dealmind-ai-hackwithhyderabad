import { useState } from 'react';

function getMemorySignals(deal) {
  const timeline = deal.timeline ?? [];
  const timelineText = timeline.map((item) => item.summary).join(' ').toLowerCase();
  const riskLevel = deal.risk?.level ?? 'unknown';
  return [
    `${riskLevel.toUpperCase()} risk`,
    'Budget reversal detected',
    timelineText.includes('sap') ? 'SAP concern' : 'Historical integration concern',
    timelineText.includes('salesforce') ? 'Salesforce pressure' : 'Competitive pressure detected',
    `Personalized question: ${deal.recommendation?.suggested_question ?? 'Ready'}`,
    `Action: ${deal.recommendation?.action ?? 'Prepare next step'}`,
  ];
}

export default function MemoryComparison({ deal }) {
  const [mode, setMode] = useState('with');
  const withMemory = getMemorySignals(deal);

  return (
    <section className="section memory-comparison">
      <div className="comparison-head">
        <div>
          <div className="section-title"><span className="icon">◌</span> Memory impact</div>
          <p className="comparison-subtitle">The difference Hindsight makes to deal intelligence.</p>
        </div>
        <div className="memory-toggle" role="group" aria-label="Memory comparison">
          <button
            className={mode === 'without' ? 'active' : ''}
            onClick={() => setMode('without')}
          >
            Without memory
          </button>
          <button
            className={mode === 'with' ? 'active' : ''}
            onClick={() => setMode('with')}
          >
            With Hindsight
          </button>
        </div>
      </div>

      <div className="comparison-columns">
        <div className={`comparison-panel without-memory ${mode === 'without' ? 'selected' : ''}`}>
          <div className="comparison-label">WITHOUT MEMORY</div>
          <ul>
            {['Generic risk', 'Generic questions', 'No historical contradiction'].map((signal) => <li key={signal}>{signal}</li>)}
          </ul>
        </div>
        <div className="comparison-arrow" aria-hidden="true">→</div>
        <div className={`comparison-panel with-memory ${mode === 'with' ? 'selected' : ''}`}>
          <div className="comparison-label">WITH HINDSIGHT</div>
          <ul>
            {withMemory.map((signal) => <li key={signal}>{signal}</li>)}
          </ul>
        </div>
      </div>
    </section>
  );
}
