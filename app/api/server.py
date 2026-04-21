import os
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from app.agent.insurance_agent import LifeInsuranceAgent


load_dotenv()

app = FastAPI(
    title="Life Insurance Support Agent API",
    description="AI-powered assistant for life insurance inquiries",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent: Optional[LifeInsuranceAgent] = None

# In-memory session storage (in production, use Redis or database)
sessions: dict[str, List[BaseMessage]] = {}


# Request/Response Models
class ChatMessage(BaseModel):
    """Chat message model."""
    role: str = Field(..., description="Role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User message", min_length=1)
    session_id: Optional[str] = Field(default="default", description="Session ID for conversation history")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="AI assistant response")
    session_id: str = Field(..., description="Session ID")


class SessionHistoryResponse(BaseModel):
    """Response model for session history."""
    session_id: str
    messages: List[ChatMessage]


@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup."""
    global agent

    # Get configuration from environment
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    vector_store_path = os.getenv("VECTOR_STORE_PATH", "./data/vector_store")
    top_k_results = int(os.getenv("TOP_K_RESULTS", "3"))

    print("Initializing Life Insurance Agent...")
    agent = LifeInsuranceAgent(
        model_name=model_name,
        embedding_model=embedding_model,
        vector_store_path=vector_store_path,
        top_k_results=top_k_results
    )
    print("Agent initialized successfully!")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Life Insurance Support Agent",
        "version": "1.0.0"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the life insurance agent.

    Args:
        request: Chat request containing user message and optional session ID

    Returns:
        AI response
    """
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    try:

        session_id = request.session_id
        conversation_history = sessions.get(session_id, [])

        # Get response from agent
        response = await agent.achat(
            user_query=request.message,
            conversation_history=conversation_history
        )

        # Update session history
        conversation_history.extend([
            HumanMessage(content=request.message),
            AIMessage(content=response)
        ])
        sessions[session_id] = conversation_history

        return ChatResponse(
            response=response,
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


@app.get("/sessions/{session_id}/history", response_model=SessionHistoryResponse)
async def get_session_history(session_id: str):
    """
    Get conversation history for a session.

    Args:
        session_id: Session identifier

    Returns:
        Conversation history
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = []
    for msg in sessions[session_id]:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        messages.append(ChatMessage(role=role, content=msg.content))

    return SessionHistoryResponse(
        session_id=session_id,
        messages=messages
    )


@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """
    Clear conversation history for a session.

    Args:
        session_id: Session identifier

    Returns:
        Success message
    """
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} cleared successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@app.get("/sessions")
async def list_sessions():
    """
    List all active sessions.

    Returns:
        List of session IDs with message counts
    """
    return {
        "sessions": [
            {"session_id": sid, "message_count": len(msgs)}
            for sid, msgs in sessions.items()
        ]
    }


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))

    uvicorn.run(app, host=host, port=port)
