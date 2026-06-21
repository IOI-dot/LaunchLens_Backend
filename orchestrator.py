from agents import discovery_agent, analysis_agent, planning_agent
from schemas import IdeaState
# from llm import check_safety  ← comment this out

def generate_execution_plan(user_input: str) -> IdeaState:

    # STEP 0: DISABLED — re-enable when credits available
    # try:
    #     if check_safety(user_input):
    #         raise ValueError("Input violated safety policies.")
    # except ValueError as e:
    #     raise e
    # except Exception as e:
    #     raise RuntimeError(f"Safety check failed: {str(e)}") from e

    try:
        discovery = discovery_agent(user_input)
    except Exception as e:
        raise ValueError(f"Discovery phase failed: {str(e)}") from e

    try:
        analysis = analysis_agent(discovery)
    except Exception as e:
        raise ValueError(f"Analysis phase failed: {str(e)}") from e

    try:
        planning = planning_agent(discovery, analysis)
    except Exception as e:
        raise ValueError(f"Planning phase failed: {str(e)}") from e

    return IdeaState(
        user_input=user_input,
        **discovery,
        **analysis,
        **planning
    )