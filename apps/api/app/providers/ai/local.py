"""Local AI provider - mock analysis for demo mode."""

from app.providers.base import AIProvider

class LocalAIProvider(AIProvider):
    async def analyze(self, context: str) -> str:
        return (
            "MODEL_OUTPUT: Analysis based on technical, fundamental, whale, and derivative dimensions. "
            "Composite score derived from weighted multi-dimensional assessment.\n\n"
            "AI_INTERPRETATION: The asset shows mixed signals across dimensions. "
            "Technical indicators suggest consolidation while on-chain metrics show accumulation. "
            "Recommend monitoring for directional confirmation before taking position. "
            "Risk management: use stop-loss at 3% and take-profit at 6%."
        )
