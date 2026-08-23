export default function PaperTradingPage() {
  const portfolio = { cash: 45230.50, total: 100000, unrealizedPnl: 3250.75, realizedPnl: 1200 };
  const positions = [
    { symbol: "BTC", side: "long", entry: 65200, current: 67432.18, size: 25000, pnl: 856.25, opened: "Aug 21" },
    { symbol: "SOL", side: "long", entry: 165, current: 178.92, size: 15000, pnl: 1265.45, opened: "Aug 22" },
    { symbol: "ETH", side: "long", entry: 3480, current: 3521.45, size: 15000, pnl: 128.93, opened: "Aug 23" },
  ];

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Paper Trading</h1>

      <div className="grid grid-cols-4 gap-4">
        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <div className="text-[10px] text-[#8b949e] uppercase">Cash Balance</div>
          <div className="text-xl font-bold font-mono mt-1">${portfolio.cash.toLocaleString()}</div>
        </div>
        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <div className="text-[10px] text-[#8b949e] uppercase">Total Value</div>
          <div className="text-xl font-bold font-mono mt-1">${portfolio.total.toLocaleString()}</div>
        </div>
        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <div className="text-[10px] text-[#8b949e] uppercase">Unrealized P&L</div>
          <div className="text-xl font-bold font-mono mt-1 text-[#22c55e]">+${portfolio.unrealizedPnl.toLocaleString()}</div>
        </div>
        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <div className="text-[10px] text-[#8b949e] uppercase">Realized P&L</div>
          <div className="text-xl font-bold font-mono mt-1 text-[#22c55e]">+${portfolio.realizedPnl.toLocaleString()}</div>
        </div>
      </div>

      <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
        <h2 className="text-sm font-semibold mb-3">Open Positions</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-[10px] text-[#8b949e] uppercase border-b border-[#1e2d4a]">
              <th className="text-left py-2">Asset</th>
              <th className="text-center py-2">Side</th>
              <th className="text-right py-2">Entry</th>
              <th className="text-right py-2">Current</th>
              <th className="text-right py-2">Size</th>
              <th className="text-right py-2">P&L</th>
              <th className="text-right py-2">Opened</th>
            </tr>
          </thead>
          <tbody>
            {positions.map((p) => (
              <tr key={p.symbol} className="border-b border-[#1e2d4a]/30">
                <td className="py-3 font-mono font-bold">{p.symbol}</td>
                <td className="py-3 text-center"><span className={`direction-badge direction-${p.side}`}>{p.side.toUpperCase()}</span></td>
                <td className="py-3 text-right font-mono">${p.entry.toLocaleString()}</td>
                <td className="py-3 text-right font-mono">${p.current.toLocaleString()}</td>
                <td className="py-3 text-right font-mono">${p.size.toLocaleString()}</td>
                <td className="py-3 text-right font-mono text-[#22c55e]">+${p.pnl.toFixed(2)}</td>
                <td className="py-3 text-right text-[#8b949e]">{p.opened}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
        <h2 className="text-sm font-semibold mb-3">New Order</h2>
        <div className="flex gap-3 items-end">
          <div><label className="text-[10px] text-[#8b949e] block mb-1">Asset</label><input className="text-sm w-24" placeholder="BTC" /></div>
          <div><label className="text-[10px] text-[#8b949e] block mb-1">Side</label><select className="text-sm"><option>BUY</option><option>SELL</option></select></div>
          <div><label className="text-[10px] text-[#8b949e] block mb-1">Amount ($)</label><input className="text-sm w-32" placeholder="1000" type="number" /></div>
          <button className="bg-[#38bdf8] text-[#0a0a0f] px-4 py-2 rounded text-sm font-semibold hover:bg-[#7dd3fc]">Execute</button>
        </div>
      </div>
    </div>
  );
}
