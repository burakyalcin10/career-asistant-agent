"""
Unknown Question Detection Tool
Detects when the agent lacks sufficient knowledge to answer,
using a hybrid approach: keyword matching + LLM confidence scoring.
"""
import google.generativeai as genai
from config import settings
from models import UnknownQuestionResult
import json
import re
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)

# Keyword-based detection patterns
UNKNOWN_PATTERNS = {
    "salary_negotiation": [
        "salary", "compensation", "pay", "wage", "maaş", "ücret", "maaş beklentisi",
        "salary expectation", "negotiate", "package", "offer amount", "annual salary",
        "hourly rate", "stock options", "equity", "bonus"
    ],
    "legal": [
        "legal", "contract terms", "liability", "non-compete", "NDA", "intellectual property",
        "lawsuit", "legal obligation", "terms and conditions", "sözleşme", "hukuki",
        "yasal", "gizlilik sözleşmesi", "patent"
    ],
    "out_of_domain": [
        "blockchain", "cryptocurrency", "trading", "forex", "medical",
        "pharmaceutical", "biotechnology", "mechanical engineering",
        "civil engineering", "chemical engineering", "law degree"
    ],
    "ambiguous_offer": [
        "relocate immediately", "start tomorrow", "urgent position",
        "confidential opportunity", "guaranteed income", "work from home earning",
        "multi-level", "MLM", "investment opportunity"
    ]
}


def keyword_check(message: str) -> tuple[bool, str, list[str]]:
    """
    Check message against keyword patterns.
    Returns: (is_flagged, category, matched_keywords)
    """
    message_lower = message.lower()
    
    for category, keywords in UNKNOWN_PATTERNS.items():
        matched = [kw for kw in keywords if kw.lower() in message_lower]
        if matched:
            return True, category, matched
    
    return False, "clear", []


CONFIDENCE_PROMPT = """You are a confidence assessment system for a Career Assistant AI Agent representing Burak Yalçın,
a Computer Engineering student with experience in Python, FastAPI, AI/ML, LangChain, Angular, Spring Boot.

Analyze the following employer message and determine if the agent can confidently handle it.

EMPLOYER'S MESSAGE:
{message}

Assess the following:
1. Does the agent have enough information from the candidate's CV to answer this?
2. Is this within the candidate's domain of expertise?
3. Does this require human intervention (salary negotiation, legal matters, ambiguous offers)?
4. How confident is the agent in handling this message? (0.0 to 1.0)

Respond ONLY in valid JSON:
{{
    "is_unknown": <boolean>,
    "confidence_score": <float 0.0-1.0>,
    "category": "<salary_negotiation|legal|out_of_domain|ambiguous_offer|clear>",
    "reason": "<brief explanation>"
}}
"""


async def detect_unknown_question(message: str) -> UnknownQuestionResult:
    """
    Detect if a question is outside the agent's knowledge scope.
    Uses hybrid approach: keyword matching + LLM confidence scoring.
    
    Args:
        message: The employer's message to analyze
    
    Returns:
        UnknownQuestionResult with detection details
    """
    # Step 1: Keyword-based check
    is_flagged, kw_category, matched_keywords = keyword_check(message)
    
    # Step 2: LLM confidence scoring
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction="You are a confidence assessment system. Respond only in valid JSON."
        )
        
        prompt = CONFIDENCE_PROMPT.format(message=message)
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean markdown code blocks
        if response_text.startswith("```"):
            response_text = re.sub(r'^```(?:json)?\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
        
        llm_result = json.loads(response_text)
        
        llm_is_unknown = llm_result.get("is_unknown", False)
        llm_confidence = float(llm_result.get("confidence_score", 0.8))
        llm_category = llm_result.get("category", "clear")
        llm_reason = llm_result.get("reason", "")
        
    except Exception as e:
        logger.error(f"LLM confidence check failed: {e}")
        llm_is_unknown = False
        llm_confidence = 0.7
        llm_category = "clear"
        llm_reason = "LLM check failed, using keyword results only."
    
    # Step 3: Combine results (hybrid)
    # If either method flags it, mark as unknown
    final_is_unknown = is_flagged or llm_is_unknown
    final_confidence = llm_confidence
    final_category = kw_category if is_flagged else llm_category
    
    if is_flagged:
        reason = f"Keyword match detected ({', '.join(matched_keywords)}). {llm_reason}"
        # Lower confidence when keywords are matched
        final_confidence = min(final_confidence, 0.5)
    else:
        reason = llm_reason
    
    # Apply confidence threshold
    if final_confidence < settings.CONFIDENCE_THRESHOLD:
        final_is_unknown = True
    
    result = UnknownQuestionResult(
        is_unknown=final_is_unknown,
        confidence_score=round(final_confidence, 2),
        category=final_category,
        reason=reason
    )
    
    if result.is_unknown:
        logger.warning(f"Unknown question detected! Category: {final_category}, Confidence: {final_confidence}")
    
    return result
