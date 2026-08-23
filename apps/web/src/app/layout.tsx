import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Crypto Intelligence Terminal",
  description: "Multi-dimensional crypto analysis platform",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-[#0a0a0f] text-[#e6edf3] min-h-screen">
        <div className="flex min-h-screen">
          <Sidebar />
          <div className="flex-1 flex flex-col ml-60">
            <Header />
            <main className="flex-1 p-6 overflow-auto">{children}</main>
          </div>
        </div>
      </body>
    </html>
  );
}

function Sidebar() {
  const items = [
    { icon: "📊", label: "Dashboard", href: "/" },
    { icon: "🔍", label: "Screener", href: "/screener" },
    { icon: "⚡", label: "Signals", href: "/signals" },
    { icon: "🤖", label: "AI Analyst", href: "/predictions" },
    { icon: "💰", label: "Paper Trading", href: "/paper-trading" },
    { icon: "🔔", label: "Alerts", href: "/alerts" },
    { icon: "⏱", label: "Backtesting", href: "/backtesting" },
  ];
  return (
    <aside className="w-60 bg-[#12121a] border-r border-[#1e2d4a] fixed h-full flex flex-col">
      <div className="p-4 border-b border-[#1e2d4a]">
        <div className="text-xl font-bold bg-gradient-to-r from-[#38bdf8] to-[#a78bfa] bg-clip-text text-transparent font-mono">CIT</div>
        <div className="text-xs text-[#8b949e] mt-1">Crypto Intelligence Terminal</div>
      </div>
      <nav className="flex-1 p-2">
        {items.map((item) => (
          <a key={item.href} href={item.href} className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#8b949e] hover:text-[#e6edf3] hover:bg-[#1a1a2e] transition-colors mb-1">
            <span className="text-base">{item.icon}</span>
            <span>{item.label}</span>
          </a>
        ))}
      </nav>
      <div className="p-3 border-t border-[#1e2d4a]">
        <div className="text-[10px] text-[#8b949e] bg-[#1a1a2e] rounded px-2 py-1 text-center font-mono">100% Demo Mode</div>
      </div>
    </aside>
  );
}

function Header() {
  return (
    <header className="h-14 bg-[#12121a] border-b border-[#1e2d4a] flex items-center justify-between px-6 sticky top-0 z-10">
      <div className="text-sm font-mono text-[#8b949e]">CRYPTO INTELLIGENCE TERMINAL</div>
      <div className="flex items-center gap-6">
        <span className="text-xs px-2 py-0.5 rounded bg-[#22c55e]/20 text-[#22c55e] border border-[#22c55e]/30 font-mono">TRENDING UP</span>
        <div className="text-xs font-mono"><span className="text-[#8b949e]">BTC</span> <span className="text-[#22c55e]">$67,432</span></div>
        <div className="text-xs font-mono"><span className="text-[#8b949e]">ETH</span> <span className="text-[#22c55e]">$3,521</span></div>
        <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-[#22c55e] animate-pulse"></div><span className="text-xs text-[#8b949e]">Connected</span></div>
      </div>
    </header>
  );
}
