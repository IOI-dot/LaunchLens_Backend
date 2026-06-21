from pydantic import BaseModel
from typing import List, Dict, Any

class IdeaState(BaseModel):
    user_input: str
    idea_summary: str = ""
    domain: str = ""
    ambiguity: str = ""
    project_type: str = ""
    clarified_idea: str = ""
    constraints: Dict[str, Any] = {}
    assumptions: List[str] = []
    risks: List[Dict[str, Any]] = []
    execution_paths: Dict[str, Any] = {}
    tradeoffs: Dict[str, Any] = {}
    recommendation: Dict[str, Any] = {}
    milestones: List[str] = []
    plan_30: List[str] = []
    plan_60: List[str] = []
    plan_90: List[str] = []
    first_action: str = ""
    confidence: str = ""
    uncertainties: List[str] = []