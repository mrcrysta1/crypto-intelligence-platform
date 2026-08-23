from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog
import time

from app.config import settings
from app.routers import health, assets, market, signals, rankings, predictions, paper_trading, alerts, ai, backtests

logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Crypto Intelligence Platform", demo_mode=settings.DEMO_MODE)
    yield
    logger.info("Shutting down Crypto Intelligence Platform")

app = FastAPI(
    title="Crypto Intelligence Platform",
    description="Multi-dimensional crypto analysis with technical, fundamental, whale, and derivative signals",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(assets.router)
app.include_router(market.router)
app.include_router(signals.router)
app.include_router(rankings.router)
app.include_router(predictions.router)
app.include_router(paper_trading.router)
app.include_router(alerts.router)
app.include_router(ai.router)
app.include_router(backtests.router)

@app.get("/")
async def root():
    return {"name": "Crypto Intelligence Platform", "version": "1.0.0", "docs": "/docs", "mode": "demo"}
