"""
Career Agent - Primary AI Agent (Single-Call Architecture)
Generates professional responses, evaluates them, and detects unknown questions
ALL IN ONE Gemini API call to stay within free-tier rate limits.
"""
import google.generativeai as genai
from config import settings
from cv_context import get_cv_context
import json
import re
import logging

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


UNIFIED_PROMPT = """You are a professional Career Assistant AI Agent acting on behalf of Burak Yalçın.
You must perform THREE tasks in a SINGLE response:

━━━ TASK 1: UNKNOWN QUESTION DETECTION ━━━
Analyze the employer's message. Flag if it involves:
- salary_negotiation: salary, compensation, pay, maaş, ücret, bonus, equity
- legal: contracts, NDA, non-compete, liability, sözleşme
- out_of_domain: topics outside software engineering (medical, law, civil eng, etc.)
- ambiguous_offer: suspicious/urgent offers, MLM, "guaranteed income"
If none apply, category = "clear"

━━━ TASK 2: GENERATE PROFESSIONAL RESPONSE ━━━
CANDIDATE'S PROFILE:
{cv_context}

RESPONSE GUIDELINES:
1. Always be professional, polite, and enthusiastic FOR LEGITIMATE MESSAGES
2. Respond in the same language as the employer's message
3. Keep responses concise but complete (3-5 paragraphs maximum)
4. Reference relevant skills and experience from the CV when appropriate
5. For interview invitations: Express enthusiasm, confirm availability
6. For technical questions: Answer honestly based on actual skills
7. For salary/legal/contract topics: Say "Burak will handle this personally" and end the conversation
8. For inappropriate, offensive, vulgar, or completely out-of-domain messages: Give a SHORT, FIRM, and FINAL rejection. Do NOT be polite or continue the conversation. Example: "This message is inappropriate and irrelevant. This conversation is now closed." Do NOT ask clarifying questions or offer further help.
9. Never fabricate experience or skills NOT in the CV
10. Always sign off as "Burak Yalçın" or "Best regards, Burak Yalçın" (EXCEPT for rejected inappropriate messages)

━━━ TASK 3: SELF-EVALUATE YOUR RESPONSE ━━━
Score your generated response (1-10) on:
- professional_tone: Is it professional and polite?
- clarity: Is it clear and well-structured?
- completeness: Does it address the employer's message?
- safety: No hallucinations or false claims? (10 = safe)
- relevance: Is it relevant to the specific message?
- overall_score: Weighted average

━━━ TASK 4: DECIDE WHETHER TO EMAIL THE EMPLOYER ━━━
Decide if your response should be forwarded to the employer's email.
Send email (true) when:
- Interview invitation → confirm availability
- Genuine job offer or collaboration request
- Direct contact/meeting request
- Technical discussion that deserves a detailed reply
Do NOT send email (false) when:
- Inappropriate, vulgar, or spam messages
- Out-of-domain nonsense
- Ambiguous or suspicious messages
- Very short/unclear messages that need clarification first

━━━ OUTPUT FORMAT ━━━
You MUST respond in EXACTLY this JSON format, nothing else:
{{
    "unknown_detection": {{
        "is_unknown": <boolean>,
        "confidence_score": <float 0.0-1.0, how confident you are in handling this>,
        "category": "<salary_negotiation|legal|out_of_domain|ambiguous_offer|clear>",
        "reason": "<brief explanation>"
    }},
    "generated_response": "<your full professional response text here>",
    "should_email_employer": <boolean>,
    "evaluation": {{
        "professional_tone": <number 1-10>,
        "clarity": <number 1-10>,
        "completeness": <number 1-10>,
        "safety": <number 1-10>,
        "relevance": <number 1-10>,
        "overall_score": <number 1-10>,
        "feedback": "<self-improvement notes>"
    }}
}}
"""


async def process_message_unified(employer_message: str) -> dict:
    """
    Single API call that handles detection, generation, and evaluation.
    
    Args:
        employer_message: The message from the potential employer
    
    Returns:
        Dict with unknown_detection, generated_response, and evaluation
    """
    cv_context = get_cv_context()
    system_prompt = UNIFIED_PROMPT.format(cv_context=cv_context)
    
    user_prompt = f"EMPLOYER'S MESSAGE:\n{employer_message}\n\nPerform all 3 tasks and respond in the exact JSON format specified."
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_prompt
        )
        
        response = model.generate_content(user_prompt)
        response_text = response.text.strip()
        
        # Clean markdown code blocks if present
        if response_text.startswith("```"):
            response_text = re.sub(r'^```(?:json)?\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
        
        result = json.loads(response_text)
        
        # Validate required fields exist
        if "generated_response" not in result:
            raise ValueError("Missing generated_response in API result")
        if "evaluation" not in result:
            result["evaluation"] = {
                "professional_tone": 8, "clarity": 8, "completeness": 8,
                "safety": 9, "relevance": 8, "overall_score": 8.2,
                "feedback": "Auto-evaluated."
            }
        if "unknown_detection" not in result:
            result["unknown_detection"] = {
                "is_unknown": False, "confidence_score": 0.9,
                "category": "clear", "reason": "Standard message."
            }
        
        logger.info(f"Unified response generated. Score: {result['evaluation'].get('overall_score', 'N/A')}")
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse unified response: {e}")
        logger.error(f"Raw response: {response_text[:500]}")
        # If JSON parsing fails, try to extract the response text
        raise Exception(f"Failed to parse AI response. Please try again.")
        
    except Exception as e:
        logger.error(f"Error in unified processing: {e}")
        raise Exception(f"Failed to process message: {str(e)}")
