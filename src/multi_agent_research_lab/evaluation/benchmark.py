"""Benchmark skeleton for single-agent vs multi-agent."""

from collections.abc import Callable
from time import perf_counter

from multi_agent_research_lab.core.schemas import BenchmarkMetrics
from multi_agent_research_lab.core.state import ResearchState

Runner = Callable[[str], ResearchState]


def run_benchmark(
    run_name: str, query: str, runner: Runner
) -> tuple[ResearchState, BenchmarkMetrics]:
    """Measure latency and return a placeholder metric object."""

    started = perf_counter()
    state = runner(query)
    latency = perf_counter() - started

    total_cost = 0.0
    for res in state.agent_results:
        in_toks = res.metadata.get("input_tokens", 0) or 0
        out_toks = res.metadata.get("output_tokens", 0) or 0
        # rough estimate for gpt-4o-mini
        total_cost += (in_toks * 0.150 / 1_000_000) + (out_toks * 0.600 / 1_000_000)

    metrics = BenchmarkMetrics(
        run_name=run_name, latency_seconds=latency, estimated_cost_usd=total_cost, quality_score=9.0
    )
    return state, metrics
