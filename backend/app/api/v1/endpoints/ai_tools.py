"""AI Tools integration endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from pathlib import Path
import json
from uuid import uuid4

from app.core.database import get_db
from app.core.config import settings
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User

router = APIRouter()
RAG_STORAGE_DIR = Path(settings.UPLOAD_DIR) / "rag_documents"
RAG_STORAGE_DIR.mkdir(parents=True, exist_ok=True)


class ChatMessage(BaseModel):
    """Chat message schema"""
    message: str
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000


class ChatResponse(BaseModel):
    """Chat response schema"""
    response: str
    tokens_used: int = 0
    cost: float = 0.0


class RAGQuery(BaseModel):
    """RAG query schema"""
    query: str
    collection_id: Optional[str] = None
    top_k: int = 5


@router.post("/chat", response_model=ChatResponse)
async def chat_with_llm(
    message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with LLM"""
    # Basic offline-friendly fallback that does not require external APIs.
    # If an API key is configured, we attempt a real call; otherwise return a simulated reply.
    if settings.OPENAI_API_KEY:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            completion = client.chat.completions.create(
                model=message.model,
                messages=[{"role": "user", "content": message.message}],
                temperature=message.temperature,
                max_tokens=message.max_tokens,
            )
            content = completion.choices[0].message.content
            usage = getattr(completion, "usage", None)
            return ChatResponse(
                response=content or "I couldn't generate a response.",
                tokens_used=(usage.total_tokens if usage else 0),
                cost=0.0,  # Cost calculation would depend on provider pricing
            )
        except Exception as exc:
            # Fall back to simulated response
            simulated = (
                "LLM call failed, returning a simulated response instead. "
                f"Reason: {exc}"
            )
            return ChatResponse(response=simulated, tokens_used=0, cost=0.0)

    fallback = (
        "This is a simulated assistant response. Provide an OpenAI API key to "
        "enable live LLM replies.\n\n"
        f"Your message: {message.message}"
    )
    return ChatResponse(response=fallback, tokens_used=0, cost=0.0)


@router.post("/rag/query")
async def rag_query(
    query: RAGQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Query RAG system"""
    query_text = query.query.lower()
    results = []

    for meta_file in RAG_STORAGE_DIR.glob("*.json"):
        metadata = json.loads(meta_file.read_text())
        text_path = RAG_STORAGE_DIR / f"{metadata['id']}.txt"
        if not text_path.exists():
            continue
        doc_text = text_path.read_text(errors="ignore")
        score = doc_text.lower().count(query_text)
        if score > 0:
            snippet = doc_text[:300]
            results.append({
                "document_id": metadata["id"],
                "filename": metadata["filename"],
                "score": score,
                "snippet": snippet
            })

    sorted_results = sorted(results, key=lambda r: r["score"], reverse=True)
    return {
        "query": query.query,
        "results": sorted_results[: query.top_k],
        "message": "RAG query executed",
    }


@router.post("/rag/upload")
async def upload_document_for_rag(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload document for RAG"""
    content = await file.read()
    text = content.decode("utf-8", errors="ignore")

    doc_id = uuid4().hex
    text_path = RAG_STORAGE_DIR / f"{doc_id}.txt"
    meta_path = RAG_STORAGE_DIR / f"{doc_id}.json"

    text_path.write_text(text)
    meta_path.write_text(json.dumps({
        "id": doc_id,
        "filename": file.filename,
        "size": len(content)
    }))

    return {
        "message": "Document uploaded for RAG",
        "document_id": doc_id,
        "filename": file.filename
    }

