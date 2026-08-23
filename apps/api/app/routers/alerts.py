from fastapi import APIRouter

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

ALERTS = [
    {"id": "alert-1", "symbol": "BTC", "alert_type": "price", "condition": {"operator": "above", "value": 70000}, "is_active": True, "message": "BTC above $70,000", "last_triggered": None, "created_at": "2026-08-22T00:00:00Z"},
    {"id": "alert-2", "symbol": "ETH", "alert_type": "signal", "condition": {"direction": "LONG", "min_confidence": 0.8}, "is_active": True, "message": "ETH long signal with high confidence", "last_triggered": "2026-08-23T14:00:00Z", "created_at": "2026-08-21T00:00:00Z"},
    {"id": "alert-3", "symbol": "SOL", "alert_type": "whale", "condition": {"min_amount_usd": 5000000}, "is_active": True, "message": "Large SOL transfer detected", "last_triggered": "2026-08-24T00:18:00Z", "created_at": "2026-08-20T00:00:00Z"},
    {"id": "alert-4", "symbol": "BTC", "alert_type": "score", "condition": {"min_composite": 85}, "is_active": False, "message": "BTC composite score above 85", "last_triggered": "2026-08-23T08:00:00Z", "created_at": "2026-08-19T00:00:00Z"},
]

TRIGGERS = [
    {"alert_id": "alert-3", "triggered_at": "2026-08-24T00:18:00Z", "data": {"type": "exchange_outflow", "amount": 8500000, "asset": "SOL"}},
    {"alert_id": "alert-2", "triggered_at": "2026-08-23T14:00:00Z", "data": {"direction": "LONG", "confidence": 0.85}},
    {"alert_id": "alert-4", "triggered_at": "2026-08-23T08:00:00Z", "data": {"composite_score": 87}},
]

@router.get("/")
async def list_alerts():
    return {"alerts": ALERTS}

@router.post("/")
async def create_alert(alert: dict):
    return {"status": "created", "alert_id": "alert-new", "alert": alert}

@router.put("/{alert_id}")
async def update_alert(alert_id: str, alert: dict):
    return {"status": "updated", "alert_id": alert_id}

@router.delete("/{alert_id}")
async def delete_alert(alert_id: str):
    return {"status": "deleted", "alert_id": alert_id}

@router.get("/triggers")
async def get_triggers():
    return {"triggers": TRIGGERS}
