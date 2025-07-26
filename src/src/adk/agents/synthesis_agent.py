import os
import json
import google.generativeai as genai
from ...utils.text_processor import extract_json_from_response

# Configure the Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

SYNTHESIS_INSTRUCTION = """
You are the Synthesis Agent for TradeSage AI. Create a comprehensive investment analysis based on the provided evidence.

CRITICAL: Generate an ACTUAL analysis, not a summary of the inputs.

The final output must be a single JSON object with the following keys:
- "summary": A concise, balanced executive summary of the investment thesis.
- "confirmations": A JSON array of 3-5 specific, positive factors supporting the hypothesis. Use real data and metrics.
- "contradictions": A JSON array of 3-5 specific, negative factors or risks challenging the hypothesis.
- "confidence_score": A float between 0.15 and 0.85, representing your confidence in the hypothesis.
- "recommendation": A clear, final recommendation (e.g., "Favorable Outlook", "High Risk, High Reward", "Significant Headwinds").

RULES FOR "confirmations" and "contradictions":
- Each item in the array must be a JSON object with keys: "quote", "reason", "source", "strength".
- "quote" must be a specific, verifiable fact (e.g., "Apple Services revenue reached $85.2B in 2024...").
- "reason" must explain WHY this fact matters.
- "source" should be "Market Analysis" or a specific publication if available.
- "strength" must be "Strong", "Medium", or "Weak".

BAD EXAMPLES (NEVER generate these):
❌ "Summary: Apple presents a moderately attractive investment opportunity"
❌ "Buy"
❌ "Analysis shows positive factors"

Generate the complete JSON output based on the provided hypothesis and evidence.
"""

async def synthesize_evidence(
    structured_hypothesis: dict,
    supporting_evidence: list,
    contradictory_evidence: list
) -> dict:
    """
    Uses the Gemini API to synthesize all gathered evidence into a final report.
    """
    hypothesis_str = structured_hypothesis.get("structured_hypothesis", "")
    prompt = f"{SYNTHESIS_INSTRUCTION}\n\nHypothesis: \"{hypothesis_str}\"\n\nSupporting Evidence: {supporting_evidence}\n\nContradictory Evidence: {contradictory_evidence}\n\nJSON Output:"

    try:
        response = await model.generate_content_async(prompt)
        
        print("--- RAW GEMINI RESPONSE (SYNTHESIS AGENT) ---")
        print(response.text)
        print("---------------------------------------------")

        # Use the robust JSON extractor
        report = extract_json_from_response(response.text)
        return report
    except Exception as e:
        print(f"Error synthesizing evidence: {e}")
        return {
            "error": "Failed to synthesize evidence.",
            "details": str(e)
        }
