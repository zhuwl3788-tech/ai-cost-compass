"""Tests for pricing module."""

import pytest
from ai_cost_compass.pricing import get_pricing, list_models, search_models
from ai_cost_compass.models import Provider


class TestGetPricing:
    def test_known_model(self):
        p = get_pricing("gpt-4o")
        assert p.provider == Provider.OPENAI
        assert p.input_price == 2.50
        assert p.output_price == 10.00

    def test_anthropic_model(self):
        p = get_pricing("claude-sonnet-4-6")
        assert p.provider == Provider.ANTHROPIC
        assert p.input_price == 3.00

    def test_unknown_model_raises(self):
        with pytest.raises(KeyError, match="Unknown model"):
            get_pricing("nonexistent-model")

    def test_all_models_have_positive_prices(self):
        for m in list_models():
            assert m.input_price >= 0, f"{m.model_id} has negative input price"
            assert m.output_price >= 0, f"{m.model_id} has negative output price"


class TestListModels:
    def test_all_models(self):
        models = list_models()
        assert len(models) > 20  # We have 25+ models

    def test_filter_by_provider(self):
        openai = list_models(Provider.OPENAI)
        assert all(m.provider == Provider.OPENAI for m in openai)
        assert len(openai) > 5

    def test_filter_anthropic(self):
        anthropic = list_models(Provider.ANTHROPIC)
        assert len(anthropic) >= 3


class TestSearchModels:
    def test_search_gpt(self):
        results = search_models("gpt")
        assert len(results) > 0
        assert all("gpt" in m.model_id.lower() for m in results)

    def test_search_claude(self):
        results = search_models("claude")
        assert len(results) >= 3

    def test_search_empty(self):
        results = search_models("zzz_nonexistent")
        assert len(results) == 0
