# Changelog

## [1.0.0] - 2026-05-31

### Added
- Initial release
- 25+ models from 8 providers (OpenAI, Anthropic, Google, DeepSeek, Mistral, xAI, Alibaba)
- CLI tool (`aicc`) with list, estimate, compare, daily, recommend, savings commands
- Python API with `estimate()`, `compare()`, `recommend()`, `savings_report()`
- Usage tracking with local JSON storage
- Task-based model recommendations
- Cache hit rate cost modeling
- JSON output mode for all commands
- Full test suite with pytest
- CI/CD with GitHub Actions (Python 3.9-3.13)
