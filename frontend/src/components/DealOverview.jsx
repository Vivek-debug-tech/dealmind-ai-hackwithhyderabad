export default function DealOverview({ deal, comparison, activeMode }) {
  const riskObj = comparison ? (activeMode === 'with' ? comparison.with_hindsight?.risk : comparison.without_memory?.risk) : deal.risk;
  const levelStr = (riskObj?.level || 'low').toLowerCase();
  
  const riskClass =
    levelStr === 'high' ? 'risk-high' :
    levelStr === 'medium' ? 'risk-medium' : 'risk-low';

  const riskLabel =
    levelStr === 'high' ? 'High' :
    levelStr === 'medium' ? 'Medium' : 'Low';

  return (
    <div className="section">
      <div className="deal-head">
        <div>
          <p className="deal-name">{deal.deal_name}</p>
          <p className="deal-sub">Owner: {deal.owner} · Last call just now</p>
        </div>
        <div className="stage-pill">{deal.stage}</div>
      </div>

      <div className="metrics">
        <div className="metric">
          <div className="label">Deal value</div>
          <div className="value">{deal.value}</div>
        </div>
        <div className="metric">
          <div className="label">Segment</div>
          <div className="value">{deal.segment}</div>
        </div>
        <div className="metric">
          <div className="label">Deal risk</div>
          <div className={`risk-row ${riskClass}`}>
            <span className="risk-dot"></span>
            <span className="value">{riskLabel}</span>
          </div>
        </div>
      </div>

      <div className="metrics" style={{ marginTop: '8px', gridTemplateColumns: '1fr' }}>
        <div className="metric" style={{ padding: '6px 10px', background: 'transparent' }}>
          <div className="label">Key Stakeholders & Concerns</div>
          <div className="value" style={{ fontSize: '11px', fontWeight: 'normal', display: 'flex', gap: '14px', flexWrap: 'wrap', marginTop: '2px' }}>
            <span><strong>Michael Roberts (CFO)</strong>: Budget & Commercial</span>
            <span><strong>David Chen (CTO)</strong>: SAP Integration</span>
            <span><strong>Sarah Mitchell (VP Sales)</strong>: Pricing & ROI</span>
          </div>
        </div>
      </div>
    </div>
  );
}
