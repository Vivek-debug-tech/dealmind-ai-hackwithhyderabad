export default function DealOverview({ deal }) {
  const riskClass =
    deal.risk.level === 'high' ? 'risk-high' :
    deal.risk.level === 'medium' ? 'risk-medium' : 'risk-low';

  const riskLabel =
    deal.risk.level === 'high' ? 'High' :
    deal.risk.level === 'medium' ? 'Medium' : 'Low';

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
    </div>
  );
}
