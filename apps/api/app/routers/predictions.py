from fastapi import APIRouter

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

PREDICTIONS = [
    {"symbol": "BTC", "p_long": 0.72, "p_short": 0.12, "p_neutral": 0.16, "model_version": "v1.0.0", "confidence": 0.87},
    {"symbol": "ETH", "p_long": 0.68, "p_short": 0.14, "p_neutral": 0.18, "model_version": "v1.0.0", "confidence": 0.82},
    {"symbol": "SOL", "p_long": 0.74, "p_short": 0.10, "p_neutral": 0.16, "model_version": "v1.0.0", "confidence": 0.85},
    {"symbol": "ADA", "p_long": 0.22, "p_short": 0.55, "p_neutral": 0.23, "model_version": "v1.0.0", "confidence": 0.65},
    {"symbol": "DOGE", "p_long": 0.45, "p_short": 0.20, "p_neutral": 0.35, "model_version": "v1.0.0", "confidence": 0.48},
    {"symbol": "BNB", "p_long": 0.38, "p_short": 0.22, "p_neutral": 0.40, "model_version": "v1.0.0", "confidence": 0.61},
    {"symbol": "XRP", "p_long": 0.30, "p_short": 0.32, "p_neutral": 0.38, "model_version": "v1.0.0", "confidence": 0.52},
    {"symbol": "AVAX", "p_long": 0.60, "p_short": 0.18, "p_neutral": 0.22, "model_version": "v1.0.0", "confidence": 0.72},
    {"symbol": "LINK", "p_long": 0.58, "p_short": 0.16, "p_neutral": 0.26, "model_version": "v1.0.0", "confidence": 0.68},
    {"symbol": "NEAR", "p_long": 0.55, "p_short": 0.20, "p_neutral": 0.25, "model_version": "v1.0.0", "confidence": 0.70},
    {"symbol": "MATIC", "p_long": 0.18, "p_short": 0.52, "p_neutral": 0.30, "model_version": "v1.0.0", "confidence": 0.62},
    {"symbol": "SHIB", "p_long": 0.42, "p_short": 0.25, "p_neutral": 0.33, "model_version": "v1.0.0", "confidence": 0.48},
]

@router.get("/")
async def get_predictions():
    return {"predictions": PREDICTIONS, "model_version": "v1.0.0", "total": len(PREDICTIONS)}

@router.get("/{symbol}")
async def get_prediction(symbol: str):
    pred = next((p for p in PREDICTIONS if p["symbol"] == symbol.upper()), None)
    if not pred:
        return {"error": f"Prediction for {symbol} not found"}
    return pred

@router.get("/model/info")
async def model_info():
    return {
        "version": "v1.0.0",
        "algorithm": "ensemble RandomForest + XGBoost + LightGBM",
        "accuracy": 0.73,
        "precision": 0.71,
        "recall": 0.68,
        "f1_score": 0.69,
        "training_samples": 50000,
        "feature_count": 42,
        "trained_at": "2026-08-20T00:00:00Z",
        "next_retrain": "2026-08-27T00:00:00Z",
    }

@router.post("/train")
async def train_model():
    return {"status": "queued", "message": "Model training initiated (demo mode)"}
