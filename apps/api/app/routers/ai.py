from fastapi import APIRouter

router = APIRouter(prefix="/api/ai", tags=["ai-analyst"])

ANALYSES = {
    "BTC": {
        "asset": "BTC",
        "analysis": "Bitcoin is showing strong bullish momentum with technical indicators confirming the uptrend. ETF inflows continue to provide structural demand, while on-chain metrics show accumulation by large holders. The composite score of 82/100 reflects alignment across all dimensions. Risk is contained with clear support levels.",
        "prediction": {"p_long": 0.72, "p_short": 0.12, "p_neutral": 0.16},
        "reasoning": [
            "Technical: Price above all key EMAs, RSI at 62 (bullish), MACD positive",
            "Fundamental: ETF inflows averaging $500M/day, halving supply shock in effect",
            "Whale: Net accumulation pattern, exchange outflows dominant",
            "Derivatives: Positive funding but not overheated, OI increasing steadily"
        ],
        "risks": ["Regulatory uncertainty persists", "Potential profit-taking at $70K resistance"],
        "type": "AI_INTERPRETATION",
        "model_version": "v1.0.0",
        "generated_at": "2026-08-24T01:00:00Z",
    },
    "ETH": {
        "asset": "ETH",
        "analysis": "Ethereum benefits from strong L2 ecosystem growth and increasing staking yields. While BTC correlation remains high, ETH shows independent strength from network usage. The ETH/BTC ratio appears to be finding a bottom.",
        "prediction": {"p_long": 0.68, "p_short": 0.14, "p_neutral": 0.18},
        "reasoning": [
            "Technical: Consolidating above $3,400 support, momentum building",
            "Fundamental: L2 TVL at ATH, staking rate attractive at 3.8%",
            "Whale: Moderate accumulation, some profit-taking at highs",
            "Derivatives: Neutral funding, healthy open interest growth"
        ],
        "risks": ["Competition from alternative L1s", "Gas fees could spike during NFT mania"],
        "type": "AI_INTERPRETATION",
        "model_version": "v1.0.0",
        "generated_at": "2026-08-24T01:00:00Z",
    },
    "SOL": {
        "asset": "SOL",
        "analysis": "Solana continues its strong recovery with meme coin activity driving network usage and fee revenue. Technical momentum is the strongest among major alts. However, the elevated activity may not be sustainable long-term.",
        "prediction": {"p_long": 0.74, "p_short": 0.10, "p_neutral": 0.16},
        "reasoning": [
            "Technical: Breaking out of consolidation, strong volume confirmation",
            "Fundamental: Network activity metrics at cycle highs",
            "Whale: Net inflows to non-exchange wallets suggest accumulation",
            "Derivatives: Slightly elevated funding indicates bullish positioning"
        ],
        "risks": ["Meme coin activity could reverse quickly", "Network stability concerns remain"],
        "type": "AI_INTERPRETATION",
        "model_version": "v1.0.0",
        "generated_at": "2026-08-24T01:00:00Z",
    },
}

@router.post("/analyze")
async def analyze(request: dict):
    symbol = request.get("symbol", "BTC").upper()
    if symbol in ANALYSES:
        return ANALYSES[symbol]
    return {
        "asset": symbol,
        "analysis": f"Insufficient data for {symbol}. Recommend gathering more market data before generating analysis.",
        "prediction": {"p_long": 0.33, "p_short": 0.33, "p_neutral": 0.34},
        "reasoning": ["Insufficient data", "Model confidence too low"],
        "risks": ["Cannot generate reliable analysis without sufficient data"],
        "type": "AI_INTERPRETATION",
        "model_version": "v1.0.0",
        "generated_at": "2026-08-24T01:00:00Z",
    }

@router.get("/analyses")
async def get_recent_analyses():
    return {"analyses": list(ANALYSES.values())}

@router.get("/market-summary")
async def market_summary():
    return {
        "summary": "Crypto markets are in a bullish trending regime with Bitcoin leading at $67.4K. Total market cap stands at $2.45T with strong institutional inflows via ETFs. Altcoins are showing mixed performance, with SOL and NEAR outperforming while ADA and MATIC lag. Whale activity shows net accumulation across major assets. Risk sentiment is moderately bullish.",
        "market_regime": "trending_up",
        "key_levels": {"btc_support": 65000, "btc_resistance": 70000, "eth_support": 3400, "eth_resistance": 3800},
        "top_themes": ["ETF inflows", "L2 growth", "Meme coin mania", "Institutional adoption"],
        "type": "AI_INTERPRETATION",
        "generated_at": "2026-08-24T01:00:00Z",
    }
