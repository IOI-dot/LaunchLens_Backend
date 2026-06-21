from agents import discovery_agent, analysis_agent, planning_agent
from schemas import IdeaState

def generate_execution_plan(user_input: str, context: dict = None) -> IdeaState:
    context = context or {}

    try:
        discovery = discovery_agent(user_input, context)
    except Exception as e:
        raise ValueError(f"Discovery phase failed: {str(e)}") from e

    try:
        analysis = analysis_agent(discovery, context)
    except Exception as e:
        raise ValueError(f"Analysis phase failed: {str(e)}") from e

    try:
        planning = planning_agent(discovery, analysis, context)
    except Exception as e:
        raise ValueError(f"Planning phase failed: {str(e)}") from e

    return IdeaState(
        user_input=user_input,
        **discovery,
        **analysis,
        **planning
    )