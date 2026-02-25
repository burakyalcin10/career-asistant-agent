"""
Pydantic models for request/response schemas.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class EmployerMessage(BaseModel):
    """Incoming message from a potential employer."""
    sender_name: str = "Employer"
    sender_email: str = "employer@company.com"
    subject: str = "General Inquiry"
    message: str


class EvaluationResult(BaseModel):
    """Result from the Response Evaluator Agent."""
    overall_score: float
    professional_tone: float
    clarity: float
    completeness: float
    safety: float
    relevance: float
    feedback: str
    passed: bool


class UnknownQuestionResult(BaseModel):
    """Result from the Unknown Question Detector."""
    is_unknown: bool
    confidence_score: float
    category: str  # e.g., "salary_negotiation", "legal", "out_of_domain", "clear"
    reason: str


class AgentResponse(BaseModel):
    """Complete response from the Career Agent system."""
    original_message: str
    generated_response: str
    evaluation: EvaluationResult
    unknown_detection: UnknownQuestionResult
    revision_count: int
    conversation_id: str
    timestamp: str
    notification_sent: bool


class ConversationEntry(BaseModel):
    """A single conversation entry for history tracking."""
    id: str
    employer_message: str
    agent_response: str
    evaluation_score: float
    is_unknown: bool
    confidence: float
    timestamp: str
    revision_count: int
