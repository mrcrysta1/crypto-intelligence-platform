"use client";

export default function ScreenerPage() {
  const assets = [
    { rank: 1, symbol: "BTC", name: "Bitcoin", price: 67432.18, change24h: 2.34, marketCap: 1324000000000, volume24h: 28500000000, fundamental: 92, technical: 78, whale: 85, derivative: 71, composite: 82, direction: "LONG", confidence: 87, risk: "low" },
    { rank: 2, symbol: "SOL", name: "Solana", price: 178.92, change24h: 5.67, marketCap: 78000000000, volume24h: 3200000000, fundamental: 82, technical: 88, whale: 75, derivative: 72, composite: 81, direction: "LONG", confidence: 85, risk: "medium" },
    { rank: 3, symbol: "ETH", name: "Ethereum", price: 3521.45, change24h: 1.87, marketCap: 423000000000, volume24h: 15200000000, fundamental: 88, technical: 72, whale: 80, derivative: 68, composite: 78, direction: "LONG", confidence: 82, risk: "low" },
    { rank: 4, symbol: "BNB", name: "BNB", price: 598.32, change24h: -0.45, marketCap: 92000000000, volume24h: 1800000000, fundamental: 75, technical: 55, whale: 62, derivative: 58, composite: 64, direction: "WATCH", confidence: 61, risk: "medium" },
    { rank: 5, symbol: "XRP", name: "XRP", price: 0.6234, change24h: -1.23, marketCap: 34000000000, volume24h: 1200000000, fundamental: 65, technical: 42, whale: 55, derivative: 48, composite: 53, direction: "WATCH", confidence: 52, risk: "medium" },
    { rank: 6, symbol: "ADA", name: "Cardano", price: 0.5123, change24h: -2.15, marketCap: 18000000000, volume24h: 520000000, fundamental: 60, technical: 35, whale: 48, derivative: 42, composite: 47, direction: "SHORT", confidence: 65, risk: "medium" },
    { rank: 7, symbol: "DOGE", name: "Dogecoin", price: 0.1567, change24h: 8.34, marketCap: 22000000000, volume24h: 2100000000, fundamental: 35, technical: 72, whale: 68, derivative: 55, composite: 56, direction: "WATCH", confidence: 58, risk: "high" },
    { rank: 8, symbol: "AVAX", name: "Avalanche", price: 42.67, change24h: 3.21, marketCap: 16000000000, volume24h: 650000000, fundamental: 72, technical: 65, whale: 58, derivative: 55, composite: 64, direction: "LONG", confidence: 72, risk: "medium" },
    { rank: 9, symbol: "LINK", name: "Chainlink", price: 18.92, change24h: 1.45, marketCap: 11000000000, volume24h: 420000000, fundamental: 78, technical: 58, whale: 65, derivative: 52, composite: 65, direction: "LONG", confidence: 68, risk: "medium" },
    { rank: 10, symbol: "MATIC", name: "Polygon", price: 0.7891, change24h: -3.45, marketCap: 7800000000, volume24h: 310000000, fundamental: 62, technical: 32, whale: 45, derivative: 38, composite: 45, direction: "SHORT", confidence: 62, risk: "high" },
    { rank: 11, symbol: "UNI", name: "Uniswap", price: 12.34, change24h: 2.12, marketCap: 9500000000, volume24h: 280000000, fundamental: 70, technical: 62, whale: 55, derivative: 48, composite: 60, direction: "WATCH", confidence: 62, risk: "medium" },
    { rank: 12, symbol: "SHIB", name: "Shiba Inu", price: 0.00002345, change24h: 12.56, marketCap: 14000000000, volume24h: 1500000000, fundamental: 20, technical: 75, whale: 72, derivative: 45, composite: 50, direction: "WATCH", confidence: 48, risk: "extreme" },
  ];

  return (
    <div className="space-y-4">
      <h1 className="text-lg font-semibold">Asset Screener</h1>
      <div className="flex gap-3 items-center">
        <select className="text-sm"><option>All Directions</option><option>LONG</option><option>SHORT</option><option>WATCH</option><option>NO_TRADE</option></select>
        <input type="number" placeholder="Min Score" className="text-sm w-32" />
        <input type="text" placeholder="Search symbol..." className="text-sm w-40" />
      </div>
      <div className="bg-[#12121a] border border-[#1e2d4a] rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-[10px] text-[#8b949e] uppercase tracking-wider border-b border-[#1e2d4a] bg-[#0d0d14]">
              <th className="text-left px-4 py-3">#</th>
              <th className="text-left px-4 py-3">Asset</th>
              <th className="text-right px-4 py-3">Price</th>
              <th className="text-right px-4 py-3">24h</th>
              <th className="text-right px-4 py-3">Mkt Cap</th>
              <th className="text-right px-4 py-3">Volume</th>
              <th className="text-center px-4 py-3">Fund</th>
              <th className="text-center px-4 py-3">Tech</th>
              <th className="text-center px-4 py-3">Whale</th>
              <th className="text-center px-4 py-3">Deriv</th>
              <th className="text-center px-4 py-3">Total</th>
              <th className="text-center px-4 py-3">Signal</th>
              <th className="text-center px-4 py-3">Conf</th>
            </tr>
          </thead>
          <tbody>
            {assets.map((a) => (
              <tr key={a.symbol} className="border-b border-[#1e2d4a]/30 hover:bg-[#1a1a2e]">
                <td className="px-4 py-3 text-[#8b949e]">{a.rank}</td>
                <td className="px-4 py-3"><span className="font-mono font-bold">{a.symbol}</span> <span className="text-[10px] text-[#8b949e] ml-1">{a.name}</span></td>
                <td className="px-4 py-3 text-right font-mono">${a.price >= 1 ? a.price.toLocaleString(undefined, {maximumFractionDigits:2}) : a.price}</td>
                <td className={`px-4 py-3 text-right font-mono ${a.change24h >= 0 ? 'text-[#22c55e]' : 'text-[#ef4444]'}`}>{a.change24h >= 0 ? '+' : ''}{a.change24h}%</td>
                <td className="px-4 py-3 text-right font-mono text-[#8b949e]">${(a.marketCap / 1e9).toFixed(0)}B</td>
                <td className="px-4 py-3 text-right font-mono text-[#8b949e]">${(a.volume24h / 1e9).toFixed(1)}B</td>
                <td className="px-4 py-3 text-center font-mono" style={{color: a.fundamental >= 70 ? '#22c55e' : a.fundamental >= 50 ? '#eab308' : '#ef4444'}}>{a.fundamental}</td>
                <td className="px-4 py-3 text-center font-mono" style={{color: a.technical >= 70 ? '#22c55e' : a.technical >= 50 ? '#eab308' : '#ef4444'}}>{a.technical}</td>
                <td className="px-4 py-3 text-center font-mono" style={{color: a.whale >= 70 ? '#22c55e' : a.whale >= 50 ? '#eab308' : '#ef4444'}}>{a.whale}</td>
                <td className="px-4 py-3 text-center font-mono" style={{color: a.derivative >= 70 ? '#22c55e' : a.derivative >= 50 ? '#eab308' : '#ef4444'}}>{a.derivative}</td>
                <td className="px-4 py-3 text-center font-mono font-bold" style={{color: a.composite >= 70 ? '#22c55e' : a.composite >= 50 ? '#eab308' : '#ef4444'}}>{a.composite}</td>
                <td className="px-4 py-3 text-center"><span className={`direction-badge direction-${a.direction.toLowerCase()}`}>{a.direction}</span></td>
                <td className="px-4 py-3 text-center font-mono text-[#8b949e]">{a.confidence}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
