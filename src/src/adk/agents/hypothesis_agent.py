import os
import google.generativeai as genai

# Configure the Gemini API key
# In a real app, use a more secure method like Secret Manager
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-2.0-flash')

HYPOTHESIS_INSTRUCTION = """
You are the Hypothesis Agent for TradeSage AI. Process and structure trading hypotheses.

CRITICAL: Output ONLY the clean, structured hypothesis statement. NO explanations or meta-text.

Transform input into this format: "[Company] ([Symbol]) will [direction] [target] by [timeframe]"

EXAMPLES:
Input: "I think Apple will go up to $220 by Q2 next year"
Output: Apple (AAPL) will reach $220 by end of Q2 2025

Input: "Bitcoin to hit 100k by end of year"
Output: Bitcoin (BTC-USD) will rise to $100,000 by year-end 2025

Input: "Oil prices will exceed $95 this summer"
Output: Crude Oil (CL=F) will exceed $95/barrel by summer 2025

RULES:
- Extract exact price targets and timeframes
- Use proper ticker symbols in parentheses
- Convert vague timeframes to specific ones (Q1/Q2/Q3/Q4 YYYY)
- Use clear action verbs: reach, rise to, decline to, exceed, fall below
- NO additional commentary, ONLY the hypothesis statement

Output the clean hypothesis statement directly.
"""

async def structure_hypothesis(query: str) -> dict:
    """
    Uses the Gemini API to convert a natural language query into a structured
    hypothesis.
    """
    prompt = f"{HYPOTHESIS_INSTRUCTION}\n\nHypothesis: \"{query}\""

    try:
        # The new prompt asks for a direct string, not JSON
        response = await model.generate_content_async(prompt)
        structured_statement = response.text.strip()
        
        # We will return this as a dictionary for consistency in the orchestrator
        return {
            "structured_hypothesis": structured_statement
        }
    except Exception as e:
        print(f"Error structuring hypothesis: {e}")
        return {
            "error": "Failed to structure hypothesis.",
            "details": str(e)
        }
