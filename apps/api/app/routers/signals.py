from fastapi import APIRouter

router = APIRouter(prefix="/api/signals", tags=["signals"])

SIGNALS = [
    {"asset": "BTC", "direction": "LONG", "confidence": 0.87, "composite_score": 82, "reasons": ["Strong technical momentum", "ETF inflows bullish", "Whale accumulation pattern"], "risk_level": "low", "technical_score": 78, "fundamental_score": 92, "whale_score": 85, "derivative_score": 71},
    {"asset": "ETH", "direction": "LONG", "confidence": 0.82, "composite_score": 78, "reasons": ["L2 growth driving demand", "Staking yield attractive", "Network activity rising"], "risk_level": "low", "technical_score": 72, "fundamental_score": 88, "whale_score": 80, "derivative_score": 68},
    {"asset": "SOL", "direction": "LONG", "confidence": 0.85, "composite_score": 81, "reasons": ["Strong momentum breakout", "Meme coin activity boosting fees", "Validator count increasing"], "risk_level": "medium", "technical_score": 88, "fundamental_score": 82, "whale_score": 75, "derivative_score": 72},
    {"asset": "ADA", "direction": "SHORT", "confidence": 0.65, "composite_score": 47, "reasons": ["Weak technical structure", "Declining on-chain metrics", "Bearish market structure"], "risk_level": "medium", "technical_score": 35, "fundamental_score": 60, "whale_score": 48, "derivative_score": 42},
    {"asset": "MATIC", "direction": "SHORT", "confidence": 0.62, "composite_score": 45, "reasons": ["Below key support", "Declining volume", "Whale selling pressure"], "risk_level": "high", "technical_score": 32, "fundamental_score": 62, "whale_score": 45, "derivative_score": 38},
    {"asset": "DOGE", "direction": "WATCH", "confidence": 0.58, "composite_score": 56, "reasons": ["High volatility", "Social sentiment mixed", "Unsustainable pump possible"], "risk_level": "high", "technical_score": 72, "fundamental_score": 35, "whale_score": 68, "derivative_score": 55},
    {"asset": "BNB", "direction": "WATCH", "confidence": 0.61, "composite_score": 64, "reasons": ["Neutral technical setup", "Regulatory overhang", "Exchange volume stable"], "risk_level": "medium", "technical_score": 55, "fundamental_score": 75, "whale_score": 62, "derivative_score": 58},
    {"asset": "XRP", "direction": "WATCH", "confidence": 0.52, "composite_score": 53, "reasons": ["Consolidating in range", "Awaiting legal clarity", "Low conviction signal"], "risk_level": "medium", "technical_score": 42, "fundamental_score": 65, "whale_score": 55, "derivative_score": 48},
    {"asset": "AVAX", "direction": "LONG", "confidence": 0.72, "composite_score": 64, "reasons": ["Recovery momentum", "Subnet adoption growing", "Technical breakout forming"], "risk_level": "medium", "technical_score": 65, "fundamental_score": 72, "whale_score": 58, "derivative_score": 55},
    {"asset": "LINK", "direction": "LONG", "confidence": 0.68, "composite_score": 65, "reasons": ["Oracle demand increasing", "CCIP adoption growing", "Technical support holding"], "risk_level": "medium", "technical_score": 58, "fundamental_score": 78, "whale_score": 65, "derivative_score": 52},
    {"asset": "NEAR", "direction": "LONG", "confidence": 0.70, "composite_score": 64, "reasons": ["Chain abstraction narrative", "Developer activity rising", "Technical momentum"], "risk_level": "medium", "technical_score": 70, "fundamental_score": 68, "whale_score": 60, "derivative_score": 55},
    {"asset": "BCH", "direction": "NO_TRADE", "confidence": 0.42, "composite_score": 44, "reasons": ["Low conviction signal", "Conflicting indicators", "Insufficient volume"], "risk_level": "medium", "technical_score": 42, "fundamental_score": 55, "whale_score": 38, "derivative_score": 35},
    {"asset": "FIL", "direction": "NO_TRADE", "confidence": 0.40, "composite_score": 44, "reasons": ["Weak trend", "Declining usage metrics", "No clear catalyst"], "risk_level": "high", "technical_score": 38, "fundamental_score": 58, "whale_score": 42, "derivative_score": 35},
]

@router.get("/")
async def get_signals(min_confidence: float = 0.0, direction: str = None):
    filtered = SIGNALS
    if direction:
        filtered = [s for s in filtered if s["direction"] == direction.upper()]
    if min_confidence > 0:
        filtered = [s for s in filtered if s["confidence"] >= min_confidence]
    return {"signals": filtered, "total": len(filtered)}

@router.get("/latest")
async def latest_signals():
    return {"signals": SIGNALS, "generated_at": "2026-08-24T01:00:00Z", "model_version": "v1.0.0"}

@router.get("/conflicts")
async def conflicting_signals():
    conflicts = [
        {"asset": "DOGE", "conflict": "Technical bullish but fundamentals weak", "technical": 72, "fundamental": 35, "recommendation": "Wait for confirmation"},
        {"asset": "SHIB", "conflict": "Social hype vs weak on-chain", "social": 85, "onchain": 30, "recommendation": "High risk, small position only"},
    ]
    return {"conflicts": conflicts}
