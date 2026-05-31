"""Usage tracking with local JSON storage."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from ai_cost_compass.models import Provider, TaskType, UsageRecord
from ai_cost_compass.pricing import get_pricing


_DEFAULT_DB = Path.home() / ".ai-cost-compass" / "usage.json"


def _ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def _load_db(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_db(path: Path, records: list[dict]) -> None:
    _ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def log_usage(
    model_id: str,
    input_tokens: int,
    output_tokens: int,
    cached_tokens: int = 0,
    task_type: Optional[TaskType] = None,
    metadata: Optional[dict] = None,
    db_path: Optional[Path] = None,
) -> dict:
    """Log a single API usage and return the record with cost."""
    pricing = get_pricing(model_id)
    cost = pricing.calc_cost(input_tokens, output_tokens, cached_tokens)

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "provider": pricing.provider.value,
        "model_id": model_id,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cached_tokens": cached_tokens,
        "cost_usd": cost,
        "task_type": task_type.value if task_type else None,
        "metadata": metadata or {},
    }

    path = db_path or _DEFAULT_DB
    records = _load_db(path)
    records.append(record)
    _save_db(path, records)
    return record


def get_usage(
    days: int = 30,
    provider: Optional[Provider] = None,
    model_id: Optional[str] = None,
    db_path: Optional[Path] = None,
) -> list[dict]:
    """Get usage records, optionally filtered."""
    path = db_path or _DEFAULT_DB
    records = _load_db(path)

    if days:
        cutoff = datetime.now(timezone.utc).isoformat()
        # Simple filter: keep last N days worth
        records = records[-(days * 500):]  # rough upper bound

    if provider:
        records = [r for r in records if r.get("provider") == provider.value]
    if model_id:
        records = [r for r in records if r.get("model_id") == model_id]

    return records


def get_summary(
    days: int = 30,
    db_path: Optional[Path] = None,
) -> dict:
    """Get a usage summary with costs broken down by provider/model."""
    records = get_usage(days=days, db_path=db_path)

    total_cost = sum(r.get("cost_usd", 0) for r in records)
    total_input = sum(r.get("input_tokens", 0) for r in records)
    total_output = sum(r.get("output_tokens", 0) for r in records)
    total_calls = len(records)

    by_model: dict[str, dict] = {}
    for r in records:
        mid = r.get("model_id", "unknown")
        if mid not in by_model:
            by_model[mid] = {
                "calls": 0, "cost": 0.0,
                "input_tokens": 0, "output_tokens": 0,
            }
        by_model[mid]["calls"] += 1
        by_model[mid]["cost"] += r.get("cost_usd", 0)
        by_model[mid]["input_tokens"] += r.get("input_tokens", 0)
        by_model[mid]["output_tokens"] += r.get("output_tokens", 0)

    # Round costs
    for v in by_model.values():
        v["cost"] = round(v["cost"], 6)

    return {
        "period_days": days,
        "total_calls": total_calls,
        "total_cost": round(total_cost, 6),
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "by_model": dict(sorted(by_model.items(),
                                 key=lambda x: x[1]["cost"], reverse=True)),
    }
