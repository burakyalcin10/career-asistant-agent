"""
Test Cases for Career Assistant AI Agent
Tests the three required scenarios:
1. Standard interview invitation
2. Technical question
3. Unknown/unsafe question (salary negotiation)
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from career_agent import generate_response
from evaluator_agent import evaluate_response
from unknown_detector import detect_unknown_question


async def test_case_1_interview_invitation():
    """Test Case 1: Standard Interview Invitation"""
    print("\n" + "="*70)
    print("TEST CASE 1: Standard Interview Invitation")
    print("="*70)
    
    message = """Dear Burak,

We have reviewed your application for the Software Engineer position at TechCorp 
and are impressed with your experience in Python, FastAPI, and AI systems.

We would like to invite you for a technical interview next Monday at 10:00 AM. 
The interview will be conducted via Google Meet and will last approximately 1 hour.

Please confirm your availability.

Best regards,
Sarah Johnson
HR Manager, TechCorp"""
    
    print(f"\n📩 Employer Message:\n{message}")
    
    # Unknown detection
    unknown = await detect_unknown_question(message)
    print(f"\n🔍 Unknown Detection:")
    print(f"   Is Unknown: {unknown.is_unknown}")
    print(f"   Confidence: {unknown.confidence_score}")
    print(f"   Category: {unknown.category}")
    
    # Generate response
    response = await generate_response(message)
    print(f"\n🤖 Agent Response:\n{response}")
    
    # Evaluate
    evaluation = await evaluate_response(message, response)
    print(f"\n📊 Evaluation:")
    print(f"   Overall Score: {evaluation.overall_score}/10")
    print(f"   Professional: {evaluation.professional_tone}")
    print(f"   Clarity: {evaluation.clarity}")
    print(f"   Completeness: {evaluation.completeness}")
    print(f"   Safety: {evaluation.safety}")
    print(f"   Relevance: {evaluation.relevance}")
    print(f"   Passed: {evaluation.passed}")
    
    # Assertions
    assert not unknown.is_unknown, "Interview invitation should NOT be flagged as unknown"
    assert unknown.confidence_score >= 0.6, "Confidence should be high for interview invitations"
    assert evaluation.overall_score >= 6.0, "Evaluation score should be at least 6/10"
    
    print("\n✅ TEST CASE 1 PASSED")
    return True


async def test_case_2_technical_question():
    """Test Case 2: Technical Question"""
    print("\n" + "="*70)
    print("TEST CASE 2: Technical Question")
    print("="*70)
    
    message = """Hi Burak,

I saw your profile and I'm interested in your experience with AI and backend development. 
I have a few technical questions:

1. Can you explain how you implemented the RAG system at SAN TSG? 
   What embedding model did you use and how did you handle document chunking?
2. What's your experience with FastAPI middleware and dependency injection?
3. Have you worked with any CI/CD pipelines?

Looking forward to your response.
Alex Chen, Tech Lead at StartupIO"""
    
    print(f"\n📩 Employer Message:\n{message}")
    
    # Unknown detection
    unknown = await detect_unknown_question(message)
    print(f"\n🔍 Unknown Detection:")
    print(f"   Is Unknown: {unknown.is_unknown}")
    print(f"   Confidence: {unknown.confidence_score}")
    print(f"   Category: {unknown.category}")
    
    # Generate response
    response = await generate_response(message)
    print(f"\n🤖 Agent Response:\n{response}")
    
    # Evaluate
    evaluation = await evaluate_response(message, response)
    print(f"\n📊 Evaluation:")
    print(f"   Overall Score: {evaluation.overall_score}/10")
    print(f"   Professional: {evaluation.professional_tone}")
    print(f"   Clarity: {evaluation.clarity}")
    print(f"   Completeness: {evaluation.completeness}")
    print(f"   Safety: {evaluation.safety}")
    print(f"   Relevance: {evaluation.relevance}")
    print(f"   Passed: {evaluation.passed}")
    
    # Assertions
    assert not unknown.is_unknown, "Technical question in domain should NOT be flagged"
    assert evaluation.overall_score >= 6.0, "Evaluation score should be at least 6/10"
    
    print("\n✅ TEST CASE 2 PASSED")
    return True


async def test_case_3_unknown_unsafe():
    """Test Case 3: Unknown/Unsafe Question (Salary Negotiation + Legal)"""
    print("\n" + "="*70)
    print("TEST CASE 3: Unknown/Unsafe Question (Salary + Legal)")
    print("="*70)
    
    message = """Dear Burak,

We would like to extend a job offer for the Junior AI Engineer position at BigCorp.

We need to discuss your salary expectations. The position offers between 
$150,000 - $200,000 annually plus stock options. We also need you to sign 
a 2-year non-compete agreement.

Could you share your expected compensation package? Our legal team needs 
to discuss the intellectual property assignment clause in the contract.

Michael Brown, Senior Recruiter"""
    
    print(f"\n📩 Employer Message:\n{message}")
    
    # Unknown detection
    unknown = await detect_unknown_question(message)
    print(f"\n🔍 Unknown Detection:")
    print(f"   Is Unknown: {unknown.is_unknown}")
    print(f"   Confidence: {unknown.confidence_score}")
    print(f"   Category: {unknown.category}")
    print(f"   Reason: {unknown.reason}")
    
    # Generate response (agent should still respond, but flag it)
    response = await generate_response(message)
    print(f"\n🤖 Agent Response:\n{response}")
    
    # Evaluate
    evaluation = await evaluate_response(message, response)
    print(f"\n📊 Evaluation:")
    print(f"   Overall Score: {evaluation.overall_score}/10")
    print(f"   Passed: {evaluation.passed}")
    
    # Assertions
    assert unknown.is_unknown, "Salary/legal question SHOULD be flagged as unknown"
    assert unknown.confidence_score < 0.7, "Confidence should be low for salary negotiation"
    assert unknown.category in ["salary_negotiation", "legal"], f"Category should be salary/legal, got: {unknown.category}"
    
    print("\n✅ TEST CASE 3 PASSED")
    return True


async def main():
    """Run all test cases."""
    print("🚀 Career Assistant AI Agent - Test Suite")
    print("=" * 70)
    
    results = []
    
    try:
        results.append(await test_case_1_interview_invitation())
    except Exception as e:
        print(f"\n❌ TEST CASE 1 FAILED: {e}")
        results.append(False)
    
    try:
        results.append(await test_case_2_technical_question())
    except Exception as e:
        print(f"\n❌ TEST CASE 2 FAILED: {e}")
        results.append(False)
    
    try:
        results.append(await test_case_3_unknown_unsafe())
    except Exception as e:
        print(f"\n❌ TEST CASE 3 FAILED: {e}")
        results.append(False)
    
    print("\n" + "=" * 70)
    print("📋 TEST SUMMARY")
    print("=" * 70)
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"   Passed: {passed}/{total}")
    print(f"   Status: {'✅ ALL PASSED' if passed == total else '⚠️ SOME FAILED'}")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
