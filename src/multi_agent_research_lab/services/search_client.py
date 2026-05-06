"""Search client abstraction for ResearcherAgent."""

import os
import json
import urllib.request
from typing import Any

from multi_agent_research_lab.core.errors import StudentTodoError
from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("TAVILY_API_KEY")

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query."""
        if not self.api_key:
            # Local mock fallback
            return [
                SourceDocument(
                    title=f"Mock Result for {query}",
                    url="https://example.com/mock-result",
                    snippet=f"This is a mocked search result for the query: {query}. It contains simulated information.",
                    metadata={"source": "mock"}
                )
            ]
            
        try:
            req = urllib.request.Request(
                "https://api.tavily.com/search",
                data=json.dumps({"query": query, "api_key": self.api_key, "max_results": max_results}).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
            
            docs = []
            for r in result.get("results", []):
                docs.append(SourceDocument(
                    title=r.get("title", "Untitled"),
                    url=r.get("url", ""),
                    snippet=r.get("content", ""),
                    metadata={"score": r.get("score")}
                ))
            return docs
        except Exception as e:
            # Fallback to mock on error
            return [
                SourceDocument(
                    title=f"Error Search for {query}",
                    url="https://example.com/error",
                    snippet=f"Search failed with error: {str(e)}. Mocking fallback.",
                    metadata={"source": "mock_error"}
                )
            ]
