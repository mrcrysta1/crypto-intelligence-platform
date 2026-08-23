export default function SignalsPage() {
  const signals = [
    { asset: "BTC", direction: "LONG", confidence: 87, composite: 82, reasons: ["Strong technical momentum", "ETF inflows bullish", "Whale accumulation"], risk: "low", tech: 78, fund: 92, whale: 85, deriv: 71 },
    { asset: "ETH", direction: "LONG", confidence: 82, composite: 78, reasons: ["L2 growth driving demand", "Staking yield attractive", "Network activity rising"], risk: "low", tech: 72, fund: 88, whale: 80, deriv: 68 },
    { asset: "SOL", direction: "LONG", confidence: 85, composite: 81, reasons: ["Strong momentum breakout", "Meme coin activity boosting fees"], risk: "medium", tech: 88, fund: 82, whale: 75, deriv: 72 },
    { asset: "ADA", direction: "SHORT", confidence: 65, composite: 47, reasons: ["Weak technical structure", "Declining on-chain metrics"], risk: "medium", tech: 35, fund: 60, whale: 48, deriv: 42 },
    { asset: "DOGE", direction: "WATCH", confidence: 58, composite: 56, reasons: ["High volatility", "Social sentiment mixed"], risk: "high", tech: 72, fund: 35, whale: 68, deriv: 55 },
    { asset: "MATIC", direction: "SHORT", confidence: 62, composite: 45, reasons: ["Below key support", "Declining volume"], risk: "high", tech: 32, fund: 62, whale: 45, deriv: 38 },
    { asset: "AVAX", direction: "LONG", confidence: 72, composite: 64, reasons: ["Recovery momentum", "Subnet adoption growing"], risk: "medium", tech: 65, fund: 72, whale: 58, deriv: 55 },
    { asset: "LINK", direction: "LONG", confidence: 68, composite: 65, reasons: ["Oracle demand increasing", "CCIP adoption growing"], risk: "medium", tech: 58, fund: 78, whale: 65, deriv: 52 },
    { asset: "NEAR", direction: "LONG", confidence: 70, composite: 64, reasons: ["Chain abstraction narrative", "Developer activity rising"], risk: "medium", tech: 70, fund: 68, whale: 60, deriv: 55 },
    { asset: "BCH", direction: "NO_TRADE", confidence: 42, composite: 44, reasons: ["Low conviction signal", "Conflicting indicators"], risk: "medium", tech: 42, fund: 55, whale: 38, deriv: 35 },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold">Trading Signals</h1>
        <div className="flex gap-2 text-xs font-mono">
          <span className="px-2 py-1 rounded bg-[#22c55e]/15 text-[#22c55e]">6 LONG</span>
          <span className="px-2 py-1 rounded bg-[#ef4444]/15 text-[#ef4444]">2 SHORT</span>
          <span className="px-2 py-1 rounded bg-[#eab308]/15 text-[#eab308]">8 WATCH</span>
          <span className="px-2 py-1 rounded bg-[#8b949e]/15 text-[#8b949e]">3 NO_TRADE</span>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-3">
        {signals.map((s) => (
          <div key={s.asset} className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <span className="text-lg font-bold font-mono">{s.asset}</span>
                <span className={`direction-badge direction-${s.direction.toLowerCase()}`}>{s.direction}</span>
                <span className="text-xs text-[#8b949e]">Risk: {s.risk}</span>
              </div>
              <div className="flex items-center gap-4 text-xs font-mono">
                <span>Confidence: <span className="text-[#e6edf3]">{s.confidence}%</span></span>
                <span>Score: <span style={{color: s.composite >= 70 ? '#22c55e' : s.composite >= 50 ? '#eab308' : '#ef4444'}}>{s.composite}</span></span>
              </div>
            </div>
            <div className="grid grid-cols-4 gap-2 mb-3">
              {[
                { label: "Technical", score: s.tech },
                { label: "Fundamental", score: s.fund },
                { label: "Whale", score: s.whale },
                { label: "Derivative", score: s.deriv },
              ].map((dim) => (
                <div key={dim.label} className="text-center">
                  <div className="text-[10px] text-[#8b949e] mb-1">{dim.label}</div>
                  <div className="score-bar"><div className="score-bar-fill" style={{width: `${dim.score}%`, backgroundColor: dim.score >= 70 ? '#22c55e' : dim.score >= 50 ? '#eab308' : '#ef4444'}}></div></div>
                  <div className="text-xs font-mono mt-1" style={{color: dim.score >= 70 ? '#22c55e' : dim.score >= 50 ? '#eab308' : '#ef4444'}}>{dim.score}</div>
                </div>
              ))}
            </div>
            <div className="flex flex-wrap gap-2">
              {s.reasons.map((r, i) => (
                <span key={i} className="text-[10px] bg-[#1a1a2e] text-[#8b949e] px-2 py-0.5 rounded">{r}</span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
