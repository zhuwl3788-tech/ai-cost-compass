"""Compare costs across providers and recommend models."""

from __future__ import annotations

from typing import Optional

from ai_cost_compass.models import ModelPricing, Provider, TaskType
from ai_cost_compass.pricing import list_models
from ai_cost_compass.estimator import estimate


def compare(
    input_tokens: int = 1_000,
    output_tokens: int = 500,
    cached_tokens: int = 0,
    provider: Optional[Provider] = None,
    task: Optional[TaskType] = None,
    supports_vision: Optional[bool] = None,
    max_context: Optional[int] = None,
    sort_by: str = "cost",  # "cost" or "output_price"
) -> list[dict]:
    """Compare costs across all models matching the filters.

    Returns a sorted list of cost estimates.
    """
    models = list_models(provider)
    results = []

    for m in models:
        if supports_vision and not m.supports_vision:
            continue
        if max_context and m.context_window < max_context:
            continue
        # Skip embedding-only and image-only models for regular comparison
        if m.notes and ("Embedding" in m.notes or "image" in m.notes.lower()):
            continue

        est = estimate(
            m.model_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_tokens=cached_tokens,
        )
        results.append(est)

    reverse = sort_by != "cost"
    results.sort(key=lambda x: x["total_cost"], reverse=reverse)
    return results


def recommend(
    task: TaskType,
    budget_per_call: Optional[float] = None,
    min_context: int = 0,
    needs_vision: bool = False,
) -> list[dict]:
    """Recommend models for a task with optional constraints.

    Returns models sorted by cost (cheapest first) that meet the constraints.
    """
    defaults = {
        TaskType.CHAT: (500, 200),
        TaskType.CODE: (2_000, 1_500),
        TaskType.VISION: (1_000, 300),
        TaskType.TRANSLATION: (500, 600),
        TaskType.SUMMARIZATION: (3_000, 500),
        TaskType.CREATIVE: (300, 2_000),
        TaskType.ANALYSIS: (2_000, 1_000),
        TaskType.EMBEDDING: (500, 0),
        TaskType.IMAGE_GEN: (100, 0),
        TaskType.AUDIO: (1_000, 500),
    }
    in_tok, out_tok = defaults.get(task, (500, 200))

    all_models = list_models()
    candidates = []

    for m in all_models:
        if needs_vision and not m.supports_vision:
            continue
        if min_context and m.context_window < min_context:
            continue
        # Skip non-applicable models
        if task == TaskType.EMBEDDING and not m.embedding_price:
            continue
        if task != TaskType.EMBEDDING and m.embedding_price is not None:
            continue

        est = estimate(m.model_id, in_tok, out_tok)
        if budget_per_call is not None and est["total_cost"] > budget_per_call:
            continue
        candidates.append(est)

    candidates.sort(key=lambda x: x["total_cost"])
    return candidates


def savings_report(
    current_model: str,
    alternative_model: str,
    calls_per_day: int = 100,
    avg_input_tokens: int = 1_000,
    avg_output_tokens: int = 500,
) -> dict:
    """Calculate potential savings from switching models."""
    from ai_cost_compass.estimator import estimate_daily_cost

    current = estimate_daily_cost(current_model, calls_per_day,
                                   avg_input_tokens, avg_output_tokens)
    alternative = estimate_daily_cost(alternative_model, calls_per_day,
                                       avg_input_tokens, avg_output_tokens)

    daily_save = current["daily_cost"] - alternative["daily_cost"]
    monthly_save = current["monthly_cost"] - alternative["monthly_cost"]
    pct = (daily_save / current["daily_cost"] * 100) if current["daily_cost"] > 0 else 0

    return {
        "current": current_model,
        "alternative": alternative_model,
        "current_daily": current["daily_cost"],
        "alternative_daily": alternative["daily_cost"],
        "daily_savings": round(daily_save, 4),
        "monthly_savings": round(monthly_save, 2),
        "yearly_savings": round(monthly_save * 12, 2),
        "savings_pct": round(pct, 1),
    }
