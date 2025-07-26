https://www.loom.com/share/e26383c4bf81452494bcb2ea7d28189e

- `00:00–00:17` – Intro & setup  
  MarketAI is an AI-powered system that transforms trading predictions into structured, testable hypotheses. Users input a statement like “Apple will reach $300 by end of 2025” and click analyze.

- `00:17–00:31` – User input → Planning  
  Behind the scenes, a team of agents processes the input: one structures the hypothesis, one gathers supporting evidence, another finds contradicting evidence, and one synthesizes a summary with a confidence score.

- `00:31–01:11` – Tool calls & memory  
  The system outputs the confidence score (e.g., 35%), a reasoning summary, supporting and contradicting evidence, current stock data, growth estimates, and a raw JSON report for easy reuse.

- `01:11–01:27` – Final output & edge case handling  
  The backend is modular and cleanly separated into agents, tools, and orchestration logic. Lightweight frontend enables local interaction. MarketAI reframes financial speculation as structured, evidence-backed analysis.