export default function BacktestingPage() {
  const strategies = [
    { id: "1", name: "Momentum Breakout", desc: "Buy on EMA crossover with volume confirmation", params: "EMA 12/26, Vol > 1.5x avg" },
    { id: "2", name: "Mean Reversion RSI", desc: "Buy oversold RSI, sell overbought RSI", params: "RSI 14, Buy <30, Sell >70" },
    { id: "3", name: "Whale Following", desc: "Follow large wallet accumulation", params: "Whale score >70, 3 bar confirm" },
    { id: "4", name: "Composite Signal", desc: "Trade on composite score threshold", params: "Long >70, Short <30, Conf >0.7" },
  ];

  const backtests = [
    { id: "1", strategy: "Momentum Breakout", symbol: "BTC", return: 84.5, sharpe: 2.14, drawdown: 12, winRate: 62, trades: 45 },
    { id: "2", strategy: "Mean Reversion RSI", symbol: "ETH", return: 52.0, sharpe: 1.78, drawdown: 18, winRate: 58, trades: 62 },
    { id: "3", strategy: "Composite Signal", symbol: "BTC", return: 113.0, sharpe: 2.45, drawdown: 15, winRate: 68, trades: 38 },
  ];

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Backtesting</h1>

      <div className="grid grid-cols-2 gap-4">
        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <h2 className="text-sm font-semibold mb-3">Available Strategies</h2>
          <div className="space-y-2">
            {strategies.map((s) => (
              <div key={s.id} className="bg-[#1a1a2e] rounded p-3 hover:bg-[#1e2d4a] cursor-pointer">
                <div className="font-semibold text-sm">{s.name}</div>
                <div className="text-[10px] text-[#8b949e] mt-1">{s.desc}</div>
                <div className="text-[10px] text-[#38bdf8] mt-1 font-mono">{s.params}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
          <h2 className="text-sm font-semibold mb-3">Run Backtest</h2>
          <div className="space-y-3">
            <div><label className="text-[10px] text-[#8b949e] block mb-1">Strategy</label><select className="text-sm w-full">{strategies.map(s => <option key={s.id}>{s.name}</option>)}</select></div>
            <div><label className="text-[10px] text-[#8b949e] block mb-1">Asset</label><select className="text-sm w-full"><option>BTC</option><option>ETH</option><option>SOL</option><option>ALL</option></select></div>
            <div className="grid grid-cols-2 gap-3">
              <div><label className="text-[10px] text-[#8b949e] block mb-1">Start Date</label><input type="date" className="text-sm w-full" defaultValue="2026-01-01" /></div>
              <div><label className="text-[10px] text-[#8b949e] block mb-1">End Date</label><input type="date" className="text-sm w-full" defaultValue="2026-08-24" /></div>
            </div>
            <div><label className="text-[10px] text-[#8b949e] block mb-1">Initial Capital ($)</label><input type="number" className="text-sm w-full" defaultValue={10000} /></div>
            <button className="w-full bg-[#38bdf8] text-[#0a0a0f] py-2 rounded text-sm font-semibold hover:bg-[#7dd3fc]">Run Backtest</button>
          </div>
        </div>
      </div>

      <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
        <h2 className="text-sm font-semibold mb-3">Results</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-[10px] text-[#8b949e] uppercase border-b border-[#1e2d4a]">
              <th className="text-left py-2">Strategy</th>
              <th className="text-left py-2">Asset</th>
              <th className="text-right py-2">Return</th>
              <th className="text-right py-2">Sharpe</th>
              <th className="text-right py-2">Max DD</th>
              <th className="text-right py-2">Win Rate</th>
              <th className="text-right py-2">Trades</th>
            </tr>
          </thead>
          <tbody>
            {backtests.map((b) => (
              <tr key={b.id} className="border-b border-[#1e2d4a]/30 hover:bg-[#1a1a2e]">
                <td className="py-3 font-semibold">{b.strategy}</td>
                <td className="py-3 font-mono">{b.symbol}</td>
                <td className="py-3 text-right font-mono text-[#22c55e]">+{b.return}%</td>
                <td className="py-3 text-right font-mono">{b.sharpe}</td>
                <td className="py-3 text-right font-mono text-[#ef4444]">-{b.drawdown}%</td>
                <td className="py-3 text-right font-mono">{b.winRate}%</td>
                <td className="py-3 text-right font-mono text-[#8b949e]">{b.trades}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
