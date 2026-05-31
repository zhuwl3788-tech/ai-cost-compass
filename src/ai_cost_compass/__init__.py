"""
AI Cost Compass — Compare, estimate, and optimize AI API costs.

>>> from ai_cost_compass import estimate, compare
>>> estimate("gpt-4o", input_tokens=1000, output_tokens=500)
{'model': 'gpt-4o', 'input_cost': 0.0025, 'output_cost': 0.005, 'total_cost': 0.0075}
>>> compare(task="chat", input_tokens=1000, output_tokens=500)
[{'model': 'claude-sonnet-4-6', ...}, ...]
"""

from ai_cost_compass.models import ModelPricing, Provider, TaskType
from ai_cost_compass.pricing import get_pricing, list_models, get_provider_models
from ai_cost_compass.estimator import estimate, estimate_batch
from ai_cost_compass.comparator import compare, recommend

__version__ = "1.0.0"
__all__ = [
    "ModelPricing", "Provider", "TaskType",
    "get_pricing", "list_models", "get_provider_models",
    "estimate", "estimate_batch",
    "compare", "recommend",
]
