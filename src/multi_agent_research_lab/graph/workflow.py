"""LangGraph workflow skeleton."""

from langgraph.graph import END, StateGraph

from multi_agent_research_lab.agents.analyst import AnalystAgent
from multi_agent_research_lab.agents.critic import CriticAgent
from multi_agent_research_lab.agents.researcher import ResearcherAgent
from multi_agent_research_lab.agents.supervisor import SupervisorAgent
from multi_agent_research_lab.agents.writer import WriterAgent
from multi_agent_research_lab.core.state import ResearchState


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph."""

    def build(self) -> object:
        """Create a LangGraph graph."""
        graph = StateGraph(ResearchState)

        # Wrap node functions with trace_span
        def run_agent(agent_name: str, agent_obj):
            def _wrapped(state: ResearchState) -> ResearchState:
                from multi_agent_research_lab.observability.tracing import trace_span

                with trace_span(agent_name, {"iteration": state.iteration}) as span:
                    new_state = agent_obj.run(state)
                    new_state.add_trace_event(agent_name, span)
                    return new_state

            return _wrapped

        # Add nodes
        graph.add_node("supervisor", run_agent("supervisor", SupervisorAgent()))
        graph.add_node("researcher", run_agent("researcher", ResearcherAgent()))
        graph.add_node("analyst", run_agent("analyst", AnalystAgent()))
        graph.add_node("writer", run_agent("writer", WriterAgent()))
        graph.add_node("critic", run_agent("critic", CriticAgent()))

        # Add edges
        graph.set_entry_point("supervisor")

        # Conditional routing from supervisor
        def route(state: ResearchState) -> str:
            if not state.route_history:
                return "researcher"
            last_route = state.route_history[-1]
            if last_route == "done":
                return END
            return last_route

        graph.add_conditional_edges("supervisor", route)

        # Worker agents return to supervisor
        graph.add_edge("researcher", "supervisor")
        graph.add_edge("analyst", "supervisor")
        graph.add_edge("writer", "critic")
        graph.add_edge("critic", "supervisor")

        return graph.compile()

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state."""
        app = self.build()
        result = app.invoke(state)
        # LangGraph invoke returns a dictionary with the final state if using typed dict, but with Pydantic it might return the BaseModel or a dict.
        # Since ResearchState is a Pydantic BaseModel, langgraph may return a dict or the model itself.
        if isinstance(result, ResearchState):
            return result
        elif isinstance(result, dict):
            return ResearchState(**result)
        return state
