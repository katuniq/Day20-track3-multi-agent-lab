"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`."""
        llm = LLMClient()
        system_prompt = "You are an expert technical writer. Write a clear, comprehensive final answer based on the research and analysis notes provided. Include source references."
        user_prompt = f"Query: {state.request.query}\n\nResearch Notes:\n{state.research_notes or 'None'}\n\nAnalysis Notes:\n{state.analysis_notes or 'None'}"

        response = llm.complete(system_prompt=system_prompt, user_prompt=user_prompt)
        state.final_answer = response.content

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
