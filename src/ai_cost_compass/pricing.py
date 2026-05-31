"""Pricing database for major AI providers.

Prices are in USD per 1 million tokens. Updated May 2026.
Source: official provider pricing pages.
"""

from __future__ import annotations

from typing import Optional

from ai_cost_compass.models import ModelPricing, Provider

# ---------------------------------------------------------------------------
# Pricing database — add new models here
# ---------------------------------------------------------------------------

_MODELS: list[ModelPricing] = [
    # ── OpenAI ──────────────────────────────────────────────────────────
    ModelPricing(
        provider=Provider.OPENAI, model_id="gpt-4.1",
        display_name="GPT-4.1",
        input_price=2.00, output_price=8.00,
        cached_input_price=0.50,
        context_window=1_047_576, max_output_tokens=32_768,
        supports_vision=True, supports_function_calling=True,
        released="2025-04",
    ),
    ModelPricing(
        provider=Provider.OPENAI, model_id="gpt-4.1-mini",
        display_name="GPT-4.1 Mini",
        input_price=0.40, output_price=1.60,
        cached_input_price=0.10,
        context_window=1_047_576, max_output_tokens=32_768,
        supports_vision=True, supports_function_calling=True,
        released="2025-04",
    ),
    ModelPricing(
        provider=Provider.OPENAI, model_id="gpt-4.1-nano",
        display_name="GPT-4.1 Nano",
        input_price=0.10, output_price=0.40,
        cached_input_price=0.025,
        context_window=1_047_576, max_output_tokens=32_768,
        supports_vision=True, supports_function_calling=True,
        released="2025-04",
    ),
    ModelPricing(
        provider=Provider.OPENAI, model_id="gpt-4o",
        display_name="GPT-4o",
        input_price=2.50, output_price=10.00,
        cached_input_price=1.25,
        context_window=128_000, max_output_tokens=16_384,
        supports_vision=True, supports_function_calling=True,
        released="2024-05",
    ),
    ModelPricing(
        provider=Provider.OPENAI, model_id="gpt-4o-mini",
        display_name="GPT-4o Mini",
        input_price=0.15, output_price=0.60,
        cached_input_price=0.075,
        context_window=128_000, max_output_tokens=16_384,
        supports_vision=True, supports_function_calling=True,
        released="2024-07",
    ),
    ModelPricing(
        provider=Provider.OPENAI, model_id="o3",
        display_name="o3",
        input_price=2.00, output_price=8.00,
        cached_input_price=0.50,
        context_window=200_000, max_output_tokens=100_000,
        supports_vision=True, supports_function_calling=True,
        released="2025-04",
        notes="Reasoning model",
    ),
    ModelPricing(
        provider=Provider.OPENAI, model_id="o4-mini",
        display_name="o4-mini",
        input_price=1.10, output_price=4.40,
        cached_input_price=0.275,
        context_window=200_000, max_output_tokens=100_000,
        supports_vision=True, supports_function_calling=True,
        released="2025-04",
        notes="Reasoning model",
    ),
    ModelPricing(
        provider=Provider.OPENAI, model_id="gpt-4o-audio-preview",
        display_name="GPT-4o Audio",
        input_price=2.50, output_price=10.00,
        context_window=128_000,
        supports_vision=True,
        released="2024-10",
        notes="Audio input/output",
    ),
    # Embeddings
    ModelPricing(
        provider=Provider.OPENAI, model_id="text-embedding-3-small",
        display_name="Embedding 3 Small",
        input_price=0.02, output_price=0.0,
        embedding_price=0.02,
        context_window=8_191,
        released="2024-01",
        notes="Embedding model",
    ),
    ModelPricing(
        provider=Provider.OPENAI, model_id="text-embedding-3-large",
        display_name="Embedding 3 Large",
        input_price=0.13, output_price=0.0,
        embedding_price=0.13,
        context_window=8_191,
        released="2024-01",
        notes="Embedding model",
    ),

    # ── Anthropic ───────────────────────────────────────────────────────
    ModelPricing(
        provider=Provider.ANTHROPIC, model_id="claude-opus-4-8",
        display_name="Claude Opus 4.8",
        input_price=15.00, output_price=75.00,
        cached_input_price=1.875,
        context_window=200_000, max_output_tokens=32_000,
        supports_vision=True, supports_function_calling=True,
        released="2026-05",
        notes="Top reasoning, coding, agents",
    ),
    ModelPricing(
        provider=Provider.ANTHROPIC, model_id="claude-sonnet-4-6",
        display_name="Claude Sonnet 4.6",
        input_price=3.00, output_price=15.00,
        cached_input_price=0.375,
        context_window=200_000, max_output_tokens=16_000,
        supports_vision=True, supports_function_calling=True,
        released="2025-06",
        notes="Best coding model",
    ),
    ModelPricing(
        provider=Provider.ANTHROPIC, model_id="claude-haiku-4-5",
        display_name="Claude Haiku 4.5",
        input_price=0.80, output_price=4.00,
        cached_input_price=0.08,
        context_window=200_000, max_output_tokens=8_192,
        supports_vision=True, supports_function_calling=True,
        released="2025-10",
        notes="Fast, cost-effective",
    ),

    # ── Google ──────────────────────────────────────────────────────────
    ModelPricing(
        provider=Provider.GOOGLE, model_id="gemini-2.5-pro",
        display_name="Gemini 2.5 Pro",
        input_price=1.25, output_price=10.00,
        cached_input_price=0.3125,
        context_window=1_048_576, max_output_tokens=65_536,
        supports_vision=True, supports_function_calling=True,
        released="2025-03",
    ),
    ModelPricing(
        provider=Provider.GOOGLE, model_id="gemini-2.5-flash",
        display_name="Gemini 2.5 Flash",
        input_price=0.15, output_price=0.60,
        cached_input_price=0.0375,
        context_window=1_048_576, max_output_tokens=65_536,
        supports_vision=True, supports_function_calling=True,
        released="2025-03",
    ),
    ModelPricing(
        provider=Provider.GOOGLE, model_id="gemini-2.0-flash",
        display_name="Gemini 2.0 Flash",
        input_price=0.10, output_price=0.40,
        cached_input_price=0.025,
        context_window=1_048_576, max_output_tokens=8_192,
        supports_vision=True, supports_function_calling=True,
        released="2025-02",
    ),

    # ── DeepSeek ────────────────────────────────────────────────────────
    ModelPricing(
        provider=Provider.DEEPSEEK, model_id="deepseek-v3",
        display_name="DeepSeek V3",
        input_price=0.27, output_price=1.10,
        cached_input_price=0.07,
        context_window=128_000, max_output_tokens=8_192,
        supports_function_calling=True,
        released="2024-12",
        notes="Cost-effective Chinese LLM",
    ),
    ModelPricing(
        provider=Provider.DEEPSEEK, model_id="deepseek-r1",
        display_name="DeepSeek R1",
        input_price=0.55, output_price=2.19,
        cached_input_price=0.14,
        context_window=128_000, max_output_tokens=8_192,
        released="2025-01",
        notes="Reasoning model",
    ),

    # ── Mistral ─────────────────────────────────────────────────────────
    ModelPricing(
        provider=Provider.MISTRAL, model_id="mistral-large-latest",
        display_name="Mistral Large",
        input_price=2.00, output_price=6.00,
        context_window=128_000, max_output_tokens=8_192,
        supports_function_calling=True,
        released="2024-11",
    ),
    ModelPricing(
        provider=Provider.MISTRAL, model_id="mistral-small-latest",
        display_name="Mistral Small",
        input_price=0.10, output_price=0.30,
        context_window=128_000, max_output_tokens=8_192,
        supports_function_calling=True,
        released="2025-01",
    ),

    # ── xAI ─────────────────────────────────────────────────────────────
    ModelPricing(
        provider=Provider.XAI, model_id="grok-3",
        display_name="Grok 3",
        input_price=3.00, output_price=15.00,
        cached_input_price=0.75,
        context_window=131_072, max_output_tokens=16_384,
        supports_vision=True, supports_function_calling=True,
        released="2025-02",
    ),
    ModelPricing(
        provider=Provider.XAI, model_id="grok-3-mini",
        display_name="Grok 3 Mini",
        input_price=0.30, output_price=0.50,
        cached_input_price=0.075,
        context_window=131_072, max_output_tokens=16_384,
        supports_function_calling=True,
        released="2025-02",
        notes="Reasoning model",
    ),

    # ── Alibaba (Qwen) ──────────────────────────────────────────────────
    ModelPricing(
        provider=Provider.ALIBABA, model_id="qwen3.7-max",
        display_name="Qwen 3.7 Max",
        input_price=1.60, output_price=6.40,
        context_window=131_072, max_output_tokens=16_384,
        supports_vision=True, supports_function_calling=True,
        released="2026-05",
        notes="Global #2 coding model",
    ),
]

# Build fast lookup dict
_MODEL_MAP: dict[str, ModelPricing] = {m.model_id: m for m in _MODELS}


def get_pricing(model_id: str) -> ModelPricing:
    """Get pricing for a model by ID. Raises KeyError if not found."""
    if model_id not in _MODEL_MAP:
        available = ", ".join(sorted(_MODEL_MAP.keys()))
        raise KeyError(
            f"Unknown model '{model_id}'. Available: {available}"
        )
    return _MODEL_MAP[model_id]


def list_models(provider: Optional[Provider] = None) -> list[ModelPricing]:
    """List all models, optionally filtered by provider."""
    if provider is None:
        return list(_MODELS)
    return [m for m in _MODELS if m.provider == provider]


def get_provider_models(provider: Provider) -> list[str]:
    """Get model IDs for a provider."""
    return [m.model_id for m in _MODELS if m.provider == provider]


def search_models(query: str) -> list[ModelPricing]:
    """Search models by name or ID (case-insensitive substring match)."""
    q = query.lower()
    return [
        m for m in _MODELS
        if q in m.model_id.lower() or q in m.display_name.lower()
    ]
