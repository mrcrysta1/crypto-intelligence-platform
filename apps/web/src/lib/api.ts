const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchApi<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}

export const api = {
  getAssets: () => fetchApi<{ assets: import("@/types").Asset[] }>("/api/assets/"),
  getAsset: (symbol: string) => fetchApi<import("@/types").Asset>(`/api/assets/${symbol}`),
  getRankings: (params?: Record<string, string>) => fetchApi<{ rankings: import("@/types").Ranking[] }>(`/api/rankings/${params ? "?" + new URLSearchParams(params) : ""}`),
  getSignals: (params?: Record<string, string>) => fetchApi<{ signals: import("@/types").Signal[] }>(`/api/signals/${params ? "?" + new URLSearchParams(params) : ""}`),
  getPredictions: () => fetchApi<{ predictions: import("@/types").Prediction[] }>("/api/predictions/"),
  getMarketOverview: () => fetchApi<Record<string, unknown>>("/api/market/overview"),
  getWhaleActivity: () => fetchApi<{ events: import("@/types").WhaleEvent[] }>("/api/market/whale-activity"),
  getNews: () => fetchApi<{ articles: import("@/types").NewsArticle[] }>("/api/market/news"),
  getPortfolio: () => fetchApi<Record<string, unknown>>("/api/paper-trading/portfolio"),
  getPositions: () => fetchApi<{ positions: import("@/types").PaperPosition[] }>("/api/paper-trading/positions"),
  getAlerts: () => fetchApi<{ alerts: import("@/types").Alert[] }>("/api/alerts/"),
  getBacktests: () => fetchApi<{ backtests: import("@/types").Backtest[] }>("/api/backtests/"),
  getAIAnalysis: (symbol: string) => fetchApi<import("@/types").AIAnalysis>(`/api/ai/analyze`, { method: "POST", body: JSON.stringify({ symbol }) }),
  getMarketSummary: () => fetchApi<Record<string, unknown>>("/api/ai/market-summary"),
};
