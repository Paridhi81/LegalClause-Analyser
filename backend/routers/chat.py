"""
POST /api/chat — AI lawyer conversation
"""
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import anthropic

router = APIRouter()

SYSTEM = """You are an expert AI legal assistant. Contract context: {ctx}
Be concise, practical, legally precise. Max 160 words. Always recommend consulting a lawyer for binding decisions."""


class Msg(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Msg]
    contract_context: str = ""


@router.post("/chat")
async def chat(req: ChatRequest):
    if not req.messages:
        raise HTTPException(400, "No messages.")
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise HTTPException(500, "ANTHROPIC_API_KEY not set.")
    client = anthropic.Anthropic(api_key=api_key)
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=SYSTEM.format(ctx=req.contract_context[:1000] or "None"),
            messages=[{"role": m.role, "content": m.content} for m in req.messages[-20:]],
        )
        return {"reply": msg.content[0].text}
    except anthropic.APIError as e:
        raise HTTPException(502, f"Anthropic API error: {e}")
