from fastapi import APIRouter

router = APIRouter(prefix="/api/paper-trading", tags=["paper-trading"])

PORTFOLIO = {
    "cash_balance": 45230.50,
    "total_value": 100000.00,
    "unrealized_pnl": 3250.75,
    "realized_pnl": 1200.00,
    "positions_count": 3,
    "created_at": "2026-08-20T00:00:00Z",
}

POSITIONS = [
    {"id": "pos-1", "symbol": "BTC", "side": "long", "entry_price": 65200.00, "current_price": 67432.18, "size_usd": 25000.00, "unrealized_pnl": 856.25, "opened_at": "2026-08-21T14:30:00Z"},
    {"id": "pos-2", "symbol": "SOL", "side": "long", "entry_price": 165.00, "current_price": 178.92, "size_usd": 15000.00, "unrealized_pnl": 1265.45, "opened_at": "2026-08-22T09:15:00Z"},
    {"id": "pos-3", "symbol": "ETH", "side": "long", "entry_price": 3480.00, "current_price": 3521.45, "size_usd": 15000.00, "unrealized_pnl": 128.93, "opened_at": "2026-08-23T11:00:00Z"},
]

ORDERS = [
    {"id": "ord-1", "symbol": "BTC", "order_type": "market", "side": "buy", "amount_usd": 25000, "price": 65200.00, "status": "filled", "created_at": "2026-08-21T14:30:00Z", "filled_at": "2026-08-21T14:30:01Z"},
    {"id": "ord-2", "symbol": "SOL", "order_type": "market", "side": "buy", "amount_usd": 15000, "price": 165.00, "status": "filled", "created_at": "2026-08-22T09:15:00Z", "filled_at": "2026-08-22T09:15:01Z"},
    {"id": "ord-3", "symbol": "ETH", "order_type": "market", "side": "buy", "amount_usd": 15000, "price": 3480.00, "status": "filled", "created_at": "2026-08-23T11:00:00Z", "filled_at": "2026-08-23T11:00:01Z"},
]

@router.get("/portfolio")
async def get_portfolio():
    return PORTFOLIO

@router.get("/positions")
async def get_positions():
    return {"positions": POSITIONS, "total_pnl": sum(p["unrealized_pnl"] for p in POSITIONS)}

@router.get("/orders")
async def get_orders():
    return {"orders": ORDERS}

@router.post("/orders")
async def create_order(order: dict):
    return {"status": "filled", "order_id": "ord-new", "message": "Paper order executed"}

@router.delete("/orders/{order_id}")
async def cancel_order(order_id: str):
    return {"status": "cancelled", "order_id": order_id}

@router.post("/reset")
async def reset_portfolio():
    return {"status": "reset", "message": "Portfolio reset to $100,000 initial capital"}
