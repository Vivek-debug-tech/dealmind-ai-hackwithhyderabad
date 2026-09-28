export default function WhatChanged({ contradiction, flashKey }) {
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
