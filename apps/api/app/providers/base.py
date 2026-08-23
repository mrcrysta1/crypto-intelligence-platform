from abc import ABC, abstractmethod
from typing import Optional

class MarketDataProvider(ABC):
    @abstractmethod
    async def get_price(self, symbol: str) -> dict: ...

    @abstractmethod
    async def get_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 100) -> list: ...

    @abstractmethod
    async def get_market_data(self, symbol: str) -> dict: ...

    @abstractmethod
    async def get_derivatives(self, symbol: str) -> dict: ...

class NewsProvider(ABC):
    @abstractmethod
    async def get_news(self, query: str = "", limit: int = 20) -> list: ...

class SocialProvider(ABC):
    @abstractmethod
    async def get_sentiment(self, symbol: str) -> dict: ...

    @abstractmethod
    async def get_social_posts(self, symbol: str, limit: int = 20) -> list: ...

class BlockchainProvider(ABC):
    @abstractmethod
    async def get_whale_events(self, symbol: str) -> list: ...

    @abstractmethod
    async def get_exchange_flows(self, symbol: str) -> list: ...

    @abstractmethod
    async def get_top_holders(self, symbol: str) -> list: ...

class AIProvider(ABC):
    @abstractmethod
    async def analyze(self, context: str) -> str: ...
