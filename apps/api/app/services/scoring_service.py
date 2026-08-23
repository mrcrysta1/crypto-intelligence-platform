"""Scoring service - orchestrates scoring engines for assets."""

import structlog

logger = structlog.get_logger()

class ScoringService:
    """Orchestrates all scoring engines for an asset."""
    
    def __init__(self):
        self.weights = {
            "technical": 0.30,
            "fundamental": 0.25,
            "whale": 0.25,
            "derivative": 0.20,
        }

    async def compute_all_scores(self, asset_id: str) -> dict:
        """Compute scores for a single asset."""
        logger.info("Computing scores", asset_id=asset_id)
        # In demo mode, return pre-computed scores
        return {
            "technical_score": 78,
            "fundamental_score": 85,
            "whale_score": 72,
            "derivative_score": 65,
            "composite_score": 76,
            "direction": "LONG",
            "confidence": 0.78,
            "risk_level": "medium",
        }

    async def refresh_rankings(self) -> list:
        """Recompute rankings for all active assets."""
        logger.info("Refreshing rankings")
        return []

scoring_service = ScoringService()
