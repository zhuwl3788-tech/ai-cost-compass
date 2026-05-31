# 🧭 AI Cost Compass

**Compare, estimate, and optimize AI API costs across providers.**

[![PyPI version](https://img.shields.io/pypi/v/ai-cost-compass?style=flat-square)](https://pypi.org/project/ai-cost-compass/)
[![Python](https://img.shields.io/pypi/pyversions/ai-cost-compass?style=flat-square)](https://pypi.org/project/ai-cost-compass/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/ai-cost-compass/test.yml?style=flat-square&label=tests)]()

Stop guessing which AI model is cheapest for your use case. **AI Cost Compass** gives you real pricing data, cost estimation, side-by-side comparison, and savings analysis — all from the command line or Python.

## ✨ Features

- 📊 **25+ models** from OpenAI, Anthropic, Google, DeepSeek, Mistral, xAI, Alibaba
- 💰 **Instant cost estimation** for any model + token combination
- 🔄 **Side-by-side comparison** across all providers
- 📈 **Daily/monthly/yearly projections** with cache hit rate modeling
- 🎯 **Smart recommendations** based on task type, budget, and requirements
- 💡 **Savings calculator** — see exactly how much you save by switching models
- 🖥️ **CLI + Python API** — use in scripts, CI/CD, or interactively

## 🚀 Quick Start

```bash
pip install ai-cost-compass
```

### CLI Usage

```bash
# List all models with pricing
aicc list

# Search for specific models
aicc list -s claude

# Estimate cost for a request
aicc estimate gpt-4o -i 2000 -o 1000

# Compare all models for a specific workload
aicc compare -i 3000 -o 1500

# Get daily/monthly cost projections
aicc daily gpt-4o -n 500 --cache-rate 0.3

# Find the cheapest model for a task
aicc recommend code --budget 0.01

# Calculate savings from switching
aicc savings gpt-4o claude-haiku-4-5
```

### Python API

```python
from ai_cost_compass import estimate, compare, recommend

# Estimate cost
result = estimate("gpt-4o", input_tokens=2000, output_tokens=1000)
print(f"Cost: ${result['total_cost']:.4f}")

# Compare models
ranking = compare(input_tokens=2000, output_tokens=1000)
for r in ranking[:5]:
    print(f"{r['display_name']}: ${r['total_cost']:.4f}")

# Get recommendations
best = recommend("code", budget_per_call=0.01)
print(f"Best for coding: {best[0]['display_name']}")
```

## 📊 Example Output

```
$ aicc compare -i 3000 -o 1500

  Comparing 25 models (3,000 in / 1,500 out):

  #    Model                          Provider         Cost
  ──── ────────────────────────────── ──────────── ────────────
  1    DeepSeek V3                    deepseek     $0.002460
  2    Mistral Small                  mistral      $0.002100
  3    Gemini 2.0 Flash               google       $0.000900
  4    GPT-4.1 Nano                   openai       $0.000900
  5    Gemini 2.5 Flash               google       $0.001350
  6    Claude Haiku 4.5               anthropic    $0.008400
  ...
  22   Claude Opus 4.8                anthropic    $0.157500
```

## 🎯 Task-Based Recommendations

```bash
# "What's the cheapest model for code generation under $0.01/call?"
aicc recommend code --budget 0.01

# "I need vision support for image analysis"
aicc recommend vision --vision

# "Best model for creative writing"
aicc recommend creative
```

## 💡 Savings Calculator

```bash
$ aicc savings gpt-4o claude-haiku-4-5 -n 500

  Switching from gpt-4o to claude-haiku-4-5:
  ─────────────────────────────
  Current daily:     $3.1250
  New daily:         $1.4000
  Daily savings:     $1.7250 (55.2%)
  Monthly savings:   $51.75
  Yearly savings:    $621.00
```

## 📦 Supported Models

| Provider | Models |
|----------|--------|
| **OpenAI** | GPT-4.1, GPT-4.1 Mini/Nano, GPT-4o, o3, o4-mini, Embeddings |
| **Anthropic** | Claude Opus 4.8, Sonnet 4.6, Haiku 4.5 |
| **Google** | Gemini 2.5 Pro/Flash, Gemini 2.0 Flash |
| **DeepSeek** | DeepSeek V3, DeepSeek R1 |
| **Mistral** | Mistral Large, Mistral Small |
| **xAI** | Grok 3, Grok 3 Mini |
| **Alibaba** | Qwen 3.7 Max |

## 🔧 Development

```bash
git clone https://github.com/YOUR_USERNAME/ai-cost-compass.git
cd ai-cost-compass
pip install -e ".[dev]"
pytest
```

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Especially welcome:**
- Adding new model pricing data
- Improving cost estimation accuracy
- New CLI commands or features
- Bug reports and fixes

## 📄 License

MIT — see [LICENSE](LICENSE).
