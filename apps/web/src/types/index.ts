export interface Asset {
  symbol: string;
  name: string;
  slug: string;
  price: number;
  change24h: number;
  marketCap: number;
  volume24h: number;
  liquidityScore: number;
  fundamentalScore: number;
  technicalScore: number;
  whaleScore: number;
  derivativeScore: number;
  compositeScore: number;
  direction: "LONG" | "SHORT" | "WATCH" | "NO_TRADE";
  confidence: number;
  riskLevel: "low" | "medium" | "high" | "extreme";
}

export interface Signal {
  asset: string;
  direction: "LONG" | "SHORT" | "WATCH" | "NO_TRADE";
  confidence: number;
  composite_score: number;
  reasons: string[];
  risk_level: string;
  technical_score: number;
  fundamental_score: number;
  whale_score: number;
  derivative_score: number;
}

export interface Ranking {
  rank: number;
  symbol: string;
  composite_score: number;
  direction: string;
  confidence: number;
  price: number;
  change24h: number;
  market_cap: number;
}

export interface Prediction {
  symbol: string;
  p_long: number;
  p_short: number;
  p_neutral: number;
  model_version: string;
  confidence: number;
}

export interface WhaleEvent {
  type: string;
  asset: string;
  amount_usd: string;
  from: string;
  to: string;
  timestamp: string;
  sentiment: string;
}

export interface NewsArticle {
  title: string;
  source: string;
  sentiment: number;
  impact: string;
  published_at: string;
  related_assets: string[];
}

export interface PaperPosition {
  id: string;
  symbol: string;
  side: string;
  entry_price: number;
  current_price: number;
  size_usd: number;
  unrealized_pnl: number;
  opened_at: string;
}

export interface Backtest {
  id: string;
  strategy: string;
  symbol: string;
  total_return: number;
  sharpe_ratio: number;
  max_drawdown: number;
  win_rate: number;
  total_trades: number;
}

export interface Alert {
  id: string;
  symbol: string;
  alert_type: string;
  condition: Record<string, unknown>;
  is_active: boolean;
  message: string;
  last_triggered: string | null;
}

export interface AIAnalysis {
  asset: string;
  analysis: string;
  prediction: { p_long: number; p_short: number; p_neutral: number };
  reasoning: string[];
  risks: string[];
  type: string;
  model_version: string;
}

export type MarketRegime = "trending_up" | "trending_down" | "ranging" | "volatile";
