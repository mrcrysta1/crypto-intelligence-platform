import uuid

ASSET_LIST = [
    {"symbol": "BTC", "name": "Bitcoin", "slug": "bitcoin"},
    {"symbol": "ETH", "name": "Ethereum", "slug": "ethereum"},
    {"symbol": "BNB", "name": "BNB", "slug": "bnb"},
    {"symbol": "SOL", "name": "Solana", "slug": "solana"},
    {"symbol": "XRP", "name": "XRP", "slug": "xrp"},
    {"symbol": "ADA", "name": "Cardano", "slug": "cardano"},
    {"symbol": "DOGE", "name": "Dogecoin", "slug": "dogecoin"},
    {"symbol": "DOT", "name": "Polkadot", "slug": "polkadot"},
    {"symbol": "AVAX", "name": "Avalanche", "slug": "avalanche"},
    {"symbol": "LINK", "name": "Chainlink", "slug": "chainlink"},
    {"symbol": "MATIC", "name": "Polygon", "slug": "matic-network"},
    {"symbol": "UNI", "name": "Uniswap", "slug": "uniswap"},
    {"symbol": "SHIB", "name": "Shiba Inu", "slug": "shiba-inu"},
    {"symbol": "LTC", "name": "Litecoin", "slug": "litecoin"},
    {"symbol": "BCH", "name": "Bitcoin Cash", "slug": "bitcoin-cash"},
    {"symbol": "ATOM", "name": "Cosmos", "slug": "cosmos"},
    {"symbol": "NEAR", "name": "NEAR Protocol", "slug": "near"},
    {"symbol": "FIL", "name": "Filecoin", "slug": "filecoin"},
    {"symbol": "APT", "name": "Aptos", "slug": "aptos"},
    {"symbol": "ARB", "name": "Arbitrum", "slug": "arbitrum"},
]

SCORE_WEIGHTS = {
    "technical": 0.30,
    "fundamental": 0.25,
    "whale": 0.25,
    "derivative": 0.20,
}

DIRECTION_OPTIONS = ["LONG", "SHORT", "WATCH", "NO_TRADE"]
RISK_LEVELS = ["low", "medium", "high", "extreme"]
INTERVAL_OPTIONS = ["1m", "5m", "15m", "1h", "4h", "1d"]

def gen_id():
    return str(uuid.uuid4())
