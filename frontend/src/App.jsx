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
  const [comparison, setComparison] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [statusText, setStatusText] = useState('');
  const [isDone, setIsDone] = useState(false);
  const [flashKey, setFlashKey] = useState(0);
  const [activeMemoryMode, setActiveMemoryMode] = useState('without');

  async function handlePrepare() {
    setIsLoading(true);
    setIsDone(false);
    setStatusText('Analyzing CRM data...');

    try {
      const rawData = await prepareCall(deal.deal_id, "without_memory");
      
      let dataText = JSON.stringify(rawData);
      dataText = dataText.replace(/decisionâmaking/g, "decision-making")
                         .replace(/youâre/g, "you're")
                         .replace(/DealMindâs/g, "DealMind's")
                         .replace(/phaseâimplementation/g, "phase-implementation")
                         .replace(/costâbenefit/g, "cost-benefit")
                         .replace(/â€™/g, "'")
                         .replace(/â€“/g, "-")
                         .replace(/â€”/g, "-");
      const data = JSON.parse(dataText);

      setStatusText('Analysis complete');
      setComparison(data);
      setActiveMemoryMode('without');
      setFlashKey((k) => k + 1);
      setIsDone(true);
    } catch (error) {
      setStatusText('Unable to prepare call. Check that the backend is running.');
    } finally {
      setIsLoading(false);
    }
  }

  async function handleWithHindsight() {
    setIsLoading(true);
    setIsDone(false);
    setStatusText('Recalling Hindsight memories...');

    try {
      const rawData = await prepareCall(deal.deal_id, "with_hindsight");
      
      let dataText = JSON.stringify(rawData);
      dataText = dataText.replace(/decisionâmaking/g, "decision-making")
                         .replace(/youâre/g, "you're")
                         .replace(/DealMindâs/g, "DealMind's")
                         .replace(/phaseâimplementation/g, "phase-implementation")
                         .replace(/costâbenefit/g, "cost-benefit")
                         .replace(/â€™/g, "'")
                         .replace(/â€“/g, "-")
                         .replace(/â€”/g, "-");
      const data = JSON.parse(dataText);

      setStatusText('Hindsight intelligence loaded');
      setComparison(prev => ({ ...prev, with_hindsight: data.with_hindsight }));
      setActiveMemoryMode('with');
      setFlashKey((k) => k + 1);
      setIsDone(true);
    } catch (error) {
      setStatusText('Unable to retrieve Hindsight data.');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="app">
      <div className="topbar">
        <div className="wordmark">Deal<span>Mind</span></div>
        <div className="env-tag">Synthetic data · Live Hindsight memory</div>
      </div>

      <div className="card">
        <DealOverview deal={deal} comparison={comparison} activeMode={activeMemoryMode} />
        <WhatChanged deal={deal} comparison={comparison} activeMode={activeMemoryMode} flashKey={flashKey} />
        <MemoryComparison 
          comparison={comparison} 
          activeMode={activeMemoryMode}
          onModeSelect={(mode) => {
            if (mode === 'with' && (!comparison || !comparison.with_hindsight)) {
               handleWithHindsight();
            } else {
               setActiveMemoryMode(mode);
            }
          }}
          isLoading={isLoading}
        />
        <MemoryTimeline deal={deal} comparison={comparison} activeMode={activeMemoryMode} flashKey={flashKey} />
        <NextCallPrep
          deal={deal}
          comparison={comparison}
          activeMode={activeMemoryMode}
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
