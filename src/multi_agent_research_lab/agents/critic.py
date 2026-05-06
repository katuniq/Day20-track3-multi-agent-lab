"""Optional critic agent skeleton for bonus work."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class CriticAgent(BaseAgent):
    """Optional fact-checking and safety-review agent."""

    name = "critic"

    def run(self, state: ResearchState) -> ResearchState:
        """Validate final answer and append findings."""
        if not state.final_answer:
            return state
            
        llm = LLMClient()
        system_prompt = "You are a critical fact-checker. Review the provided answer against the notes and source materials for hallucination and citation coverage."
        user_prompt = f"Query: {state.request.query}\n\nFinal Answer:\n{state.final_answer}\n\nReview this answer and provide critique."
        
        response = llm.complete(system_prompt=system_prompt, user_prompt=user_prompt)
        
        state.agent_results.append(AgentResult(
            agent=self.name,
            content=response.content,
            metadata={"input_tokens": response.input_tokens, "output_tokens": response.output_tokens, "type": "critique"}
        ))
        
        return state
