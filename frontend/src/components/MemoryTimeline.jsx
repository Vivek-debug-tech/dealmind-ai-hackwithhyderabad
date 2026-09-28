export default function MemoryTimeline({ items, flashKey }) {
  return (
    <div className="section flash" key={flashKey}>
      <div className="section-title"><span className="icon">◆</span> Hindsight memory timeline</div>
      <div className="timeline">
        {items.map((item, i) => (
          <div className={`t-item ${item.flag ? 'flag' : ''}`} key={i}>
            <div className="t-dot"></div>
            <div className="t-call">{item.call}</div>
            <div className="t-desc">
              {item.summary}{' '}
              {item.flag && <span className="t-warn">contradiction</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
