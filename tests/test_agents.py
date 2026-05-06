from multi_agent_research_lab.agents import SupervisorAgent
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState


def test_supervisor_agent_routes() -> None:
    state = ResearchState(request=ResearchQuery(query="Explain multi-agent systems"))
    new_state = SupervisorAgent().run(state)
    assert new_state.route_history == ["researcher"]
    assert new_state.iteration == 1
