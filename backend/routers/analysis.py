"""
POST /api/analyze — Full AI contract analysis
"""
import os, json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import anthropic

router = APIRouter()

PROMPT = """You are an expert legal AI. Analyze this contract carefully.
Respond ONLY with valid JSON — no markdown, no backticks, no extra text.

{{
  "summary": "2-3 sentence plain-English summary",
  "risk_score": <1.0-10.0>,
  "risk_level": "Low"|"Medium"|"High",
  "clauses": [{{"name":"...","risk":"high|medium|low","type":"Payment/Termination/Liability/NDA/Delivery/IP/Jurisdiction/Other","text":"one-sentence extract"}}],
  "obligations": [{{"party":"...","action":"...","deadline":"specific/Undefined/Vague"}}],
  "issues": [{{"severity":"high|medium|low","title":"...","desc":"..."}}],
  "recommendations": ["..."]
}}

Contract:
{text}"""


class AnalyzeRequest(BaseModel):
    text: str


@router.post("/analyze")
async def analyze(req: AnalyzeRequest):
    if len(req.text.strip()) < 50:
        raise HTTPException(400, "Contract text too short.")
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise HTTPException(500, "ANTHROPIC_API_KEY not set in .env")
    client = anthropic.Anthropic(api_key=api_key)
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            messages=[{"role": "user", "content": PROMPT.format(text=req.text[:4000])}],
        )
        raw   = msg.content[0].text
        clean = raw.replace("```json","").replace("```","").strip()
        start = clean.index("{"); end = clean.rindex("}") + 1
        return json.loads(clean[start:end])
    except json.JSONDecodeError:
        raise HTTPException(500, "AI returned invalid JSON — try again.")
    except anthropic.APIError as e:
        raise HTTPException(502, f"Anthropic API error: {e}")
