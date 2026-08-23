export function formatPrice(n: number): string {
  if (n >= 1000) return `$${n.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  if (n >= 1) return `$${n.toFixed(2)}`;
  if (n >= 0.01) return `$${n.toFixed(4)}`;
  return `$${n.toFixed(8)}`;
}

export function formatVolume(n: number): string {
  if (n >= 1e12) return `$${(n / 1e12).toFixed(1)}T`;
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(1)}M`;
  if (n >= 1e3) return `$${(n / 1e3).toFixed(1)}K`;
  return `$${n.toFixed(2)}`;
}

export function formatPercent(n: number): string {
  return `${n >= 0 ? "+" : ""}${n.toFixed(2)}%`;
}

export function formatMarketCap(n: number): string {
  if (n >= 1e12) return `$${(n / 1e12).toFixed(2)}T`;
  if (n >= 1e9) return `$${(n / 1e9).toFixed(1)}B`;
  if (n >= 1e6) return `$${(n / 1e6).toFixed(0)}M`;
  return `$${n.toLocaleString()}`;
}

export function getScoreColor(n: number): string {
  if (n >= 70) return "#22c55e";
  if (n >= 50) return "#eab308";
  if (n >= 30) return "#f97316";
  return "#ef4444";
}

export function getDirectionColor(d: string): string {
  switch (d) {
    case "LONG": return "#22c55e";
    case "SHORT": return "#ef4444";
    case "WATCH": return "#eab308";
    default: return "#8b949e";
  }
}

export function getDirectionBadgeClass(d: string): string {
  switch (d) {
    case "LONG": return "direction-long";
    case "SHORT": return "direction-short";
    case "WATCH": return "direction-watch";
    default: return "direction-no-trade";
  }
}

export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(" ");
}

export function formatTimeAgo(date: string | Date): string {
  const now = new Date();
  const d = typeof date === "string" ? new Date(date) : date;
  const diff = now.getTime() - d.getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  return `${days}d ago`;
}
