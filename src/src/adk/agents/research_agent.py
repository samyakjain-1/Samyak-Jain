import os
import re
import google.generativeai as genai
from ...tools import news_tool, market_data_tool

# Configure the Gemini API key
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

RESEARCH_INSTRUCTION = """
You are the Research Agent for TradeSage AI. Gather SPECIFIC market data and analysis to support the hypothesis.

CRITICAL: Output ACTUAL data and findings, not descriptions of what you'll do.

Your research MUST include:
1. Current price: $XXX.XX
2. Target price: $XXX.XX
3. Required move: XX.X% to reach target
4. Key metrics: P/E, market cap, recent performance
5. Recent news: Specific headlines and dates that SUPPORT the hypothesis.

GOOD OUTPUT EXAMPLE:
"AAPL currently trades at $195.64, requiring 12.4% appreciation to reach $220 target.
P/E ratio: 32.5x (vs sector avg 25.2x)
Market cap: $3.04T
YTD performance: +8.2%
Recent news: 'Apple Vision Pro exceeds sales expectations' (WSJ, Jan 23)"

BAD OUTPUT (NEVER do this):
"I will research Apple's current price and calculate the required move"
"Let me look up the latest market data for AAPL"

Use the provided tool data to get REAL data, then present the ACTUAL findings.
NO meta-commentary about what you're doing.
"""

async def find_supporting_evidence(structured_hypothesis: dict) -> list:
    """
    Uses tools to find news and market data, then uses Gemini to format it as supporting evidence.
    """
    hypothesis_str = structured_hypothesis.get("structured_hypothesis", "")
    print(f"Research Agent is looking for evidence for: {hypothesis_str}")

    # Extract symbol and query from the hypothesis string
    symbol_match = re.search(r'\((.*?)\)', hypothesis_str)
    symbol = symbol_match.group(1) if symbol_match else ""
    query = hypothesis_str.split('(')[0].strip()

    # Use tools to get real data
    news_data = news_tool.search_news(query)
    market_data = market_data_tool.search_market_data(symbol)

    prompt = f"{RESEARCH_INSTRUCTION}\n\nHypothesis: \"{hypothesis_str}\"\n\nTool Data (News): {news_data}\n\nTool Data (Market): {market_data}"

    try:
        response = await model.generate_content_async(prompt)
        # The prompt asks for a direct string, so we wrap it in a list for consistency
        return [response.text.strip()]
    except Exception as e:
        print(f"Error in Research Agent: {e}")
        return [{"error": "Failed to generate research findings.", "details": str(e)}]
