export default function PredictionsPage() {
  const predictions = [
    { symbol: "BTC", pLong: 72, pShort: 12, pNeutral: 16, confidence: 87 },
    { symbol: "ETH", pLong: 68, pShort: 14, pNeutral: 18, confidence: 82 },
    { symbol: "SOL", pLong: 74, pShort: 10, pNeutral: 16, confidence: 85 },
    { symbol: "ADA", pLong: 22, pShort: 55, pNeutral: 23, confidence: 65 },
    { symbol: "DOGE", pLong: 45, pShort: 20, pNeutral: 35, confidence: 48 },
    { symbol: "BNB", pLong: 38, pShort: 22, pNeutral: 40, confidence: 61 },
    { symbol: "XRP", pLong: 30, pShort: 32, pNeutral: 38, confidence: 52 },
    { symbol: "AVAX", pLong: 60, pShort: 18, pNeutral: 22, confidence: 72 },
    { symbol: "LINK", pLong: 58, pShort: 16, pNeutral: 26, confidence: 68 },
    { symbol: "MATIC", pLong: 18, pShort: 52, pNeutral: 30, confidence: 62 },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold">ML Predictions</h1>
        <div className="text-xs text-[#8b949e] font-mono bg-[#12121a] border border-[#1e2d4a] px-3 py-1 rounded">
          Model: RandomForest + XGBoost + LightGBM | Accuracy: 73% | Features: 42
        </div>
      </div>

      <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
        <h2 className="text-sm font-semibold mb-3">7-Day Forecast</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-[10px] text-[#8b949e] uppercase border-b border-[#1e2d4a]">
              <th className="text-left py-2">Asset</th>
              <th className="text-center py-2">P(LONG)</th>
              <th className="text-center py-2">P(SHORT)</th>
              <th className="text-center py-2">P(NEUTRAL)</th>
              <th className="text-center py-2">Confidence</th>
              <th className="text-center py-2">Visual</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map((p) => (
              <tr key={p.symbol} className="border-b border-[#1e2d4a]/30 hover:bg-[#1a1a2e]">
                <td className="py-3 font-mono font-bold">{p.symbol}</td>
                <td className="py-3 text-center"><span className="text-[#22c55e] font-mono">{p.pLong}%</span></td>
                <td className="py-3 text-center"><span className="text-[#ef4444] font-mono">{p.pShort}%</span></td>
                <td className="py-3 text-center"><span className="text-[#8b949e] font-mono">{p.pNeutral}%</span></td>
                <td className="py-3 text-center"><span className="font-mono">{p.confidence}%</span></td>
                <td className="py-3 px-4">
                  <div className="flex h-4 rounded overflow-hidden">
                    <div className="bg-[#22c55e]" style={{width: `${p.pLong}%`}}></div>
                    <div className="bg-[#ef4444]" style={{width: `${p.pShort}%`}}></div>
                    <div className="bg-[#8b949e]" style={{width: `${p.pNeutral}%`}}></div>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <div className="text-[10px] text-[#8b949e] uppercase mb-1">Model Accuracy</div>
          <div className="text-2xl font-bold font-mono text-[#38bdf8]">73%</div>
          <div className="score-bar mt-2"><div className="score-bar-fill bg-[#38bdf8]" style={{width: '73%'}}></div></div>
        </div>
        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <div className="text-[10px] text-[#8b949e] uppercase mb-1">F1 Score</div>
          <div className="text-2xl font-bold font-mono text-[#a78bfa]">0.69</div>
          <div className="score-bar mt-2"><div className="score-bar-fill bg-[#a78bfa]" style={{width: '69%'}}></div></div>
        </div>
        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <div className="text-[10px] text-[#8b949e] uppercase mb-1">Training Samples</div>
          <div className="text-2xl font-bold font-mono text-[#22c55e]">50K</div>
          <div className="text-[10px] text-[#8b949e] mt-2">Last trained: Aug 20, 2026</div>
        </div>
      </div>
    </div>
  );
}
