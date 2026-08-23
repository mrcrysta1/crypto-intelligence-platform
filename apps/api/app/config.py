from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./crypto_intel.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    DEMO_MODE: bool = True
    API_KEYS_ALLOWLIST: str = ""
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    COINGECKO_API_KEY: Optional[str] = None
    BINANCE_API_KEY: Optional[str] = None
    NEWS_API_KEY: Optional[str] = None
    ETHERSCAN_API_KEY: Optional[str] = None
    WALLETCONNECT_API_KEY: Optional[str] = None
    SANDBOX_API_KEY: Optional[str] = None

    GEMINI_API_KEY: Optional[str] = None
    GEMINI_BASE_URL: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
