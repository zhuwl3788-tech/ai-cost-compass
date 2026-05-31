# Contributing to AI Cost Compass

Thanks for your interest in contributing! Here's how to get started.

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/ai-cost-compass.git
cd ai-cost-compass
pip install -e ".[dev]"
pytest
```

## Ways to Contribute

### � Adding New Model Pricing

1. Edit `src/ai_cost_compass/pricing.py`
2. Add a new `ModelPricing` entry to the `_MODELS` list
3. Run `pytest` to verify nothing breaks
4. Submit a PR with a link to the official pricing page

### 🐛 Bug Fixes

1. Open an issue first (if one doesn't exist)
2. Write a failing test that reproduces the bug
3. Fix the bug
4. Ensure all tests pass

### ✨ New Features

1. Open an issue to discuss the feature
2. Write tests first (TDD)
3. Implement the feature
4. Update README if adding new CLI commands

## Code Style

- Follow existing code patterns
- Keep functions small and focused
- Add docstrings to public functions
- Use type hints

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_cost_compass

# Run specific test file
pytest tests/test_pricing.py
```

## Pull Request Process

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Commit with clear messages (`feat: add Grok 3 pricing`)
4. Push and open a PR
5. Ensure CI passes
6. Request review

## Pricing Data Guidelines

- Use official pricing pages as the source
- All prices in USD per 1 million tokens
- Include `released` date when known
- Add `notes` for special models (reasoning, embedding, etc.)
