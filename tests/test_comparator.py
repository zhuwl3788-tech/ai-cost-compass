"""Tests for comparator module."""

from ai_cost_compass.comparator import compare, recommend, savings_report
from ai_cost_compass.models import Provider, TaskType


class TestCompare:
    def test_returns_sorted(self):
        results = compare(input_tokens=1000, output_tokens=500)
        costs = [r["total_cost"] for r in results]
        assert costs == sorted(costs)

    def test_filter_provider(self):
        results = compare(input_tokens=1000, output_tokens=500,
                          provider=Provider.OPENAI)
        assert all(r["provider"] == "openai" for r in results)

    def test_vision_filter(self):
        results = compare(input_tokens=1000, output_tokens=500,
                          supports_vision=True)
        # All returned models should support vision
        assert len(results) > 0

    def test_empty_with_impossible_filter(self):
        results = compare(input_tokens=1000, output_tokens=500,
                          max_context=999_999_999)
        assert len(results) == 0


class TestRecommend:
    def test_chat_recommendations(self):
        results = recommend(TaskType.CHAT)
        assert len(results) > 0
        assert results[0]["total_cost"] <= results[-1]["total_cost"]

    def test_budget_filter(self):
        results = recommend(TaskType.CHAT, budget_per_call=0.001)
        for r in results:
            assert r["total_cost"] <= 0.001

    def test_vision_requirement(self):
        results = recommend(TaskType.VISION, needs_vision=True)
        assert len(results) > 0


class TestSavingsReport:
    def test_savings_positive(self):
        report = savings_report("gpt-4o", "gpt-4o-mini")
        assert report["monthly_savings"] > 0
        assert report["savings_pct"] > 0

    def test_savings_structure(self):
        report = savings_report("claude-opus-4-8", "claude-haiku-4-5")
        assert "daily_savings" in report
        assert "monthly_savings" in report
        assert "yearly_savings" in report
        assert report["yearly_savings"] == round(report["monthly_savings"] * 12, 2)
