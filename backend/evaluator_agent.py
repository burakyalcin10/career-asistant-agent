"""
Response Evaluator Agent (Critic/Judge)
Evaluates generated responses before they are sent using LLM-as-a-Judge approach.
"""
import google.generativeai as genai
from config import settings
from models import EvaluationResult
import json
import logging
import re

logger = logging.getLogger(__name__)

genai.configure(api_key=settings.GEMINI_API_KEY)


EVALUATOR_PROMPT = """You are a Response Quality Evaluator for a Career Assistant AI Agent.
Your job is to critically evaluate the AI-generated response before it is sent to an employer.

EMPLOYER'S ORIGINAL MESSAGE:
{employer_message}

GENERATED RESPONSE:
{generated_response}

Evaluate the response on the following criteria (score each 1-10):

1. **professional_tone**: Is the tone professional, polite, and appropriate for employer communication?
2. **clarity**: Is the response clear, well-structured, and easy to understand?
3. **completeness**: Does the response adequately address the employer's message? Are all questions answered?
4. **safety**: Are there any hallucinations, false claims, or inappropriate content? (10 = completely safe)
5. **relevance**: Is the response relevant to the employer's specific message and needs?

Also provide:
- **overall_score**: The weighted average of all scores (1-10)
- **feedback**: Specific, actionable feedback for improvement if the score is below 7

IMPORTANT: Respond ONLY in valid JSON format with exactly these fields:
{{
    "professional_tone": <number>,
    "clarity": <number>,
    "completeness": <number>,
    "safety": <number>,
    "relevance": <number>,
    "overall_score": <number>,
    "feedback": "<string>"
}}
"""


async def evaluate_response(
    employer_message: str,
    generated_response: str
) -> EvaluationResult:
    """
    Evaluate a generated response using LLM-as-a-Judge.
    
    Args:
        employer_message: The employer's original message
        generated_response: The AI-generated response to evaluate
    
    Returns:
        EvaluationResult with scores and feedback
    """
    prompt = EVALUATOR_PROMPT.format(
        employer_message=employer_message,
        generated_response=generated_response
    )
    
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction="You are a strict but fair response quality evaluator. Always respond in valid JSON only."
        )
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up the response - remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = re.sub(r'^```(?:json)?\s*', '', response_text)
            response_text = re.sub(r'\s*```$', '', response_text)
        
        result = json.loads(response_text)
        
        overall_score = result.get("overall_score", 5.0)
        
        evaluation = EvaluationResult(
            overall_score=overall_score,
            professional_tone=result.get("professional_tone", 5.0),
            clarity=result.get("clarity", 5.0),
            completeness=result.get("completeness", 5.0),
            safety=result.get("safety", 5.0),
            relevance=result.get("relevance", 5.0),
            feedback=result.get("feedback", "No specific feedback."),
            passed=overall_score >= settings.EVALUATION_THRESHOLD
        )
        
        logger.info(f"Evaluation score: {overall_score}/10 - {'PASSED' if evaluation.passed else 'NEEDS REVISION'}")
        return evaluation
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse evaluator response: {e}")
        # Return a default passing evaluation if parsing fails
        return EvaluationResult(
            overall_score=7.0,
            professional_tone=7.0,
            clarity=7.0,
            completeness=7.0,
            safety=7.0,
            relevance=7.0,
            feedback="Evaluation parsing failed, using default scores.",
            passed=True
        )
    except Exception as e:
        logger.error(f"Evaluator error: {e}")
        raise Exception(f"Evaluation failed: {str(e)}")
