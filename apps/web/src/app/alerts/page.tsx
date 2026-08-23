export default function AlertsPage() {
  const alerts = [
    { id: "1", symbol: "BTC", type: "price", condition: "above $70,000", active: true, lastTriggered: null, created: "Aug 22" },
    { id: "2", symbol: "ETH", type: "signal", condition: "LONG with >80% confidence", active: true, lastTriggered: "Aug 23 14:00", created: "Aug 21" },
    { id: "3", symbol: "SOL", type: "whale", condition: "transfer > $5M", active: true, lastTriggered: "Aug 24 00:18", created: "Aug 20" },
    { id: "4", symbol: "BTC", type: "score", condition: "composite > 85", active: false, lastTriggered: "Aug 23 08:00", created: "Aug 19" },
  ];

  const triggers = [
    { alert: "SOL whale transfer", time: "Aug 24 00:18", data: "Exchange outflow $8.5M" },
    { alert: "ETH signal alert", time: "Aug 23 14:00", data: "LONG signal confidence 85%" },
    { alert: "BTC score alert", time: "Aug 23 08:00", data: "Composite score reached 87" },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-lg font-semibold">Alerts</h1>
        <button className="bg-[#38bdf8] text-[#0a0a0f] px-3 py-1.5 rounded text-xs font-semibold">+ New Alert</button>
      </div>

      <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
        <h2 className="text-sm font-semibold mb-3">Active Alerts</h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="text-[10px] text-[#8b949e] uppercase border-b border-[#1e2d4a]">
              <th className="text-left py-2">Asset</th>
              <th className="text-left py-2">Type</th>
              <th className="text-left py-2">Condition</th>
              <th className="text-center py-2">Active</th>
              <th className="text-right py-2">Last Triggered</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((a) => (
              <tr key={a.id} className="border-b border-[#1e2d4a]/30">
                <td className="py-3 font-mono font-bold">{a.symbol}</td>
                <td className="py-3"><span className="text-xs px-2 py-0.5 rounded bg-[#1a1a2e] text-[#8b949e]">{a.type}</span></td>
                <td className="py-3 text-[#8b949e]">{a.condition}</td>
                <td className="py-3 text-center"><span className={`w-2 h-2 rounded-full inline-block ${a.active ? 'bg-[#22c55e]' : 'bg-[#8b949e]'}`}></span></td>
                <td className="py-3 text-right text-[#8b949e] text-xs">{a.lastTriggered || "Never"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg p-4">
        <h2 className="text-sm font-semibold mb-3">Recent Triggers</h2>
        <div className="space-y-2">
          {triggers.map((t, i) => (
            <div key={i} className="flex items-center justify-between text-xs py-2 border-b border-[#1e2d4a]/30 last:border-0">
              <div className="flex items-center gap-2">
                <span className="w-1.5 h-1.5 rounded-full bg-[#eab308]"></span>
                <span className="font-semibold">{t.alert}</span>
              </div>
              <span className="text-[#8b949e]">{t.data}</span>
              <span className="text-[#8b949e] font-mono">{t.time}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
