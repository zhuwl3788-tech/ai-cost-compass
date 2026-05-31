"""CLI interface for AI Cost Compass."""

from __future__ import annotations

import argparse
import json
import sys

from ai_cost_compass import __version__
from ai_cost_compass.models import Provider, TaskType
from ai_cost_compass.pricing import list_models, get_pricing, search_models
from ai_cost_compass.estimator import estimate, estimate_daily_cost
from ai_cost_compass.comparator import compare, recommend, savings_report


def _fmt_usd(val: float) -> str:
    if val < 0.01:
        return f"${val:.6f}"
    if val < 1.0:
        return f"${val:.4f}"
    return f"${val:,.2f}"


def cmd_list(args: argparse.Namespace) -> None:
    provider = Provider(args.provider) if args.provider else None
    models = list_models(provider)
    if args.search:
        models = search_models(args.search)

    if args.json:
        print(json.dumps([{
            "model_id": m.model_id, "provider": m.provider.value,
            "display_name": m.display_name,
            "input_price": m.input_price, "output_price": m.output_price,
            "context_window": m.context_window,
        } for m in models], indent=2))
        return

    print(f"{'Model':<30} {'Provider':<12} {'Input $/1M':>12} {'Output $/1M':>12} {'Context':>10}")
    print("-" * 80)
    for m in models:
        print(f"{m.display_name:<30} {m.provider.value:<12} "
              f"{m.input_price:>12.2f} {m.output_price:>12.2f} "
              f"{m.context_window:>10,}")


def cmd_estimate(args: argparse.Namespace) -> None:
    result = estimate(
        args.model,
        input_tokens=args.input_tokens,
        output_tokens=args.output_tokens,
        cached_tokens=args.cached,
    )
    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"\n  Model: {result['display_name']} ({result['provider']})")
    print(f"  Input:  {result['input_tokens']:,} tokens → {_fmt_usd(result['input_cost'])}")
    if result['cached_tokens']:
        print(f"  Cached: {result['cached_tokens']:,} tokens → {_fmt_usd(result['cached_cost'])}")
    print(f"  Output: {result['output_tokens']:,} tokens → {_fmt_usd(result['output_cost'])}")
    print(f"  ─────────────────────────────")
    print(f"  Total:  {_fmt_usd(result['total_cost'])}")


def cmd_compare(args: argparse.Namespace) -> None:
    provider = Provider(args.provider) if args.provider else None
    results = compare(
        input_tokens=args.input_tokens,
        output_tokens=args.output_tokens,
        cached_tokens=args.cached,
        provider=provider,
    )
    if args.json:
        print(json.dumps(results, indent=2))
        return

    print(f"\n  Comparing {len(results)} models "
          f"({args.input_tokens:,} in / {args.output_tokens:,} out):\n")
    print(f"  {'#':<4} {'Model':<30} {'Provider':<12} {'Cost':>12}")
    print(f"  {'─'*4} {'─'*30} {'─'*12} {'─'*12}")
    for i, r in enumerate(results, 1):
        print(f"  {i:<4} {r['display_name']:<30} {r['provider']:<12} "
              f"{_fmt_usd(r['total_cost']):>12}")


def cmd_daily(args: argparse.Namespace) -> None:
    result = estimate_daily_cost(
        args.model,
        calls_per_day=args.calls,
        avg_input_tokens=args.input_tokens,
        avg_output_tokens=args.output_tokens,
        cache_hit_rate=args.cache_rate,
    )
    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"\n  Model: {result['model']}")
    print(f"  Calls/day: {result['calls_per_day']:,}")
    print(f"  Cache hit rate: {result['cache_hit_rate']:.0%}")
    print(f"  ─────────────────────────────")
    print(f"  Daily:   {_fmt_usd(result['daily_cost'])}")
    print(f"  Monthly: {_fmt_usd(result['monthly_cost'])}")
    print(f"  Yearly:  {_fmt_usd(result['yearly_cost'])}")


