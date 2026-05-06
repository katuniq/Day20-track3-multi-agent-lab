"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`."""
        llm = LLMClient()
        system_prompt = "You are a research analyst. Given the research notes, extract key claims, compare viewpoints, and provide structured insights."
        user_prompt = f"Query: {state.request.query}\nResearch Notes:\n{state.research_notes or 'None'}"
        
        response = llm.complete(system_prompt=system_prompt, user_prompt=user_prompt)
        state.analysis_notes = response.content
        
        state.agent_results.append(AgentResult(
            agent=self.name,
            content=response.content,
            metadata={"input_tokens": response.input_tokens, "output_tokens": response.output_tokens}
        ))
        
        return state
