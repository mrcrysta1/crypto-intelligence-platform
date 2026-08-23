export default function Dashboard() {
  const assets = [
    { rank: 1, symbol: "BTC", name: "Bitcoin", price: 67432.18, change24h: 2.34, compositeScore: 82, direction: "LONG", confidence: 87 },
    { rank: 2, symbol: "SOL", name: "Solana", price: 178.92, change24h: 5.67, compositeScore: 81, direction: "LONG", confidence: 85 },
    { rank: 3, symbol: "ETH", name: "Ethereum", price: 3521.45, change24h: 1.87, compositeScore: 78, direction: "LONG", confidence: 82 },
    { rank: 4, symbol: "AVAX", name: "Avalanche", price: 42.67, change24h: 3.21, compositeScore: 64, direction: "LONG", confidence: 72 },
    { rank: 5, symbol: "LINK", name: "Chainlink", price: 18.92, change24h: 1.45, compositeScore: 65, direction: "LONG", confidence: 68 },
    { rank: 6, symbol: "NEAR", name: "NEAR Protocol", price: 7.89, change24h: 4.56, compositeScore: 64, direction: "LONG", confidence: 70 },
    { rank: 7, symbol: "BNB", name: "BNB", price: 598.32, change24h: -0.45, compositeScore: 64, direction: "WATCH", confidence: 61 },
    { rank: 8, symbol: "UNI", name: "Uniswap", price: 12.34, change24h: 2.12, compositeScore: 60, direction: "WATCH", confidence: 62 },
    { rank: 9, symbol: "DOGE", name: "Dogecoin", price: 0.1567, change24h: 8.34, compositeScore: 56, direction: "WATCH", confidence: 58 },
    { rank: 10, symbol: "APT", name: "Aptos", price: 9.45, change24h: 2.78, compositeScore: 56, direction: "WATCH", confidence: 58 },
  ];

  const whales = [
    { type: "large_transfer", asset: "BTC", amount: "$45.2M", from: "0x742d...8f2a", to: "Coinbase", sentiment: "neutral" },
    { type: "accumulation", asset: "ETH", amount: "$12.8M", from: "Unknown", to: "0x3f5c...9a1b", sentiment: "bullish" },
    { type: "exchange_outflow", asset: "SOL", amount: "$8.5M", from: "Binance", to: "Cold Wallet", sentiment: "bullish" },
    { type: "distribution", asset: "DOGE", amount: "$5.2M", from: "Whale", to: "Multiple", sentiment: "bearish" },
  ];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Fundamental", score: 66, icon: "📈", color: "#38bdf8" },
          { label: "Technical", score: 55, icon: "📊", color: "#a78bfa" },
          { label: "Whale Activity", score: 58, icon: "🐋", color: "#22c55e" },
          { label: "Derivatives", score: 50, icon: "📉", color: "#eab308" },
        ].map((card) => (
          <div key={card.label} className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-[#8b949e] uppercase tracking-wider">{card.label}</span>
              <span className="text-lg">{card.icon}</span>
            </div>
            <div className="text-2xl font-bold font-mono" style={{ color: card.color }}>{card.score}</div>
            <div className="w-full bg-[#1a1a2e] rounded-full h-1.5 mt-2">
              <div className="h-1.5 rounded-full" style={{ width: `${card.score}%`, backgroundColor: card.color }}></div>
            </div>
            <div className="text-[10px] text-[#8b949e] mt-1">Average Score</div>
          </div>
        ))}
      </div>

      <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
        <h2 className="text-sm font-semibold mb-3 text-[#e6edf3]">Top 10 Opportunities</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-[10px] text-[#8b949e] uppercase tracking-wider border-b border-[#1e2d4a]">
              <th className="text-left py-2">#</th>
              <th className="text-left py-2">Asset</th>
              <th className="text-right py-2">Price</th>
              <th className="text-right py-2">24h</th>
              <th className="text-right py-2">Score</th>
              <th className="text-center py-2">Signal</th>
              <th className="text-right py-2">Confidence</th>
            </tr>
          </thead>
          <tbody>
            {assets.map((a) => (
              <tr key={a.symbol} className="border-b border-[#1e2d4a]/50 hover:bg-[#1a1a2e]">
                <td className="py-2.5 text-[#8b949e]">{a.rank}</td>
                <td className="py-2.5"><span className="font-mono font-semibold">{a.symbol}</span> <span className="text-[10px] text-[#8b949e]">{a.name}</span></td>
                <td className="py-2.5 text-right font-mono">${a.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                <td className={`py-2.5 text-right font-mono ${a.change24h >= 0 ? 'text-[#22c55e]' : 'text-[#ef4444]'}`}>{a.change24h >= 0 ? '+' : ''}{a.change24h}%</td>
                <td className="py-2.5 text-right">
                  <span className={`font-mono ${a.compositeScore >= 70 ? 'text-[#22c55e]' : a.compositeScore >= 50 ? 'text-[#eab308]' : 'text-[#ef4444]'}`}>{a.compositeScore}</span>
                </td>
                <td className="py-2.5 text-center">
                  <span className={`text-[10px] px-2 py-0.5 rounded font-mono ${a.direction === 'LONG' ? 'bg-[#22c55e]/20 text-[#22c55e]' : a.direction === 'SHORT' ? 'bg-[#ef4444]/20 text-[#ef4444]' : 'bg-[#eab308]/20 text-[#eab308]'}`}>{a.direction}</span>
                </td>
                <td className="py-2.5 text-right font-mono text-[#8b949e]">{a.confidence}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <h2 className="text-sm font-semibold mb-3 text-[#e6edf3]">Whale Activity</h2>
          <div className="space-y-3">
            {whales.map((w, i) => (
              <div key={i} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  <span className={`w-1.5 h-1.5 rounded-full ${w.sentiment === 'bullish' ? 'bg-[#22c55e]' : w.sentiment === 'bearish' ? 'bg-[#ef4444]' : 'bg-[#8b949e]'}`}></span>
                  <span className="font-mono font-semibold">{w.asset}</span>
                  <span className="text-[#8b949e]">{w.type.replace('_', ' ')}</span>
                </div>
                <span className="font-mono">{w.amount}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <h2 className="text-sm font-semibold mb-3 text-[#e6edf3]">AI Analyst</h2>
          <div className="space-y-3">
            <div className="bg-[#1a1a2e] rounded p-3">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#a78bfa]/20 text-[#a78bfa] font-mono">MODEL_OUTPUT</span>
                <span className="text-[10px] text-[#8b949e]">BTC 7d forecast</span>
              </div>
              <div className="flex gap-4 text-xs font-mono">
                <span className="text-[#22c55e]">↑ 72% LONG</span>
                <span className="text-[#ef4444]">↓ 12% SHORT</span>
                <span className="text-[#8b949e]">→ 16% NEUTRAL</span>
              </div>
            </div>
            <div className="bg-[#1a1a2e] rounded p-3">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-[10px] px-1.5 py-0.5 rounded bg-[#38bdf8]/20 text-[#38bdf8] font-mono">AI_INTERPRETATION</span>
              </div>
              <p className="text-xs text-[#8b949e] leading-relaxed">Bitcoin is showing strong bullish momentum with technical indicators confirming the uptrend. ETF inflows continue to provide structural demand.</p>
            </div>
            <div className="text-[10px] text-[#eab308] flex items-center gap-1">⚠ AI interpretations are subjective and may differ from model output</div>
          </div>
        </div>
      </div>
    </div>
  );
}
