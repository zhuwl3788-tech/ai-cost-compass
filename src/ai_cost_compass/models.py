"""Data models for AI Cost Compass."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Provider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    META = "meta"
    MISTRAL = "mistral"
    XAI = "xai"
    DEEPSEEK = "deepseek"
    ALIBABA = "alibaba"


class TaskType(str, Enum):
    """Broad task categories for cost comparison."""
    CHAT = "chat"
    CODE = "code"
    VISION = "vision"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"
    CREATIVE = "creative"
    ANALYSIS = "analysis"
    EMBEDDING = "embedding"
    IMAGE_GEN = "image_gen"
    AUDIO = "audio"


@dataclass(frozen=True)
class ModelPricing:
    """Pricing information for a single model.

    All prices are in USD per 1 million tokens unless noted otherwise.
    """
    provider: Provider
    model_id: str
    display_name: str
    input_price: float          # USD per 1M input tokens
    output_price: float         # USD per 1M output tokens
    cached_input_price: Optional[float] = None   # discounted cached input
    context_window: int = 128_000
    max_output_tokens: int = 4_096
    supports_vision: bool = False
    supports_function_calling: bool = False
    supports_streaming: bool = True
    # For embedding models
    embedding_price: Optional[float] = None  # USD per 1M tokens
    # For image generation models
    image_price_per_1024: Optional[float] = None  # USD per 1024x1024 image
    # Metadata
    released: Optional[str] = None  # YYYY-MM or YYYY-MM-DD
    notes: str = ""

    @property
    def cost_per_1k_input(self) -> float:
        return self.input_price / 1_000

    @property
    def cost_per_1k_output(self) -> float:
        return self.output_price / 1_000

    def calc_cost(self, input_tokens: int, output_tokens: int,
                  cached_tokens: int = 0) -> float:
        """Calculate total cost in USD for a request."""
        regular_input = max(0, input_tokens - cached_tokens)
        regular_cost = (regular_input / 1_000_000) * self.input_price
        cached_cost = 0.0
        if cached_tokens > 0 and self.cached_input_price is not None:
            cached_cost = (cached_tokens / 1_000_000) * self.cached_input_price
        elif cached_tokens > 0:
            # Fallback: no cache discount available, charge full price
            cached_cost = (cached_tokens / 1_000_000) * self.input_price
        output_cost = (output_tokens / 1_000_000) * self.output_price
        return round(regular_cost + cached_cost + output_cost, 6)


@dataclass
class UsageRecord:
    """A single API usage record for tracking."""
    timestamp: str              # ISO 8601
    provider: Provider
    model_id: str
    input_tokens: int
    output_tokens: int
    cached_tokens: int = 0
    cost_usd: float = 0.0
    task_type: Optional[TaskType] = None
    metadata: dict = field(default_factory=dict)
