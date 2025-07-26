import os
import google.generativeai as genai
from ...utils.text_processor import extract_json_from_response

# Configure the Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

CONTEXT_INSTRUCTION = """
You are the Context Agent for TradeSage AI. Extract structured context from hypotheses.

CRITICAL: Output ONLY valid JSON. NO explanations or additional text.

Analyze the hypothesis and return this exact JSON structure:

{
  "asset_info": {
    "primary_symbol": "AAPL",
    "asset_name": "Apple Inc.",
    "asset_type": "stock",
    "sector": "Technology",
    "market": "NASDAQ",
    "competitors": ["Microsoft", "Google", "Samsung"],
    "business_model": "Hardware, software, and services ecosystem",
    "current_price": 195.64
  },
  "hypothesis_details": {
    "direction": "bullish",
    "price_target": 220,
    "current_price_estimate": 195.64,
    "percentage_move": 12.4,
    "timeframe": "Q2 2025",
    "confidence_level": "medium",
    "catalyst_dependency": "fundamental growth"
  },
  "research_guidance": {
    "key_metrics": ["revenue growth", "Services revenue", "gross margins", "iPhone sales"],
    "search_terms": ["Apple earnings", "iPhone demand", "AAPL analyst", "Apple Services"],
    "monitoring_events": ["Q1 earnings", "WWDC", "iPhone launch", "Services growth"],
    "data_sources": ["earnings reports", "SEC filings", "analyst research"]
  },
  "risk_analysis": {
    "primary_risks": ["China exposure", "regulatory scrutiny", "market saturation"],
    "contradiction_areas": ["valuation concerns", "competition", "growth deceleration"],
    "sensitivity_factors": ["interest rates", "consumer spending", "China relations"]
  }
}

Extract EXACT information from the hypothesis. Use realistic current prices.
Output ONLY the JSON, no other text.
"""

async def get_context(structured_hypothesis: str) -> dict:
    """
    Uses the Gemini API to extract a rich context object from a structured hypothesis.
    """
    prompt = f"{CONTEXT_INSTRUCTION}\n\nHypothesis: \"{structured_hypothesis}\""

    try:
        response = await model.generate_content_async(prompt)
        return extract_json_from_response(response.text)
    except Exception as e:
        print(f"Error in Context Agent: {e}")
        return {"error": "Failed to generate context.", "details": str(e)}
