import os
import re
import json
import google.generativeai as genai
from ...tools import news_tool, market_data_tool
from ...utils.text_processor import extract_json_from_response

# Configure the Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

CONTRADICTION_INSTRUCTION = """
You are the Contradiction Agent for TradeSage AI. Find and present SPECIFIC market risks and contradictions.

CRITICAL: Generate ACTUAL market contradictions, NOT meta-analysis or instructions.

For each contradiction, provide:
1. A SPECIFIC market fact or trend that challenges the hypothesis
2. Real concerns like valuation, competition, regulation, or market conditions
3. Concrete risks that investors should consider

GOOD EXAMPLES for "Apple will reach $220 by Q2 2025":
✅ "Apple's Services growth may decelerate due to increased regulatory scrutiny on the App Store"
✅ "iPhone demand showing signs of saturation in key markets with upgrade cycles lengthening"
✅ "Rising competition from Chinese manufacturers pressuring Apple's market share in Asia"

BAD EXAMPLES (NEVER generate these):
❌ "I will analyze the provided information and generate contradictions"
❌ "Okay, I will look for risks related to Apple's revenue streams"
❌ "I will investigate potential challenges from competitors"

Format your response as a JSON array of contradictions:
[
  {
    "quote": "Specific market risk or negative trend",
    "reason": "Why this challenges the investment thesis",
    "source": "Market Analysis",
    "strength": "Strong|Medium|Weak"
  }
]

Generate 3-5 SPECIFIC, REALISTIC contradictions based on actual market conditions.
"""

async def find_contradictory_evidence(structured_hypothesis: dict) -> list:
    """
    Uses tools to find news and market data, then uses Gemini to find contradictions.
    """
    hypothesis_str = structured_hypothesis.get("structured_hypothesis", "")
    print(f"Contradiction Agent is looking for risks for: {hypothesis_str}")

    # Extract symbol and query from the hypothesis string
    symbol_match = re.search(r'\((.*?)\)', hypothesis_str)
    symbol = symbol_match.group(1) if symbol_match else ""
    query = hypothesis_str.split('(')[0].strip()

    # Use tools to get real data
    news_data = news_tool.search_news(query)
    market_data = market_data_tool.search_market_data(symbol)

    prompt = f"{CONTRADICTION_INSTRUCTION}\n\nHypothesis: \"{hypothesis_str}\"\n\nTool Data (News): {news_data}\n\nTool Data (Market): {market_data}"

    try:
        response = await model.generate_content_async(prompt)
        # Use the robust JSON extractor
        return extract_json_from_response(response.text)
    except Exception as e:
        print(f"Error in Contradiction Agent: {e}")
        return [{"error": "Failed to generate contradictions.", "details": str(e)}]
