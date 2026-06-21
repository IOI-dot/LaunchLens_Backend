import json
from llm import call_llm_json
from prompts import DISCOVERY_PROMPT, ANALYSIS_PROMPT, PLANNING_PROMPT

def discovery_agent(user_input: str):
    prompt = f"{DISCOVERY_PROMPT}\n\nUser Idea:\n{user_input}"
    return call_llm_json(prompt)

def analysis_agent(discovery_output: dict):
    project_type = discovery_output.get("project_type", "serious business project")
    if project_type == "personal hobby":
        focus = "Focus on ease of implementation, personal learning, and cost minimization."
    elif project_type == "university project":
        focus = "Focus on academic grading criteria, strict timeline constraints, and core requirements."
    else:
        focus = "Focus heavily on market fit, commercial feasibility, scaling, and business risks."
    prompt = f"""
{ANALYSIS_PROMPT}

Project Type: {project_type}
Analysis Focus: {focus}

Idea:
{json.dumps(discovery_output, indent=2)}
"""
    return call_llm_json(prompt)

def planning_agent(discovery_output: dict, analysis_output: dict):
    project_type = discovery_output.get("project_type", "serious business project")
    if project_type == "personal hobby":
        focus = "Prioritize quick setup, minimal cost, and developer enjoyment."
    elif project_type == "university project":
        focus = "Guarantee meeting submission deadlines and grading criteria."
    else:
        focus = "Prioritize commercial launch, security, scaling, and user growth."
    prompt = f"""
{PLANNING_PROMPT}

Project Type: {project_type}
Planning Focus: {focus}

Idea:
{json.dumps(discovery_output, indent=2)}

Analysis:
{json.dumps(analysis_output, indent=2)}
"""
    return call_llm_json(prompt)