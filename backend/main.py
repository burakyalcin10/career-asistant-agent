"""
Career Assistant AI Agent - FastAPI Backend
Main application with agent loop, tool invocation, and API endpoints.
"""
import uuid
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from models import EmployerMessage, AgentResponse, ConversationEntry, EvaluationResult, UnknownQuestionResult
from career_agent import process_message_unified
from notification import notify_new_message, notify_response_sent, notify_unknown_question, send_response_to_employer
from config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Career Assistant AI Agent",
    description="An AI agent that communicates with potential employers on behalf of Burak Yalçın",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory conversation history (bonus: memory feature)
conversation_history: list[ConversationEntry] = []

# Agent loop logs
agent_logs: list[dict] = []


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agent": "Career Assistant AI Agent",
        "candidate": "Burak Yalçın",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/message", response_model=AgentResponse)
async def process_employer_message(msg: EmployerMessage):
    """
    Main Agent Loop (Single-Call Architecture):
    1. Receive employer message
    2. Single Gemini API call: detect + generate + evaluate
    3. Send notifications
    4. Return final response
    """
    conversation_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().isoformat()
    
    logger.info(f"[{conversation_id}] New message from {msg.sender_name}: {msg.message[:100]}...")
    
    # Step 1: Notify about new message
    notify_new_message(msg.sender_name, msg.message[:300])
    
    # Step 2: Single unified API call (detect + generate + evaluate)
    logger.info(f"[{conversation_id}] Processing with unified single API call...")
    
    try:
        result = await process_message_unified(msg.message)
    except Exception as e:
        logger.error(f"[{conversation_id}] Unified processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    # Parse results
    response_text = result["generated_response"]
    
    # Build evaluation
    eval_data = result.get("evaluation", {})
    overall_score = float(eval_data.get("overall_score", 8.0))
    evaluation = EvaluationResult(
        overall_score=overall_score,
        professional_tone=float(eval_data.get("professional_tone", 8.0)),
        clarity=float(eval_data.get("clarity", 8.0)),
        completeness=float(eval_data.get("completeness", 8.0)),
        safety=float(eval_data.get("safety", 9.0)),
        relevance=float(eval_data.get("relevance", 8.0)),
        feedback=eval_data.get("feedback", "Self-evaluated."),
        passed=overall_score >= settings.EVALUATION_THRESHOLD
    )
    
    # Build unknown detection
    unknown_data = result.get("unknown_detection", {})
    unknown_result = UnknownQuestionResult(
        is_unknown=bool(unknown_data.get("is_unknown", False)),
        confidence_score=float(unknown_data.get("confidence_score", 0.9)),
        category=unknown_data.get("category", "clear"),
        reason=unknown_data.get("reason", "")
    )
    
    if unknown_result.is_unknown:
        logger.warning(f"[{conversation_id}] Unknown question detected: {unknown_result.category}")
        notify_unknown_question(
            msg.sender_name,
            msg.message,
            unknown_result.category,
            unknown_result.confidence_score
        )
    
    logger.info(f"[{conversation_id}] Final score: {evaluation.overall_score}/10")
    
    # Step 3: Notify that response is approved
    notification_sent = notify_response_sent(
        msg.sender_name,
        response_text,
        evaluation.overall_score
    )
    
    # Step 3b: Forward response to employer if AI decides it's appropriate
    should_email = result.get("should_email_employer", False)
    employer_email_sent = False
    if should_email and msg.sender_email:
        employer_email_sent = send_response_to_employer(
            employer_email=msg.sender_email,
            employer_name=msg.sender_name,
            response_text=response_text
        )
        if employer_email_sent:
            logger.info(f"[{conversation_id}] Response forwarded to employer: {msg.sender_email}")
        else:
            logger.warning(f"[{conversation_id}] Failed to forward response to employer")
    
    # Step 4: Save to conversation history (memory)
    entry = ConversationEntry(
        id=conversation_id,
        employer_message=msg.message,
        agent_response=response_text,
        evaluation_score=evaluation.overall_score,
        is_unknown=unknown_result.is_unknown,
        confidence=unknown_result.confidence_score,
        timestamp=timestamp,
        revision_count=0
    )
    conversation_history.append(entry)
    
    agent_logs.append({
        "conversation_id": conversation_id,
        "event": "response_approved",
        "score": evaluation.overall_score,
        "revision_count": 0,
        "unknown_detected": unknown_result.is_unknown,
        "notification_sent": notification_sent,
        "timestamp": datetime.now().isoformat()
    })
    
    # Return complete response
    return AgentResponse(
        original_message=msg.message,
        generated_response=response_text,
        evaluation=evaluation,
        unknown_detection=unknown_result,
        revision_count=0,
        conversation_id=conversation_id,
        timestamp=timestamp,
        notification_sent=notification_sent
    )


@app.get("/api/history")
async def get_conversation_history():
    """Get conversation history (memory feature)."""
    return {"conversations": conversation_history}


@app.get("/api/logs")
async def get_agent_logs():
    """Get agent operation logs."""
    return {"logs": agent_logs}


# Serve frontend
frontend_path = Path(__file__).resolve().parent.parent / "frontend"

@app.get("/")
async def serve_frontend():
    """Serve the main HTML page."""
    return FileResponse(frontend_path / "index.html")

# Mount static files
app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")


if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting Career Assistant AI Agent Server...")
    logger.info(f"📧 Email notifications: {'configured' if settings.EMAIL_SENDER else 'not configured'}")
    logger.info(f"🤖 Gemini API: {'configured' if settings.GEMINI_API_KEY else 'NOT configured'}")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
