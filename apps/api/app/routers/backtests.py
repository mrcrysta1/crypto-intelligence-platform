from fastapi import APIRouter

router = APIRouter(prefix="/api/backtests", tags=["backtesting"])

STRATEGIES = [
    {"id": "strat-1", "name": "Momentum Breakout", "description": "Buy on EMA crossover with volume confirmation", "parameters": {"fast_ema": 12, "slow_ema": 26, "volume_threshold": 1.5}, "is_active": True},
    {"id": "strat-2", "name": "Mean Reversion RSI", "description": "Buy oversold RSI, sell overbought RSI", "parameters": {"rsi_period": 14, "oversold": 30, "overbought": 70}, "is_active": True},
    {"id": "strat-3", "name": "Whale Following", "description": "Follow large wallet accumulation patterns", "parameters": {"min_whale_score": 70, "confirmation_bars": 3}, "is_active": True},
    {"id": "strat-4", "name": "Composite Signal", "description": "Trade based on composite score threshold", "parameters": {"long_threshold": 70, "short_threshold": 30, "min_confidence": 0.7}, "is_active": True},
]

BACKTESTS = [
    {"id": "bt-1", "strategy": "Momentum Breakout", "symbol": "BTC", "start_date": "2026-01-01", "end_date": "2026-08-24", "initial_capital": 10000, "final_capital": 18450, "total_return": 0.845, "sharpe_ratio": 2.14, "max_drawdown": 0.12, "win_rate": 0.62, "total_trades": 45, "created_at": "2026-08-24T00:30:00Z"},
    {"id": "bt-2", "strategy": "Mean Reversion RSI", "symbol": "ETH", "start_date": "2026-01-01", "end_date": "2026-08-24", "initial_capital": 10000, "final_capital": 15200, "total_return": 0.52, "sharpe_ratio": 1.78, "max_drawdown": 0.18, "win_rate": 0.58, "total_trades": 62, "created_at": "2026-08-24T00:25:00Z"},
    {"id": "bt-3", "strategy": "Composite Signal", "symbol": "BTC", "start_date": "2026-01-01", "end_date": "2026-08-24", "initial_capital": 10000, "final_capital": 21300, "total_return": 1.13, "sharpe_ratio": 2.45, "max_drawdown": 0.15, "win_rate": 0.68, "total_trades": 38, "created_at": "2026-08-24T00:20:00Z"},
]

@router.get("/strategies")
async def list_strategies():
    return {"strategies": STRATEGIES}

@router.post("/run")
async def run_backtest(params: dict):
    return {
        "status": "completed",
        "backtest": {
            "id": "bt-new",
            "strategy": params.get("strategy", "Composite Signal"),
            "symbol": params.get("symbol", "BTC"),
            "total_return": 0.89,
            "sharpe_ratio": 2.05,
            "max_drawdown": 0.14,
            "win_rate": 0.64,
            "total_trades": 42,
        }
    }

@router.get("/")
async def list_backtests():
    return {"backtests": BACKTESTS}

@router.get("/{backtest_id}")
async def get_backtest(backtest_id: str):
    bt = next((b for b in BACKTESTS if b["id"] == backtest_id), None)
    if not bt:
        return {"error": f"Backtest {backtest_id} not found"}
    return bt