def cmd_recommend(args: argparse.Namespace) -> None:
    task = TaskType(args.task)
    results = recommend(
        task=task,
        budget_per_call=args.budget,
        needs_vision=args.vision,
    )
    if args.json:
        print(json.dumps(results, indent=2))
        return

    print(f"\n  Recommended models for '{args.task}' task:\n")
    print(f"  {'#':<4} {'Model':<30} {'Provider':<12} {'Cost/call':>12}")
    print(f"  {'─'*4} {'─'*30} {'─'*12} {'─'*12}")
    for i, r in enumerate(results[:10], 1):
        print(f"  {i:<4} {r['display_name']:<30} {r['provider']:<12} "
              f"{_fmt_usd(r['total_cost']):>12}")


def cmd_savings(args: argparse.Namespace) -> None:
    result = savings_report(
        args.current, args.alternative,
        calls_per_day=args.calls,
        avg_input_tokens=args.input_tokens,
        avg_output_tokens=args.output_tokens,
    )
    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"\n  Switching from {result['current']} to {result['alternative']}:")
    print(f"  ─────────────────────────────")
    print(f"  Current daily:     {_fmt_usd(result['current_daily'])}")
    print(f"  New daily:         {_fmt_usd(result['alternative_daily'])}")
    print(f"  Daily savings:     {_fmt_usd(result['daily_savings'])} ({result['savings_pct']}%)")
    print(f"  Monthly savings:   {_fmt_usd(result['monthly_savings'])}")
    print(f"  Yearly savings:    {_fmt_usd(result['yearly_savings'])}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="aicc",
        description="AI Cost Compass — Compare, estimate, and optimize AI API costs.",
    )
    parser.add_argument("-v", "--version", action="version",
                        version=f"%(prog)s {__version__}")
    parser.add_argument("--json", action="store_true",
                        help="Output as JSON")

    sub = parser.add_subparsers(dest="command")

    # list
    p_list = sub.add_parser("list", help="List available models")
    p_list.add_argument("-p", "--provider", choices=[p.value for p in Provider])
    p_list.add_argument("-s", "--search", help="Search by name")

    # estimate
    p_est = sub.add_parser("estimate", help="Estimate cost for a model")
    p_est.add_argument("model", help="Model ID (e.g. gpt-4o)")
    p_est.add_argument("-i", "--input-tokens", type=int, default=1000)
    p_est.add_argument("-o", "--output-tokens", type=int, default=500)
    p_est.add_argument("-c", "--cached", type=int, default=0,
                       help="Cached input tokens")

    # compare
    p_cmp = sub.add_parser("compare", help="Compare costs across models")
    p_cmp.add_argument("-i", "--input-tokens", type=int, default=1000)
    p_cmp.add_argument("-o", "--output-tokens", type=int, default=500)
    p_cmp.add_argument("-c", "--cached", type=int, default=0)
    p_cmp.add_argument("-p", "--provider", choices=[p.value for p in Provider])

    # daily
    p_day = sub.add_parser("daily", help="Estimate daily/monthly cost")
    p_day.add_argument("model", help="Model ID")
    p_day.add_argument("-n", "--calls", type=int, default=100,
                       help="Calls per day")
    p_day.add_argument("-i", "--input-tokens", type=int, default=1000)
    p_day.add_argument("-o", "--output-tokens", type=int, default=500)
    p_day.add_argument("--cache-rate", type=float, default=0.0,
                       help="Cache hit rate (0.0-1.0)")

    # recommend
    p_rec = sub.add_parser("recommend", help="Get model recommendations")
    p_rec.add_argument("task", choices=[t.value for t in TaskType])
    p_rec.add_argument("--budget", type=float, help="Max cost per call")
    p_rec.add_argument("--vision", action="store_true",
                       help="Must support vision")

    # savings
    p_save = sub.add_parser("savings", help="Calculate savings from switching")
    p_save.add_argument("current", help="Current model ID")
    p_save.add_argument("alternative", help="Alternative model ID")
    p_save.add_argument("-n", "--calls", type=int, default=100)
    p_save.add_argument("-i", "--input-tokens", type=int, default=1000)
    p_save.add_argument("-o", "--output-tokens", type=int, default=500)

    args = parser.parse_args()
    args.json = getattr(args, "json", False)

    if not args.command:
        parser.print_help()
        return

    handlers = {
        "list": cmd_list, "estimate": cmd_estimate,
        "compare": cmd_compare, "daily": cmd_daily,
        "recommend": cmd_recommend, "savings": cmd_savings,
    }
    handlers[args.command](args)


if __name__ == "__main__":
    main()
