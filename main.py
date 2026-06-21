from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
from orchestrator import generate_execution_plan
from agents import clarification_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class IdeaRequest(BaseModel):
    user_input: str
    context: Dict[str, Any] = {}

class ClarifyRequest(BaseModel):
    user_input: str

@app.post("/api/clarify")
async def clarify(req: ClarifyRequest):
    try:
        questions = clarification_agent(req.user_input)
        return {"questions": questions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/plan")
async def plan(req: IdeaRequest):
    try:
        result = generate_execution_plan(req.user_input, req.context)
        return result.dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))