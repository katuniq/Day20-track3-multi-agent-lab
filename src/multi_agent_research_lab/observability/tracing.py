"""Tracing hooks.

This file intentionally avoids binding to one provider. Students can plug in LangSmith,
Langfuse, OpenTelemetry, or simple JSON traces.
"""

from collections.abc import Iterator
from contextlib import contextmanager
from time import perf_counter
from typing import Any

from langsmith.run_helpers import trace
from multi_agent_research_lab.core.config import get_settings


@contextmanager
def trace_span(name: str, attributes: dict[str, Any] | None = None) -> Iterator[dict[str, Any]]:
    """Minimal span context used by the skeleton, augmented with LangSmith."""
    settings = get_settings()
    
    # We maintain the local dictionary span for compatibility with the rest of the skeleton
    started = perf_counter()
    span: dict[str, Any] = {"name": name, "attributes": attributes or {}, "duration_seconds": None}
    
    if settings.langsmith_api_key:
        # Wrap with LangSmith trace context manager
        with trace(name, "span", inputs=attributes) as run:
            try:
                yield span
            finally:
                span["duration_seconds"] = perf_counter() - started
    else:
        # Standard fallback without LangSmith
        try:
            yield span
        finally:
            span["duration_seconds"] = perf_counter() - started

