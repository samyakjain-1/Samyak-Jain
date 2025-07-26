import os
import google.generativeai as genai
from ...utils.text_processor import extract_json_from_response

# Configure the Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

ALERT_INSTRUCTION = """
You are the Alert Agent for TradeSage AI. Generate SPECIFIC, ACTIONABLE alerts.

CRITICAL: Output ONLY actionable alerts. NO meta-text or descriptions.

Based on confidence level, generate alerts like:

HIGH CONFIDENCE (70%+):
- "Enter 2-3% position in AAPL if price breaks above $197 with volume"
- "Set stop-loss at $185 (5.4% below entry) to limit downside"
- "Monitor Q1 earnings (Jan 30) for Services revenue confirmation"

MEDIUM CONFIDENCE (50-69%):
- "Wait for AAPL to establish support above $195 before entering"
- "Consider 1-2% initial position, add on strength above $200"
- "Watch for institutional buying signals above 50-day MA"

LOW CONFIDENCE (<50%):
- "Avoid entry until clearer trend emerges"
- "Monitor competitive pressures from Samsung/Google"
- "Wait for valuation to improve below 28x P/E"

Format as JSON array:
[
  {
    "type": "entry|risk|monitor|exit",
    "message": "Specific actionable alert",
    "priority": "high|medium|low"
  }
]

Generate 3-5 SPECIFIC alerts with exact price levels and actions.
"""

async def generate_alerts(final_report: dict) -> list:
    """
    Uses the Gemini API to generate actionable alerts based on the final report.
    """
    prompt = f"{ALERT_INSTRUCTION}\n\nFinal Report: {final_report}"

    try:
        response = await model.generate_content_async(prompt)
        return extract_json_from_response(response.text)
    except Exception as e:
        print(f"Error in Alert Agent: {e}")
        return [{"error": "Failed to generate alerts.", "details": str(e)}]
