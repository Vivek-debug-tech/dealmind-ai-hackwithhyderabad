import { useState } from 'react';
import { mockPrepareResponse } from './data/mockPrepareResponse.js';
import { prepareCall } from './api/prepareCall.js';

import DealOverview from './components/DealOverview.jsx';
import WhatChanged from './components/WhatChanged.jsx';
import MemoryTimeline from './components/MemoryTimeline.jsx';
import NextCallPrep from './components/NextCallPrep.jsx';
import MemoryComparison from './components/MemoryComparison.jsx';

export default function App() {
  const [deal, setDeal] = useState(mockPrepareResponse);
  const [isLoading, setIsLoading] = useState(false);
  const [statusText, setStatusText] = useState('');
  const [isDone, setIsDone] = useState(false);
  const [flashKey, setFlashKey] = useState(0);

  async function handlePrepare() {
    setIsLoading(true);
    setIsDone(false);
    setStatusText('↻ Recalling deal memory from Hindsight...');

    try {
      const data = await prepareCall(deal.deal_id);
      setStatusText('✓ 3 historical interactions recalled');
      setDeal(data);
      setFlashKey((k) => k + 1);
      setIsDone(true);
    } catch (error) {
      setStatusText('Unable to recall deal memory. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app">
      <div className="topbar">
        <div className="wordmark">Deal<span>Mind</span></div>
        <div className="env-tag">mock data</div>
      </div>

      <div className="card">
        <DealOverview deal={deal} />
        <WhatChanged contradiction={deal.contradiction} flashKey={flashKey} />
        <MemoryComparison deal={deal} />
        <MemoryTimeline items={deal.timeline} flashKey={flashKey} />
        <NextCallPrep
          recommendation={deal.recommendation}
          onPrepare={handlePrepare}
          isLoading={isLoading}
          statusText={statusText}
          isDone={isDone}
          flashKey={flashKey}
        />
      </div>
    </div>
  );
}
