import math

def format_price(n: float) -> str:
    if n >= 1000:
        return f"${n:,.2f}"
    if n >= 1:
        return f"${n:.2f}"
    if n >= 0.01:
        return f"${n:.4f}"
    return f"${n:.8f}"

def format_volume(n: float) -> str:
    if n >= 1e12:
        return f"${n/1e12:.1f}T"
    if n >= 1e9:
        return f"${n/1e9:.1f}B"
    if n >= 1e6:
        return f"${n/1e6:.1f}M"
    if n >= 1e3:
        return f"${n/1e3:.1f}K"
    return f"${n:.2f}"

def format_percent(n: float) -> str:
    sign = "+" if n >= 0 else ""
    return f"{sign}{n:.2f}%"

def calculate_change_pct(old: float, new: float) -> float:
    if old == 0:
        return 0
    return ((new - old) / old) * 100

def paginate_results(items: list, page: int = 1, per_page: int = 20):
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "items": items[start:end],
        "total": len(items),
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(len(items) / per_page),
    }
