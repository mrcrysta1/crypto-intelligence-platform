from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "healthy", "version": "1.0.0", "mode": "demo"}

@router.get("/ready")
async def readiness():
    return {"status": "ready"}

@router.get("/live")
async def liveness():
    return {"status": "alive"}
