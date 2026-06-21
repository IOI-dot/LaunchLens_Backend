import json
from llm import call_llm_json
from prompts import DISCOVERY_PROMPT, ANALYSIS_PROMPT, PLANNING_PROMPT, CLARIFICATION_PROMPT


def _context_block(context: dict) -> str:
    """Build a prompt snippet from the user's Phase 2 question-answer pairs."""
    if not context:
        return ""
    answers = context.get("answers", [])
    if not answers:
        return ""
    parts = []
    for a in answers:
        if a.get("question") and a.get("answer"):
            parts.append(f"- {a['question']}: {a['answer']}")
    if not parts:
        return ""
    return (
        "\n\nUser Context (calibrate ALL recommendations to these specifics — "
        "milestones, timelines, costs, and first steps must reflect this exactly):\n"
        + "\n".join(parts) + "\n"
    )


def clarification_agent(user_input: str) -> list:
    prompt = f"{CLARIFICATION_PROMPT}\n\nUser Idea:\n{user_input}"
    result = call_llm_json(prompt)
    return result.get("questions", [])


def discovery_agent(user_input: str, context: dict = None):
    context = context or {}
    ctx = _context_block(context)
    prompt = f"{DISCOVERY_PROMPT}{ctx}\n\nUser Idea:\n{user_input}"
    return call_llm_json(prompt)


def analysis_agent(discovery_output: dict, context: dict = None):
    context = context or {}
    ctx = _context_block(context)
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
Analysis Focus: {focus}{ctx}

Idea:
{json.dumps(discovery_output, indent=2)}
"""
    return call_llm_json(prompt)


def planning_agent(discovery_output: dict, analysis_output: dict, context: dict = None):
    context = context or {}
    ctx = _context_block(context)
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
Planning Focus: {focus}{ctx}

Idea:
{json.dumps(discovery_output, indent=2)}

Analysis:
{json.dumps(analysis_output, indent=2)}
"""
    return call_llm_json(prompt)