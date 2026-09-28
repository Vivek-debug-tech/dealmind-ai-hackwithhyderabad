export default function NextCallPrep({
  recommendation,
  onPrepare,
  isLoading,
  statusText,
  isDone,
  flashKey,
}) {
  return (
    <div className="section flash" key={flashKey}>
      <div className="prep-head">
        <div className="section-title"><span className="icon">→</span> Next call preparation</div>
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

      <div className="prep-grid">
        <div className="prep-row">
          <div className="label">Key concern</div>
          <div className="value">{recommendation.key_concern}</div>
        </div>

        <div className="prep-row">
          <div className="label">Suggested question</div>
          <div className="question-box">"{recommendation.suggested_question}"</div>
        </div>

        <div className="prep-row">
          <div className="label">Recommended action</div>
          <div className="value">{recommendation.action}</div>
        </div>
      </div>

    </div>
  );
}
