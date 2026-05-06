"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient
from multi_agent_research_lab.services.search_client import SearchClient


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`."""
        search = SearchClient()
        sources = search.search(state.request.query, max_results=state.request.max_sources)
        state.sources.extend(sources)

        # Format sources for LLM
        sources_text = "\n".join([f"- {s.title}: {s.snippet}" for s in sources])

        llm = LLMClient()
        system_prompt = "You are a research assistant. Extract concise research notes from the provided search results based on the user's query."
        user_prompt = f"Query: {state.request.query}\nSources:\n{sources_text}"

        response = llm.complete(system_prompt=system_prompt, user_prompt=user_prompt)
        state.research_notes = response.content

        state.agent_results.append(
            AgentResult(
                agent=self.name,
                content=response.content,
                metadata={
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                },
            )
        )

        return state
