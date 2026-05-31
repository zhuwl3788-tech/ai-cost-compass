"""Cost estimation for AI API usage."""

from __future__ import annotations

from typing import Optional

from ai_cost_compass.models import ModelPricing, Provider, TaskType
from ai_cost_compass.pricing import get_pricing, list_models


# Typical token ranges for common tasks (input, output)
_TASK_DEFAULTS: dict[TaskType, tuple[int, int]] = {
    TaskType.CHAT:           (500, 200),
    TaskType.CODE:           (2_000, 1_500),
    TaskType.VISION:         (1_000, 300),
    TaskType.TRANSLATION:    (500, 600),
    TaskType.SUMMARIZATION:  (3_000, 500),
    TaskType.CREATIVE:       (300, 2_000),
    TaskType.ANALYSIS:       (2_000, 1_000),
    TaskType.EMBEDDING:      (500, 0),
    TaskType.IMAGE_GEN:      (100, 0),
    TaskType.AUDIO:          (1_000, 500),
}


def estimate(
    model_id: str,
    input_tokens: Optional[int] = None,
    output_tokens: Optional[int] = None,
    cached_tokens: int = 0,
    task: Optional[TaskType] = None,
) -> dict:
    """Estimate cost for a single API call.

    If input_tokens/output_tokens are not given, uses task-type defaults.

    Returns dict with model, input_cost, output_cost, cached_cost, total_cost.
    """
    pricing = get_pricing(model_id)

    if input_tokens is None or output_tokens is None:
        default_in, default_out = _TASK_DEFAULTS.get(
            task or TaskType.CHAT, (500, 200)
        )
        input_tokens = input_tokens or default_in
        output_tokens = output_tokens or default_out

    regular_input = max(0, input_tokens - cached_tokens)
    regular_cost = (regular_input / 1_000_000) * pricing.input_price
    cached_cost = 0.0
    if cached_tokens > 0:
        rate = pricing.cached_input_price if pricing.cached_input_price is not None else pricing.input_price
        cached_cost = (cached_tokens / 1_000_000) * rate
    output_cost = (output_tokens / 1_000_000) * pricing.output_price
    total = round(regular_cost + cached_cost + output_cost, 6)

    return {
        "model": model_id,
        "provider": pricing.provider.value,
        "display_name": pricing.display_name,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cached_tokens": cached_tokens,
        "input_cost": round(regular_cost, 6),
        "cached_cost": round(cached_cost, 6),
        "output_cost": round(output_cost, 6),
        "total_cost": total,
    }


def estimate_batch(
    model_id: str,
    calls: list[dict],
) -> dict:
    """Estimate cost for multiple calls.

    Each call dict should have: input_tokens, output_tokens, and
    optionally cached_tokens.

    Returns dict with per-call costs and totals.
    """
    results = []
    total_cost = 0.0
    total_input = 0
    total_output = 0

    for i, call in enumerate(calls):
        r = estimate(
            model_id,
            input_tokens=call.get("input_tokens", 0),
            output_tokens=call.get("output_tokens", 0),
            cached_tokens=call.get("cached_tokens", 0),
        )
        results.append(r)
        total_cost += r["total_cost"]
        total_input += r["input_tokens"]
        total_output += r["output_tokens"]

    return {
        "model": model_id,
        "call_count": len(calls),
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_cost": round(total_cost, 6),
        "calls": results,
    }


def estimate_daily_cost(
    model_id: str,
    calls_per_day: int = 100,
    avg_input_tokens: int = 1_000,
    avg_output_tokens: int = 500,
    cache_hit_rate: float = 0.0,
) -> dict:
    """Estimate daily/monthly cost for sustained usage."""
    cached_per_call = int(avg_input_tokens * cache_hit_rate)
    calls = [
        {
            "input_tokens": avg_input_tokens,
            "output_tokens": avg_output_tokens,
            "cached_tokens": cached_per_call,
        }
        for _ in range(calls_per_day)
    ]
    batch = estimate_batch(model_id, calls)
    daily = batch["total_cost"]
    monthly = daily * 30

    return {
        "model": model_id,
        "calls_per_day": calls_per_day,
        "daily_cost": round(daily, 4),
        "monthly_cost": round(monthly, 2),
        "yearly_cost": round(monthly * 12, 2),
        "cache_hit_rate": cache_hit_rate,
    }
