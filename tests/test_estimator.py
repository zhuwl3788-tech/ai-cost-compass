"""Tests for estimator module."""

import pytest
from ai_cost_compass.estimator import estimate, estimate_batch, estimate_daily_cost


class TestEstimate:
    def test_basic_estimate(self):
        r = estimate("gpt-4o", input_tokens=1000, output_tokens=500)
        assert r["model"] == "gpt-4o"
        assert r["total_cost"] > 0
        assert r["input_tokens"] == 1000
        assert r["output_tokens"] == 500

    def test_zero_tokens(self):
        r = estimate("gpt-4o", input_tokens=0, output_tokens=0)
        assert r["total_cost"] == 0.0

    def test_cached_tokens_discount(self):
        full = estimate("gpt-4o", input_tokens=1000, output_tokens=500)
        cached = estimate("gpt-4o", input_tokens=1000, output_tokens=500,
                          cached_tokens=500)
        assert cached["total_cost"] < full["total_cost"]

    def test_default_tokens_from_task(self):
        r = estimate("gpt-4o", task="code")
        assert r["input_tokens"] > 0
        assert r["output_tokens"] > 0

    def test_cost_calculation_accuracy(self):
        r = estimate("gpt-4o", input_tokens=1_000_000, output_tokens=1_000_000)
        # gpt-4o: $2.50/M input, $10.00/M output = $12.50
        assert abs(r["total_cost"] - 12.50) < 0.01

    def test_cheaper_model(self):
        expensive = estimate("gpt-4o", input_tokens=1000, output_tokens=500)
        cheap = estimate("gpt-4o-mini", input_tokens=1000, output_tokens=500)
        assert cheap["total_cost"] < expensive["total_cost"]


class TestEstimateBatch:
    def test_batch_matches_sum(self):
        calls = [
            {"input_tokens": 1000, "output_tokens": 500},
            {"input_tokens": 2000, "output_tokens": 1000},
        ]
        batch = estimate_batch("gpt-4o", calls)
        individual_sum = sum(c["total_cost"] for c in batch["calls"])
        assert abs(batch["total_cost"] - individual_sum) < 0.0001

    def test_batch_totals(self):
        calls = [{"input_tokens": 1000, "output_tokens": 500}] * 10
        batch = estimate_batch("gpt-4o", calls)
        assert batch["call_count"] == 10
        assert batch["total_input_tokens"] == 10_000
        assert batch["total_output_tokens"] == 5_000


class TestEstimateDailyCost:
    def test_scaling(self):
        daily = estimate_daily_cost("gpt-4o", calls_per_day=100)
        monthly = estimate_daily_cost("gpt-4o", calls_per_day=100)
        assert abs(daily["monthly_cost"] - daily["daily_cost"] * 30) < 0.01

    def test_cache_reduces_cost(self):
        no_cache = estimate_daily_cost("gpt-4o", calls_per_day=100,
                                        cache_hit_rate=0.0)
        with_cache = estimate_daily_cost("gpt-4o", calls_per_day=100,
                                         cache_hit_rate=0.5)
        assert with_cache["monthly_cost"] < no_cache["monthly_cost"]
